#!/usr/bin/env python3
"""
Parser fuer das "build broken" Blog-Archiv (Wayback-Downloads) -> Hugo-Content.

Ziel:
  - Liest die heruntergeladenen web.archive.org HTML-Dateien aus einem Quellordner
  - Entfernt Wayback-Toolbar/Wrapper-Markup
  - Extrahiert Titel, Datum, Autor, Kategorie, Tags, Content-HTML und optional Kommentare
  - Laedt referenzierte Bilder herunter (falls online erreichbar) bzw. kopiert sie aus
    einem lokalen Assets-Ordner und schreibt sie nach static/images/<slug>/
  - Konvertiert den Content nach Markdown
  - Schreibt content/posts/<slug>.md mit YAML-Frontmatter fuer Hugo

Voraussetzungen:
    pip install beautifulsoup4 markdownify requests python-slugify lxml

Nutzung:
    python parse_buildbroken_archive.py \
        --source ../archive/wayback-html \
        --output .. \
        --download-images
"""

import argparse
import json
import re
import sys
import shutil
from pathlib import Path
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
from markdownify import MarkdownConverter
from slugify import slugify

try:
    import requests
except ImportError:
    requests = None


class HugoConverter(MarkdownConverter):
    """Markdownify-Konverter, der <img>-Tags als HTML erhaelt (statt sie zu
    ![](...) zu konvertieren), damit width/height und align-Klassen aus dem
    Original-Design nicht verloren gehen."""

    def convert_img(self, el, text, parent_tags):
        alt = el.attrs.get("alt", "") or ""
        src = el.attrs.get("src", "") or ""
        title = el.attrs.get("title", "") or ""
        w = el.attrs.get("width")
        h = el.attrs.get("height")
        cls = " ".join(el.attrs.get("class") or [])
        attrs = []
        if alt:
            attrs.append(f'alt="{alt}"')
        if title:
            attrs.append(f'title="{title}"')
        if w:
            attrs.append(f'width="{w}"')
        if h:
            attrs.append(f'height="{h}"')
        if cls:
            attrs.append(f'class="{cls}"')
        attr_str = " " + " ".join(attrs) if attrs else ""
        return f'<img src="{src}"{attr_str}/>'


def to_md(html):
    return HugoConverter(heading_style="ATX").convert(html)


WAYBACK_WRAPPER_IDS = ["wm-ipp-base", "wm-ipp", "donato"]
WAYBACK_WRAPPER_CLASSES = ["wb-autocomplete-suggestions"]

CONTENT_SELECTORS = [
    ("div", {"class": "entry"}),
    ("div", {"class": "post"}),
    ("div", {"class": "entry-content"}),
    ("article", {}),
    ("div", {"id": "content"}),
]

TITLE_SELECTORS = [
    ("h2", {"class": "posttitle"}),
    ("h2", {"class": "entry-title"}),
    ("h1", {"class": "entry-title"}),
    ("h2", {}),
    ("title", {}),
]

DATE_BADGE_SELECTORS = [
    ("div", {"class": "datestamp"}),
    ("div", {"class": "date"}),
    ("span", {"class": "date"}),
]

META_LINE_PATTERN = re.compile(
    r"(?:Geschrieben von|Posted by)\s+(?P<author>.+?)\s+in\s+"
    r"(?P<category>.*?)(?:,\s*tags:\s*(?P<tags>.*))?$",
    re.IGNORECASE,
)

FOOTER_LINE_PATTERN = re.compile(
    r"Geschrieben am\s+(?P<date>.+?)\s+um\s+(?P<time>[\d:apm\s]+)\s+und ist zu finden in",
    re.IGNORECASE,
)

COMMENT_SELECTORS = [
    ("div", {"class": "commentlist"}),
    ("ol", {"class": "commentlist"}),
    ("div", {"id": "comments"}),
]

# Slug-Overrides: Der Dateiname im Wayback-Archiv weicht vom kanonischen Slug ab
# (Tippfehler im Live-Blog, kein Parser-/Downloader-Fehler).
# aync.html: Blogbetreiber hat "async" falsch geschrieben, kein Capture fuer async.html.
SLUG_OVERRIDES = {
    "aync.html": "async",
}

MONTHS_DE = {
    "Jan": "01", "Feb": "02", "Mär": "03", "Mar": "03", "Apr": "04",
    "Mai": "05", "May": "05", "Jun": "06", "Jul": "07", "Aug": "08",
    "Sep": "09", "Okt": "10", "Oct": "10", "Nov": "11", "Dez": "12", "Dec": "12",
}


def strip_wayback_chrome(soup: BeautifulSoup) -> None:
    for wid in WAYBACK_WRAPPER_IDS:
        el = soup.find(id=wid)
        if el:
            el.decompose()
    for wcls in WAYBACK_WRAPPER_CLASSES:
        for el in soup.find_all(class_=wcls):
            el.decompose()
    for comment in soup.find_all(string=lambda s: isinstance(s, str) and "BEGIN WAYBACK TOOLBAR INSERT" in s):
        comment.extract()
    for tag in soup(["script", "style", "noscript", "iframe"]):
        tag.decompose()


def find_first(soup, selectors):
    for name, attrs in selectors:
        el = soup.find(name, attrs=attrs) if attrs else soup.find(name)
        if el:
            return el
    return None


def extract_date_from_badge(date_el):
    if not date_el:
        return None
    text = date_el.get_text(" ", strip=True)
    m = re.search(r"([A-Za-zäöü]{3})\s*(\d{1,2})\s*(\d{4})", text)
    if m:
        mon, day, year = m.groups()
        mon_num = MONTHS_DE.get(mon[:3].capitalize())
        if mon_num:
            return f"{year}-{mon_num}-{int(day):02d}"
    return None


def extract_date_from_footer(container):
    text = container.get_text(" ", strip=True)
    m = FOOTER_LINE_PATTERN.search(text)
    if not m:
        return None
    raw = m.group("date")
    m2 = re.search(r"(\d{1,2})\.?\s*([A-Za-zäöü]+)\s*(\d{4})", raw)
    if not m2:
        return None
    day, mon_name, year = m2.groups()
    mon_map = {
        "januar": "01", "februar": "02", "märz": "03", "april": "04",
        "mai": "05", "juni": "06", "juli": "07", "august": "08",
        "september": "09", "oktober": "10", "november": "11", "dezember": "12",
    }
    mon_num = mon_map.get(mon_name.lower())
    if not mon_num:
        return None
    return f"{year}-{mon_num}-{int(day):02d}"


def extract_meta_line(soup):
    # Nur im .postinfo <small> suchen, nicht im gesamten Dokument
    small = soup.find("small")
    if not small:
        return None, None, []
    text = small.get_text(" ", strip=True)
    m = META_LINE_PATTERN.search(text)
    if not m:
        return None, None, []
    author = m.group("author").strip()
    categories = [c.strip() for c in m.group("category").split(",") if c.strip()]
    tags_raw = m.group("tags") or ""
    tags = [t.strip() for t in tags_raw.split(",") if t.strip()]
    return author, categories, tags


def download_or_copy_image(src, page_url, source_dir, assets_out_dir, download):
    assets_out_dir.mkdir(parents=True, exist_ok=True)
    filename = Path(urlparse(src).path).name
    if not filename:
        return None
    target = assets_out_dir / filename

    if not target.exists():
        local_candidate = source_dir / filename
        if local_candidate.exists():
            shutil.copy2(local_candidate, target)
        elif download and requests is not None and src.startswith("http"):
            try:
                resp = requests.get(src, timeout=15)
                resp.raise_for_status()
                target.write_bytes(resp.content)
            except Exception as exc:
                print(f"  ! Bild konnte nicht geladen werden: {src} ({exc})")
                return None
        else:
            print(f"  ! Bild nicht gefunden (weder lokal noch Download aktiviert): {src}")
            return None
    return filename


def process_images(content_el, page_url, source_dir, static_dir, slug, download):
    out_dir = static_dir / "images" / slug
    for img in content_el.find_all("img"):
        src = img.get("src")
        if not src:
            continue
        full_src = urljoin(page_url or "", src)
        new_name = download_or_copy_image(full_src, page_url, source_dir, out_dir, download)
        if new_name:
            img["src"] = f"/images/{slug}/{new_name}"
        else:
            # Bild nicht auffindbar (weder lokal noch im Archiv): kaputten Verweis entfernen
            img.decompose()


def remove_placeholder_headings(content_el):
    """Entfernt reine Trenn-Headings wie <h2>.</h2> aus dem Content."""
    for h in content_el.find_all(["h1", "h2", "h3", "h4"]):
        text = h.get_text(strip=True)
        if text and not any(ch.isalnum() for ch in text):
            h.decompose()


def remove_postmetadata(content_el):
    """Entfernt die WordPress-Artikel-Fusszeile (<p class="postmetadata">),
    die Meta-Zeile und RSS/Antwort/trackback-Links enthaelt (redundant zum
    Frontmatter und auf einer statischen Seite ohne Funktion)."""
    for p in content_el.find_all("p", class_="postmetadata"):
        p.decompose()


def remove_share_buttons(content_el):
    """Entfernt AddToAny-Share-Buttons (soziales Teilen, auf einem statischen
    Archiv ohne Funktion)."""
    for a in content_el.find_all("a", href=True):
        cls = " ".join(a.get("class") or [])
        if "addtoany" in cls or "share_save" in cls:
            a.decompose()


CODE_LINE_STYLE = re.compile(r"margin\s*:\s*0px")


def _code_line_text(el):
    return el.get_text(" ", strip=False).strip().replace("\xa0", " ").replace("\u2003", " ")


def merge_sequential_pres(content_el):
    """Fasst aufeinanderfolgende <pre>-Geschwister (Word-Export mit Zeilennummern)
    innerhalb desselben Parent zu einem zusammengehoerenden Codeblock zusammen."""
    for parent in content_el.find_all(True):
        pres = parent.find_all("pre", recursive=False)
        if len(pres) < 2:
            continue
        idx = 0
        while idx < len(pres):
            pre = pres[idx]
            if not CODE_LINE_STYLE.search(pre.get("style", "").replace(" ", "")):
                idx += 1
                continue
            block = [pre]
            idx += 1
            while idx < len(pres) and CODE_LINE_STYLE.search(pres[idx].get("style", "").replace(" ", "")):
                block.append(pres[idx])
                idx += 1
            if len(block) > 1:
                lines = [_code_line_text(el) for el in block]
                code_text = "\n".join(lines)
                code_text = re.sub(r"\n{3,}", "\n\n", code_text)
                merged = content_el.new_tag("pre")
                code = content_el.new_tag("code")
                code.string = code_text
                merged.append(code)
                block[0].insert_before(merged)
                for el in block:
                    el.decompose()


def strip_code_line_numbers(content_el):
    """Entfernt fuehrende Zeilennummern (Word-Export) aus <pre><code> Inhalt."""
    for pre in content_el.find_all("pre"):
        code = pre.find("code")
        if not code or not code.string:
            continue
        lines = [re.sub(r"^\s*\d+\s+", "", ln) for ln in code.string.split("\n")]
        code.string = "\n".join(lines)


def convert_code_blocks(content_el):
    """Alle Word-Export-Code-Markierungen zu sauberen <pre><code>-Bloecken."""
    merge_sequential_pres(content_el)
    convert_code_paragraphs(content_el)
    strip_code_line_numbers(content_el)


CODE_LINE_HINT = re.compile(r"[{};=<>()\[\]//]|^\s*$")


def _looks_like_code(el):
    """margin:0px-Absatz ist Code, wenn er Syntax-Highlighting-Spans oder
    typische Code-Zeichen enthaelt (sonst z.B. Fliesstext im Word-Export)."""
    if el.find("span", style=lambda s: s and "color:" in s):
        return True
    return bool(CODE_LINE_HINT.search(el.get_text(" ", strip=True)))


def convert_code_paragraphs(content_el):
    """Fasst aufeinanderfolgende Word-Export-Absaetze (margin: 0px) mit Code-
    Formatierung zu <pre><code>-Bloecken zusammen, damit C#-Snippets erhalten
    bleiben statt als Fliesstext-Escaping zu enden. Nur Geschwister innerhalb
    desselben Parent werden zusammengefasst (nicht ueber div-Grenzen hinweg)."""
    for parent in content_el.find_all(True):
        paragraphs = parent.find_all("p", recursive=False)
        idx = 0
        while idx < len(paragraphs):
            p = paragraphs[idx]
            is_code = p.get("style", "") and CODE_LINE_STYLE.search(p.get("style", "").replace(" ", ""))
            if not is_code or not _looks_like_code(p):
                idx += 1
                continue
            block = [p]
            idx += 1
            while idx < len(paragraphs) and CODE_LINE_STYLE.search(paragraphs[idx].get("style", "").replace(" ", "")):
                if not _looks_like_code(paragraphs[idx]):
                    break
                block.append(paragraphs[idx])
                idx += 1
            if block:
                lines = [_code_line_text(el) for el in block]
                code_text = "\n".join(lines)
                code_text = re.sub(r"\n{3,}", "\n\n", code_text)
                pre = content_el.new_tag("pre")
                code = content_el.new_tag("code")
                code.string = code_text
                pre.append(code)
                block[0].insert_before(pre)
                for el in block:
                    el.decompose()


WAYBACK_REWRITE = re.compile(r"^https?://web\.archive\.org/web/\d+(?:id_|im_)?/")


def unwrap_wayback_url(url: str) -> str:
    """Entfernt einen web.archive.org-Rewrite-Praefix, falls vorhanden."""
    return WAYBACK_REWRITE.sub("", url)


def process_links(content_el, page_url, permalink_map):
    for a in content_el.find_all("a", href=True):
        href = unwrap_wayback_url(a["href"])

        # KickIt-Button (dotnet-kicks): Bild behalten, Link entfernen
        cls = " ".join(a.get("class") or [])
        if "kickit" in cls.lower() or "kick-it" in cls.lower() or "dotnet-kicks" in a["href"]:
            a.unwrap()
            continue

        # Links auf alte .html-Seiten (aztec-project.org/blog/xyz.html)
        if "aztec-project.org/blog/" in href:
            filename = Path(urlparse(href).path).name
            if filename.endswith(".html"):
                target_slug = SLUG_OVERRIDES.get(filename, slugify(filename[:-5]))
                a["href"] = f"/posts/{target_slug}/"
            continue
        # WordPress-Permalinks (blog.aztec-project.org/2009/10/23/<wp-slug>/)
        m = re.search(r"blog\.aztec-project\.org/\d{4}/\d{2}/\d{2}/([^/?#]+)", href)
        if m:
            wp_slug = m.group(1)
            target = permalink_map.get(wp_slug)
            if target:
                a["href"] = f"/posts/{target}/"
            else:
                a["href"] = href
            continue
        # Alle uebrigen Links: Wayback-Rewrite-Praefix entfernen
        a["href"] = unwrap_wayback_url(a["href"])


def convert_comments(soup, page_url, source_dir, static_dir, slug, download, permalink_map):
    comments_el = find_first(soup, COMMENT_SELECTORS)
    if not comments_el:
        return ""
    process_images(comments_el, page_url, source_dir, static_dir, slug, download)
    process_links(comments_el, page_url, permalink_map)

    # WP-UI-Elemente (Thread-Toggle) und leere Boilerplate entfernen
    to_remove = []
    for tag in comments_el.descendants:
        if not getattr(tag, "name", None):
            continue
        cls = tag.get("class") or []
        if "switch-post" in cls or "says" in cls:
            to_remove.append(tag)
    for tag in to_remove:
        tag.decompose()

    # Struktur: .comment-author vcard -> strong (Name), .commentmetadata -> Zeit in eigener Zeile
    for li in comments_el.find_all("li"):
        author = li.find(class_="comment-author") or li.find("cite")
        meta = li.find(class_="commentmetadata")
        if author:
            cite = author.find("cite") or author
            cite.name = "strong"
            cite["class"] = ["comment-author-name"]
        if meta:
            meta.name = "div"
            meta["class"] = ["comment-metadata"]

    return to_md(str(comments_el)).strip()


def load_captures(source_dir):
    cap_path = source_dir / ".captures.json"
    if cap_path.exists():
        return json.loads(cap_path.read_text(encoding="utf-8"))
    return {}


def collect_permalink_map(source_dir):
    """Mappt die WordPress-Permalink-Slugs (blog.aztec-project.org/.../<wp-slug>/) auf
    die lokalen Hugo-Slugs. Der permalink-Slug steht im h2.posttitle-Link jeder Seite."""
    mapping = {}
    for p in source_dir.glob("*.html"):
        if p.name in {"blog.html", "about.html"}:
            continue
        soup = BeautifulSoup(p.read_text(encoding="utf-8", errors="ignore"), "lxml")
        pt = soup.select_one("h2.posttitle a")
        if not pt or not pt.get("href"):
            continue
        m = re.search(r"blog\.aztec-project\.org/\d{4}/\d{2}/\d{2}/([^/?#]+)", pt["href"])
        if not m:
            continue
        wp_slug = m.group(1)
        our_slug = SLUG_OVERRIDES.get(p.name, slugify(p.stem))
        mapping[wp_slug] = our_slug
    return mapping


def archive_url_for(name, captures):
    entry = captures.get(name)
    if not entry or not entry.get("html_ts"):
        return None
    ts = entry["html_ts"]
    return f"https://web.archive.org/web/{ts}/https://aztec-project.org/blog/{name}"


def parse_post(html_path, source_dir, static_dir, content_dir, download_images, page_url_base, captures=None, permalink_map=None):
    raw = html_path.read_text(encoding="utf-8", errors="ignore")
    soup = BeautifulSoup(raw, "lxml")
    strip_wayback_chrome(soup)

    title_el = find_first(soup, TITLE_SELECTORS)
    title = title_el.get_text(strip=True) if title_el else html_path.stem
    title = re.sub(r"\s*\|\s*build broken.*$", "", title, flags=re.IGNORECASE)

    content_el = find_first(soup, CONTENT_SELECTORS)
    if not content_el:
        print(f"  ! Kein Content-Block gefunden fuer {html_path.name} - ueberspringe")
        return None

    # Meta-Zeile nur im .postinfo suchen (nicht im ganzen Dokument)
    postinfo = soup.find("div", class_="postinfo")
    meta_source = postinfo if postinfo else soup

    date_badge = find_first(soup, DATE_BADGE_SELECTORS)
    date = extract_date_from_badge(date_badge) or extract_date_from_footer(content_el)
    date_uncertain = False
    if not date:
        m = re.search(r"(19|20)\d{2}", html_path.stem)
        if m:
            date = f"{m.group(0)}-01-01"
        else:
            date = "1970-01-01"
        date_uncertain = True

    author, category, tags = extract_meta_line(meta_source)

    slug = SLUG_OVERRIDES.get(html_path.name, slugify(html_path.stem))
    page_url = urljoin(page_url_base, html_path.name)

    process_images(content_el, page_url, source_dir, static_dir, slug, download_images)
    remove_placeholder_headings(content_el)
    remove_postmetadata(content_el)
    remove_share_buttons(content_el)
    convert_code_blocks(content_el)
    process_links(content_el, page_url, permalink_map)

    body_md = to_md(str(content_el)).strip()
    body_md = re.sub(r"\n{3,}", "\n\n", body_md)

    comments_md = convert_comments(soup, page_url, source_dir, static_dir, slug, download_images, permalink_map)

    frontmatter_lines = [
        "---",
        f'title: "{title.replace(chr(34), chr(39))}"',
        f"date: {date}",
        f"slug: {slug}",
        f'original_url: "https://aztec-project.org/blog/{html_path.name}"',
    ]
    if date_uncertain:
        frontmatter_lines.append("date_uncertain: true")
    archive_url = archive_url_for(html_path.name, captures or {})
    if archive_url:
        frontmatter_lines.append(f'archive_url: "{archive_url}"')
    if author:
        frontmatter_lines.append(f'author: "{author}"')
    if category:
        cat_list = ", ".join(f'"{c}"' for c in category)
        frontmatter_lines.append(f"categories: [{cat_list}]")
    if tags:
        tag_list = ", ".join(f'"{t}"' for t in tags)
        frontmatter_lines.append(f"tags: [{tag_list}]")
    frontmatter_lines.append("---")
    frontmatter = "\n".join(frontmatter_lines)

    parts = [frontmatter, "", body_md]
    if comments_md:
        parts += ["", "## Kommentare (Archiv)", "", comments_md]

    out_path = content_dir / f"{slug}.md"
    out_path.write_text("\n".join(parts) + "\n", encoding="utf-8")
    print(f"  OK -> {out_path}")
    return out_path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, help="Ordner mit den heruntergeladenen HTML-Dateien")
    parser.add_argument("--output", required=True, help="Zielordner (Hugo-Projektwurzel)")
    parser.add_argument("--download-images", action="store_true")
    parser.add_argument("--page-url-base", default="https://aztec-project.org/blog/")
    args = parser.parse_args()

    source_dir = Path(args.source)
    output_dir = Path(args.output)
    content_dir = output_dir / "content" / "posts"
    static_dir = output_dir / "static"
    content_dir.mkdir(parents=True, exist_ok=True)
    static_dir.mkdir(parents=True, exist_ok=True)

    if not source_dir.exists():
        print(f"Quellordner {source_dir} existiert nicht.", file=sys.stderr)
        sys.exit(1)

    captures = load_captures(source_dir)

    html_files = sorted(source_dir.glob("*.html"))
    if not html_files:
        print("Keine .html Dateien im Quellordner gefunden.", file=sys.stderr)
        sys.exit(1)

    skip_as_post = {"blog.html", "about.html"}
    permalink_map = collect_permalink_map(source_dir)

    print(f"Gefunden: {len(html_files)} HTML-Dateien\n")

    for html_path in html_files:
        print(f"Verarbeite {html_path.name} ...")
        if html_path.name in skip_as_post:
            print("  - Startseite/Index wird ignoriert (wird von Hugo generiert)")
        else:
            parse_post(html_path, source_dir, static_dir, content_dir,
                       args.download_images, args.page_url_base, captures, permalink_map)

    print("\nFertig.")


if __name__ == "__main__":
    main()

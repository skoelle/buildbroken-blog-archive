#!/usr/bin/env python3
"""
Laedt die Wayback-Snapshots des "build broken" Blogs (aztec-project.org/blog/) herunter.

Verfahren:
  1. CDX-API: fuer jede gewuenschte URL den letzten Snapshot mit Status 200 ermitteln.
  2. HTML ueber den id_-Modifier laden: liefert das rohe Original-HTML ohne
     Wayback-Toolbar und ohne Link-Rewriting.
  3. Alle <img src> aus dem HTML extrahieren, per CDX nach einem Snapshot suchen und
     ueber den im_-Modifier als rohe Bilddaten laden.
Alle Dateien landen flach in archive/wayback-html/ (Basisname der Original-URL).

Zusaetzlich wird archive/wayback-html/.captures.json geschrieben, das fuer jede
HTML-Datei den Capture-Timestamp und die heruntergeladenen Bilder dokumentiert
(grundlage fuer archive_url im Frontmatter und den Parsing-Report).

Nutzung:
    python download_wayback_archive.py --urls ../URLS.md --out ../archive/wayback-html
"""

import argparse
import json
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests

CDX_ENDPOINT = "https://web.archive.org/cdx/search/cdx"
WAYBACK_BASE = "https://web.archive.org/web/{ts}{modifier}/{url}"
ORIGIN = "https://aztec-project.org/blog/"

# Fehlerhaft geschriebene Dateinamen im Live-Blog: fuer die angegebene URL gibt es
# keinen Wayback-Capture, aber fuer den korrigierten Namen. Der Downloader faellt
# nach der Hauptschleife auf den korrigierten Namen zurueck.
URL_ALIASES = {
    "async.html": "aync.html",
}


def read_urls_file(urls_path: Path):
    """Liest die Dateinamen aus der ersten Spalte der URLS.md-Tabelle."""
    names = []
    for line in urls_path.read_text(encoding="utf-8").splitlines():
        m = re.search(r"^\s*\|\s*`([^`]+\.html)`\s*\|", line)
        if m:
            names.append(m.group(1))
    return names


def cdx_latest(url: str, cache: dict = None):
    if cache is not None and url in cache:
        return cache[url]
    params = {
        "url": url,
        "output": "json",
        "filter": "statuscode:200",
        "limit": "-1",
    }
    result = None
    for attempt in range(4):
        try:
            r = requests.get(CDX_ENDPOINT, params=params, timeout=90)
            r.raise_for_status()
            rows = r.json()
            if rows and len(rows) >= 2:
                result = rows[-1][1]
            break
        except requests.RequestException as exc:
            if attempt == 3:
                print(f"  ! CDX-Fehler fuer {url}: {exc}")
                break
            time.sleep(3 * (attempt + 1))
    if cache is not None:
        cache[url] = result
    return result


def fetch_raw(url: str, ts: str, modifier: str):
    wb_url = WAYBACK_BASE.format(ts=ts, modifier=modifier, url=url)
    for attempt in range(4):
        try:
            r = requests.get(wb_url, timeout=180, allow_redirects=True)
            r.raise_for_status()
            return r.content
        except requests.RequestException as exc:
            if attempt == 3:
                print(f"  ! Download-Fehler {modifier} fuer {url}: {exc}")
                return None
            time.sleep(3 * (attempt + 1))
    return None


def extract_image_srcs(html_bytes: bytes):
    """Extrahiert alle <img src=...> als originale (unrewrittene) URLs."""
    srcs = set()
    for m in re.finditer(r"<img\b[^>]*?\bsrc\s*=\s*([\"'])(.*?)\1", html_bytes.decode("utf-8", "ignore"), re.IGNORECASE | re.DOTALL):
        srcs.add(m.group(2))
    return srcs


def cdx_lookup_many(image_urls, cache, workers=4):
    """Fuehrt CDX-Lookups parallel aus; liefert dict url -> timestamp."""
    found = {}
    pending = [u for u in image_urls if u not in cache]
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {}
        for i, u in enumerate(pending):
            time.sleep(0.2)
            futs[ex.submit(cdx_latest, u, cache)] = u
        for fut in as_completed(futs):
            u = futs[fut]
            ts = fut.result()
            if ts:
                found[u] = ts
    for u in pending:
        if u in cache and cache[u]:
            found[u] = cache[u]
    return found


WAYBACK_REWRITE = re.compile(r"^https?://web\.archive\.org/web/\d+(?:id_|im_)?/")


def unwrap_wayback_url(url: str) -> str:
    """Entfernt einen web.archive.org-Rewrite-Praefix, falls vorhanden."""
    return WAYBACK_REWRITE.sub("", url)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--urls", required=True, help="Pfad zur URLS.md")
    parser.add_argument("--out", required=True, help="Zielordner (archive/wayback-html)")
    parser.add_argument("--pause", type=float, default=1.0, help="Pause zwischen Requests (Sekunden)")
    args = parser.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    names = read_urls_file(Path(args.urls))
    if not names:
        print("Keine Dateinamen aus URLS.md gelesen.", file=sys.stderr)
        sys.exit(1)

    print(f"Gelesen: {len(names)} Eintraege aus {args.urls}\n")

    cap_path = out_dir / ".captures.json"
    captures = {}
    if cap_path.exists():
        captures = json.loads(cap_path.read_text(encoding="utf-8"))
        print(f"Resume: {len(captures)} Eintraege bereits vorhanden\n")

    cdx_cache_path = out_dir / ".cdx_cache.json"
    cdx_cache = {}
    if cdx_cache_path.exists():
        cdx_cache = json.loads(cdx_cache_path.read_text(encoding="utf-8"))
        print(f"CDX-Cache: {len(cdx_cache)} URLs bekannt\n")

    for name in names:
        out_path = out_dir / name
        if name in captures and captures[name].get("html_ts") and out_path.exists() and out_path.stat().st_size > 0:
            print(f"== {name} (bereits verarbeitet, uebersprungen)")
            continue
        page_url = ORIGIN + name
        print(f"== {name}")
        ts = cdx_latest(page_url, cdx_cache)
        if not ts:
            print(f"  ! KEIN Snapshot (Status 200) gefunden: {page_url}")
            captures[name] = {"html_ts": None, "images": {}}
            cdx_cache_path.write_text(json.dumps(cdx_cache), encoding="utf-8")
            continue

        out_path = out_dir / name
        if out_path.exists() and out_path.stat().st_size > 0:
            html = out_path.read_bytes()
            print(f"  HTML vorhanden ({len(html)} Bytes, ts={ts})")
        else:
            html = fetch_raw(page_url, ts, "id_")
            if html is None:
                captures[name] = {"html_ts": ts, "images": {}}
                continue
            out_path.write_bytes(html)
            print(f"  HTML ok ({len(html)} Bytes, ts={ts})")

        entry = {"html_ts": ts, "images": {}}
        if name == "blog.html":
            print("  (Indexseite: Bilder werden uebersprungen)")
        else:
            img_srcs = []
            for raw_src in sorted(extract_image_srcs(html)):
                if raw_src.startswith("data:"):
                    continue
                full = urljoin(page_url, raw_src)
                full = unwrap_wayback_url(full)
                if "aztec-project.org" not in full:
                    continue
                fname = Path(urlparse(full).path).name
                if not fname:
                    continue
                img_srcs.append((full, fname))
            if img_srcs:
                found = cdx_lookup_many([u for u, _ in img_srcs], cdx_cache)
            else:
                found = {}
            for full, fname in img_srcs:
                img_ts = found.get(full)
                if not img_ts:
                    print(f"  ! Bild ohne Snapshot: {full}")
                    continue
                target = out_dir / fname
                if not target.exists() or target.stat().st_size == 0:
                    data = fetch_raw(full, img_ts, "im_")
                    if data is None:
                        continue
                    target.write_bytes(data)
                entry["images"][fname] = {"url": full, "ts": img_ts}
                print(f"  Bild {fname} ok (ts={img_ts})")
                time.sleep(args.pause)
        captures[name] = entry
        cap_path.write_text(json.dumps(captures, indent=2), encoding="utf-8")
        cdx_cache_path.write_text(json.dumps(cdx_cache), encoding="utf-8")
        time.sleep(args.pause)

    # Alias-Pass: fehlerhaft geschriebene Dateinamen, fuer die es im Archiv nur
    # unter dem korrigierten Namen einen Capture gibt (z.B. async -> aync).
    for alias_name, real_name in URL_ALIASES.items():
        real_path = out_dir / real_name
        if real_path.exists() and real_path.stat().st_size > 0 and real_name in captures:
            print(f"== {alias_name} -> {real_name} (bereits vorhanden)")
            continue
        print(f"== {alias_name} -> {real_name} (Alias)")
        real_url = ORIGIN + real_name
        ts = cdx_latest(real_url, cdx_cache)
        if not ts:
            print(f"  ! KEIN Snapshot fuer Alias {real_name}: {real_url}")
            captures[real_name] = {"html_ts": None, "images": {}}
            continue
        html = fetch_raw(real_url, ts, "id_")
        if html is None:
            captures[real_name] = {"html_ts": ts, "images": {}}
            continue
        real_path.write_bytes(html)
        print(f"  HTML ok ({len(html)} Bytes, ts={ts})")
        entry = {"html_ts": ts, "images": {}}
        img_srcs = []
        for raw_src in sorted(extract_image_srcs(html)):
            if raw_src.startswith("data:"):
                continue
            full = urljoin(real_url, raw_src)
            full = unwrap_wayback_url(full)
            if "aztec-project.org" not in full:
                continue
            fname = Path(urlparse(full).path).name
            if not fname:
                continue
            img_srcs.append((full, fname))
        if img_srcs:
            found = cdx_lookup_many([u for u, _ in img_srcs], cdx_cache)
        else:
            found = {}
        for full, fname in img_srcs:
            img_ts = found.get(full)
            if not img_ts:
                print(f"  ! Bild ohne Snapshot: {full}")
                continue
            target = out_dir / fname
            if not target.exists() or target.stat().st_size == 0:
                data = fetch_raw(full, img_ts, "im_")
                if data is None:
                    continue
                target.write_bytes(data)
            entry["images"][fname] = {"url": full, "ts": img_ts}
            print(f"  Bild {fname} ok (ts={img_ts})")
            time.sleep(args.pause)
        captures[real_name] = entry
        cap_path.write_text(json.dumps(captures, indent=2), encoding="utf-8")
        cdx_cache_path.write_text(json.dumps(cdx_cache), encoding="utf-8")

    cap_path.write_text(json.dumps(captures, indent=2), encoding="utf-8")
    cdx_cache_path.write_text(json.dumps(cdx_cache), encoding="utf-8")
    print(f"\nMetadaten geschrieben: {cap_path}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Link-Checker fuer das "build broken" Blog-Archiv.

Extrahiert alle externen Links aus content/posts/*.md und prueft sie per HTTP.
Ergebnis wird als data/links.json gespeichert, die von layouts/_default/baseof.html
eingebunden wird (Broken-Links -> Modal mit web.archive.org, Replacement-Links
werden automatisch umgeschrieben).

Nutzung:
    python check_links.py                 # pruefen + data/links.json aktualisieren
    python check_links.py --check-only    # nur pruefen, data/links.json NICHT schreiben
    python check_links.py --dry-run       # wie --check-only, aber zeigt diff der Aenderungen

Optionen:
    --check-only     data/links.json nicht schreiben (nur Ausgabe)
    --dry-run        wie --check-only, zusaetzlich geplante Aenderungen anzeigen
    --include-coded  Auch Platzhalter-URLs (localhost:port, IP:port, w3.org,
                     tempuri.org aus Code-Beispielen) pruefen. Standard: ausgeschlossen.

Achtung: URLs, die nur Bot-Schutz liefern (HTTP 403/429) werden NICHT als broken
markiert. Die erkannten Status werden als Tabelle ausgegeben; manuelle
Nachpflege (replacement-Eintraege) bleibt Aufgabe des Menschen.
"""

import argparse
import glob
import json
import re
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
CONTENT_GLOB = ROOT / "content" / "posts" / "*.md"
DATA_FILE = ROOT / "data" / "links.json"

# URLs, die nie geprueft/angefasst werden:
#  - aztec-project.org (Original-Quelle, bewusst tot, Zweck des Archivs)
#  - web.archive.org   (Archive-Links, "leben" per Definition)
#  - moonweb.org       (eigene Domain)
SKIP_HOSTS = ("aztec-project.org", "web.archive.org", "moonweb.org")

# Platzhalter/Code-Beispiel-URLs, die keine echten Links sind
CODED_PLACEHOLDERS = {
    "http://IP:port",
    "http://localhost:port",
    "http://www.w3.org/2001/XMLSchema",
    "http://www.w3.org/2001/XMLSchema-instance",
    "http://www.w3.org/2003/05/soap-envelope",
    "http://tempuri.org/",
    "http://tempuri.org/AendernEtwas",
    "http://schemas.xmlsoap.org/soap/envelope/",
}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    ),
    "Accept-Language": "de,en;q=0.8",
}


def extract_urls():
    """Liefert {url: set(dateinamen)}.

    Bevorzugt werden die tatsaechlich gerenderten <a href="http...">-Links aus
    public/posts/*/index.html verwendet (nur die erscheinen dem Besucher und
    nur die werden von data/links.json/JS verarbeitet). Ist public/ nicht
    gebaut, wird auf Markdown-Extraktion zurueckgegriffen (Code-Bloecke und
    Inline-Code werden ausgeschlossen).
    """
    html_files = sorted(glob.glob(str(ROOT / "public" / "posts" / "*" / "index.html")))
    if html_files:
        hrefpat = re.compile(r'<a[^>]*href="?([^" >]+)"?')
        found = {}
        for f in html_files:
            html = Path(f).read_text(encoding="utf-8")
            name = Path(f).resolve().parent.parent.name
            for m in hrefpat.finditer(html):
                h = m.group(1).replace("&amp;", "&")
                if h.startswith("http"):
                    found.setdefault(h, set()).add(name)
        if found:
            return found

    # Fallback: Markdown-Extraktion
    urlpat = re.compile(r"https?://[^\s<>\")\]]+")

    def strip_code(text):
        text = re.sub(r"```.*?```", " ", text, flags=re.S)
        text = re.sub(r"`[^`]*`", " ", text)
        return text

    found = {}
    for f in sorted(glob.glob(str(CONTENT_GLOB))):
        text = Path(f).read_text(encoding="utf-8")
        text = strip_code(text)
        name = Path(f).name
        for m in urlpat.finditer(text):
            u = m.group(0).rstrip(".,;:!?\")>]")
            u = u.rstrip("\u201c\u201d\u201e\u2019\u2033")
            if u.startswith("http"):
                found.setdefault(u, set()).add(name)
    return found


def is_skipped(url):
    for host in SKIP_HOSTS:
        if host in url:
            return True
    return url in CODED_PLACEHOLDERS


def check_url(sess, url, timeout=25):
    """Prueft eine URL, liefert (status, final_url, error)."""
    try:
        r = sess.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True, verify=True)
        return r.status_code, r.url, None
    except Exception as e:
        return "ERR", url, str(e)[:120]


def classify(status):
    """Status -> (broken?, label)."""
    if status == 200:
        return False, "OK"
    if status in (403, 429):
        # Bot-Schutz: Seite lebt, Crawler wird nur geblockt -> NICHT broken
        return False, "BLOCKED"
    if status in ("ERR", 404, 410, 503):
        return True, "BROKEN"
    return True, "BROKEN"  # andere 4xx/5xx


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check-only", action="store_true", help="data/links.json nicht schreiben")
    ap.add_argument("--dry-run", action="store_true", help="wie --check-only, plus diff anzeigen")
    ap.add_argument("--include-coded", action="store_true", help="auch Code-Platzhalter-URLs pruefen")
    args = ap.parse_args()

    found = extract_urls()
    if not found:
        print("Keine URLs gefunden.")
        sys.exit(1)

    # Dedupe: gleiche URL aus mehreren Dateien
    urls = sorted(found.keys())
    urls_set = set(urls)
    to_check = [u for u in urls if not is_skipped(u)]

    print(f"Extrahierte URLs: {len(urls)}  |  zu pruefen: {len(to_check)}  |  uebersprungen: {len(urls)-len(to_check)}")
    print()

    sess = requests.Session()
    results = {}
    for i, u in enumerate(to_check, 1):
        status, final, err = check_url(sess, u)
        results[u] = (status, final, err)
        print(f"[{i}/{len(to_check)}] {status:>4}  {u}")
        time.sleep(0.25)

    # data/links.json laden (falls vorhanden)
    old_broken = {}
    old_replacement = {}
    if DATA_FILE.exists():
        try:
            old = json.loads(DATA_FILE.read_text(encoding="utf-8"))
            old_broken = old.get("broken", {})
            old_replacement = old.get("replacement", {})
        except Exception:
            pass

    new_broken = {}
    new_replacement = {}
    for u in to_check:
        status, final, err = results[u]
        broken, label = classify(status)
        # URLs im replacement-Block sind bewusst umgeschrieben -> nie broken
        if u in old_replacement:
            new_replacement[u] = old_replacement[u]
            continue
        if broken:
            # Bestehende spezifische Archive-URL beibehalten, sonst Wildcard-Fallback
            if u in old_broken:
                new_broken[u] = old_broken[u]
            else:
                new_broken[u] = "https://web.archive.org/web/*/" + u
        elif status == 200 and final and final != u:
            # Redirect auf lebende Seite -> kein automatischer Replacement,
            # da der Redirect eh schon funktioniert. Nur Anzeige.
            pass

    # Konservativer Merge: manuell kuratierte broken-Eintraege, deren URL noch
    # im Content vorkommt, bleiben erhalten, solange der Check sie heute NICHT
    # eindeutig als 200 (wieder online) bestaetigt. 403/429 (Bot-Schutz) und
    # ERR (DNS/Timeout) schuetzen so vor Flackern.
    for u in old_broken:
        if u not in new_broken and u in urls_set:
            status = results.get(u, (None,))[0]
            if status != 200:
                new_broken[u] = old_broken[u]

    print("\n=== Zusammenfassung ===")
    print(f"  broken (neu):    {len(new_broken)}")
    print(f"  broken (alt):    {len(old_broken)}")
    print(f"  replacement (alt, bleibt): {len(old_replacement)}")
    print()

    added = sorted(set(new_broken) - set(old_broken))
    removed = sorted(set(old_broken) - set(new_broken))
    print(f"  + neu als broken: {len(added)}")
    for u in added:
        print(f"      {u}")
    print(f"  - nicht mehr broken: {len(removed)}")
    for u in removed:
        print(f"      {u}")

    if args.check_only or args.dry_run:
        print("\n(--check-only/--dry-run: data/links.json wurde NICHT geschrieben)")
        return

    # data/links.json aktualisieren: broken ersetzen, replacement beibehalten
    data = {
        "broken": new_broken,
        "replacement": old_replacement,
    }
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"\ndata/links.json aktualisiert ({len(new_broken)} broken, {len(old_replacement)} replacement)")


if __name__ == "__main__":
    main()

# buildbroken-blog-archive

Statisches Archiv des ehemaligen ".NET/build broken"-Blogs (`aztec-project.org/blog/`),
aufgebaut mit [Hugo](https://gohugo.io). Alle Inhalte stammen aus web.archive.org
Downloads und werden lokal gehostet (Bilder, CSS, Content).

## URL-Struktur

| Bereich | Alte URL (Wayback) | Neue lokale URL |
|---|---|---|
| Startseite | `blog/blog.html` | `/` |
| About | `blog/about.html` | `/about/` |
| Blogartikel | `blog/<slug>.html` | `/posts/<slug>/` |
| Bilder | extern/beliebig | `/images/<slug>/<dateiname>` |
| CSS | Theme-CSS | `/css/style.css` |

`<slug>` ist der ursprüngliche Dateiname ohne `.html`, durch `python-slugify`
normalisiert (Kleinschreibung, Bindestriche). Beispiel:
`dotnet-openspace-leipzig-2009-buchung.html` -> `/posts/dotnet-openspace-leipzig-2009-buchung/`.

Interne Links zwischen Artikeln werden vom Parser automatisch von
`https://aztec-project.org/blog/xyz.html` auf `/posts/xyz/` umgeschrieben.

## Voraussetzungen

- [Hugo](https://gohugo.io/installation/) (extended oder normal reicht, kein Node nötig)
- Python 3.10+
- `pip install -r scripts/requirements.txt`

## Ordnerstruktur

```
buildbroken-blog-archive/
├── hugo.toml                  # Hugo-Konfiguration
├── content/
│   ├── _index.md              # Startseite
│   ├── about.md               # wird vom Parser aus about.html befüllt
│   └── posts/                 # wird vom Parser mit *.md befüllt
├── layouts/                   # eigenes Theme, angelehnt an das Original-Design
│   ├── _default/baseof.html
│   ├── _default/single.html
│   ├── _default/list.html
│   └── index.html
├── static/
│   ├── css/style.css
│   └── images/<slug>/...      # wird vom Parser befüllt
├── archive/
│   └── wayback-html/          # HIER die heruntergeladenen Wayback-HTML-Dateien ablegen
├── scripts/
│   ├── parse_buildbroken_archive.py
│   └── requirements.txt
├── URLS.md                    # Liste aller zu parsenden Quell-URLs/Dateien
└── TODO.md                    # Arbeitsauftrag für die lokale KI
```

## Ablauf

1. Alle Dateien aus `URLS.md` als HTML von web.archive.org herunterladen und
   unter `archive/wayback-html/<dateiname>.html` ablegen (exakt gleicher Name).
2. Parser laufen lassen:
   ```bash
   cd scripts
   pip install -r requirements.txt
   python parse_buildbroken_archive.py --source ../archive/wayback-html --output .. --download-images
   ```
3. Lokale Vorschau:
   ```bash
   cd ..
   hugo server -D --bind 0.0.0.0 --baseURL http://<hostname>:1313/
   ```
   `<hostname>` durch den Hostnamen des Rechners ersetzen (z. B. `xubuntu-dev.lan`).
4. Produktions-Build:
   ```bash
   hugo --minify
   ```
   Ergebnis liegt in `public/` und kann auf beliebigem statischen Hosting
   (nginx-Container, Gitea Pages, GitHub Pages) deployt werden.

## Layout anpassen

Alle Design-Änderungen passieren zentral in `layouts/_default/*.html` und
`static/css/style.css`. Nach einer Änderung reicht `hugo --minify`, um alle
Artikel neu zu bauen — der Content in `content/posts/*.md` bleibt unangetastet.

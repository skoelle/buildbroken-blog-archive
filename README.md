# buildbroken-blog-archive

Statisches Archiv des ehemaligen ".NET/build broken"-Blogs (`aztec-project.org/blog/`),
aufgebaut mit [Hugo](https://gohugo.io). Alle Inhalte stammen aus web.archive.org
Downloads und werden lokal gehostet (Bilder, CSS, Content).

Die Blogartikel unter `content/posts/` und die zugehörigen Bilder wurden
ursprünglich von den Autoren von "build broken" (aztec-project.org, 2009–2010)
geschrieben und werden hier ausschließlich zu persönlichen Archivierungszwecken
aufbewahrt. Das Urheberrecht verbleibt bei den ursprünglichen Autoren; die
MIT-Lizenz dieses Repositories gilt nur für den Code (Parser-Skripte,
Hugo-Templates und CSS), nicht für die archivierten Bloginhalte selbst.

## URL-Struktur

| Bereich | Alte URL (Wayback) | Neue lokale URL |
|---|---|---|
| Startseite (inkl. About-Text) | `blog/blog.html` | `/` |
| About | `blog/about.html` | `/` (Text liegt auf der Startseite) |
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
│   ├── _index.md              # Startseite (About-Text liegt hier, kein eigenes /about/)
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
   > **Wichtig:** Der Parser soll **nicht mehr erneut ausgeführt** werden. Die
   > generierten Artikel in `content/posts/*.md` wurden nachträglich manuell
   > ausgebessert (Titel gekürzt, Tags korrigiert, `alt`-Attribute ergänzt,
   > Links umgeschrieben). Ein erneuter Lauf würde diese Handarbeit überschreiben.
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

## Hosting (Cloudflare Pages, migriert in Workers)

Das Projekt wird über die Cloudflare-Pages-**Git-Integration** deployed
(Pages wurde inzwischen in den Workers-Bereich migriert, das Prinzip ist
unverändert):

1. **GitHub-Repo** anlegen und dieses Projekt hineinpushen.
2. In Cloudflare unter **Workers & Pages → Create application → Pages** den
   Tab **Import an existing Git repository** wählen und das Repo auswählen.
3. Build-Einstellungen hinterlegen:
   - **Framework preset:** Hugo
   - **Build command (Bereitstellungsbefehl):** `hugo --minify`
   Ein eigenes **Build output directory** kann bei Cloudflare Pages nicht
   angegeben werden — es kommt aus der Hugo-Konfiguration (`publishDir` in
   `hugo.toml`, Standard `public`).
4. Speichern. Es ist **kein Deploy-Befehl nötig**: Jeder Push auf den
   verbundenen GitHub-Branch (z. B. `main`) baut und deployed automatisch.

Die `wrangler.json` im Projekt-Root konfiguriert das Deployment:
- `name`: Projektname (`buildbroken-blog-archive`)
- `compatibility_date`: Datum der Cloudflare-Laufzeit
- `assets.directory`: `public` — das Hugo-Ausgabeverzeichnis, das bereitgestellt wird
- `assets.not_found_handling`: `404-page` — liefert die eigene `public/404.html` (statt eines generischen 404) für nicht gefundene Pfade

## SEO

Das Layout erzeugt für jede Seite automatisch SEO-Metadaten (zentral in
`layouts/_default/baseof.html`):

- `meta name="description"` (aus Frontmatter/`.Description`, sonst aus `.Summary`; für Taxonomie-, Autor- und Archiv-Seiten generisch formuliert, auf ~160 Zeichen gekürzt)
- `link rel="canonical"` mit der absoluten URL
- Open-Graph- und Twitter-Card-Tags (`og:type` article/website, `og:image` Banner, `twitter:card` summary_large_image)
- `<title>`: Tag- und Kategorie-Seiten werden differenziert (`MVC (Tag)` vs. `MVC (Kategorie)`), Länge auf ~60 Zeichen begrenzt

Außerdem:

- Eigene `layouts/_default/404.html`, die via `assets.not_found_handling: "404-page"` von Cloudflare ausgeliefert wird
- `robots.txt` verweist auf `sitemap.xml` (Hugo-generiert)
- Content-Bilder in `content/posts/*.md` tragen `alt`-Attribute; der dekorative Banner hat bewusst leeres `alt=""`

## Layout anpassen

Alle Design-Änderungen passieren zentral in `layouts/_default/*.html` und
`static/css/style.css`. Nach einer Änderung reicht `hugo --minify`, um alle
Artikel neu zu bauen — der Content in `content/posts/*.md` bleibt unangetastet.

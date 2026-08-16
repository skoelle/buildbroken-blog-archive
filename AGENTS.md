# AGENTS.md

## Wichtigste Regel: Parser NICHT erneut ausführen

Der Parser `scripts/parse_buildbroken_archive.py` wurde **einmalig** genutzt, um die
Blogartikel aus den Wayback-HTML-Dateien zu generieren. Die Artikel in
`content/posts/*.md` wurden danach **manuell ausgebessert** (Titel gekürzt,
Tags korrigiert, `alt`-Attribute ergänzt, Links umgeschrieben). Ein erneuter
Parser-Lauf würde diese Handarbeit überschreiben und ist daher **verboten**.

Das gilt ebenso für `--download-images`: Bilder und Zuweisungen sind bereits
final; nichts neu herunterladen.

## Grundregeln

- **Kein `hugo server` im Hintergrund laufen lassen, wenn `public/` deployt
  werden soll** – der Dev-Server überschreibt `public/` laufend mit
  unminifizierten Dev-Artefakten (`livereload.js`). Für den Produktionsstand:
  `hugo --minify --cleanDestinationDir`.
- **Deployment:** Cloudflare-Workers über `wrangler.json`
  (`assets.directory: public`, `not_found_handling: 404-page`).
- **Content** in `content/posts/*.md` und `content/_index.md` wird von Hand
  gepflegt. Titel sollen unter ~60 Zeichen bleiben.
- **SEO-Metadaten** werden zentral in `layouts/_default/baseof.html` erzeugt
  (description/canonical/OG/Twitter). Keine Per-Post-Hardcodes außer nötig.
- **Bilder** in Posts brauchen ein `alt`-Attribut; der Banner ist dekorativ
  (`alt=""`).
- Die Startseite enthält den About-Text (kein eigenes `/about/` mehr);
  `about.html`-Redirects zeigen auf `/`.
- **Commits:** ohne Co-Autoren; nur der eigentliche Autor.

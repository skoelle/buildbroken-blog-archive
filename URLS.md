# Quell-URLs (web.archive.org Downloads)

Alle Dateien liegen als HTML unter `https://aztec-project.org/blog/<name>.html` und wurden von web.archive.org heruntergeladen. Lege die lokalen Kopien 1:1 mit gleichem Dateinamen unter `archive/wayback-html/` ab, bevor der Parser laeuft.

> **Hinweis Tippfehler im Live-Blog:** `async.html` hat KEINEN Wayback-Capture. Der Blogbetreiber hatte den Artikel im echten Blog fehlerhaft als `aync.html` gespeichert (Tippfehler, kein Parser-/Downloader-Bug). Der Downloader laedt deshalb `aync.html` (einzig verfuegbarer Capture mit Status 200 und echtem Content) und der Parser vergibt trotzdem den sauberen Slug `async`. `archive_url` verweist auf den tatsaechlichen Snapshot von `aync.html`, `original_url` auf die historische Original-URL `.../blog/aync.html`.

| Dateiname | Titel | Ziel |
|---|---|---|
| `blog.html` | Aztec Project Build Broken Blog Startseite | index (wird nicht als Post geparst) |
| `about.html` | Aztec Project Build Broken About Us | Startseite-Intro (in `_index.md`, kein eigenes `/about/`) |
| `dotnet-openspace-leipzig-2009-buchung.html` | .NET Open Space 2009 | post |
| `dotnet-openspace-leipzig-2009.html` | .NET Open Space 2009 in Leipzig (Bericht) | post |
| `dotnet-openspace-sued-2009-buchung.html` | .NET Open Space Süd 2009 | post |
| `dotnet-openspace-sued-2009.html` | .NET Open Space Süd 2009 (Bericht) | post |
| `webservice-mit-asp-classic.html` | .NET-Webservice mit ASP-Classic ansprechen | post |
| `asp-mvc-2.html` | ASP.MVC 2 - Vortrag von Albert bei münchener UserGroup | post |
| `anonyme-datentypen.html` | Anonyme Datentypen | post |
| `aync.html` | Asynchrone Kommunikation mit dem Async-Pattern | post (Slug `async`, Tippfehler im Live-Blog) |
| `async-refactored.html` | Asynchrone Kommunikation mit dem Async-Pattern (Refactored) | post |
| `barcamp-bodensee-2010.html` | BarCamp Bodensee 2010 | post |
| `clean-code-developer.html` | Clean-Code-Developer | entfällt → siehe `clean-code-developer-yellow-brick-road.html` |
| `clean-code-developer-yellow-brick-road.html` | Clean Code Developer - The Yellow Brick Road of the Coder | post |
| `cleancode1.html` | Clean Code Teil 1 | post |
| `cleancode2.html` | Clean Code Teil 2 | post |
| `design-by-contract.html` | Design by Contract - jetzt auch mit C# | post |
| `design-by-contract-teil2.html` | Design by Contract - jetzt auch mit C# - Teil 2 | post |
| `dime-casts.html` | Dime Casts WebCasts | post |
| `dynamic-load.html` | Dynamisches Laden von Assemblies | post |
| `alt-net-energien.html` | Gibt es negative Energien in der deutschen ALT.NET Bewegung? | post |
| `mvp-winforms-teil1.html` | MVP mit WinForms | entfällt → siehe `mvp-winforms.html` |
| `mvp-winforms.html` | MVP mit WinForms - Beispiel Model-View-Presenter mit WinForms | post |
| `prio-conference-2009.html` | prio.conference 2009 München | post |
| `refaktorisierung.html` | Refaktorisierung - mal anders erklärt | post |
| `scrumbut.html` | scrumbut | post |
| `softwarezellen.html` | Softwarezellen - eine Lösung um die Komplexität zu beherrschen | post |
| `stupiddb1.html` | StupidDB – object-persistence-framework | post |
| `stupiddb2.html` | NoSQL mit StupidDB | post |
| `test-public-methods.html` | Testen von nicht öffentlichen Methoden | post |
| `plugin-pattern.html` | Umsetzung des Plug-In-Patterns | post |
| `unittests-webforms.html` | Unit-Tests für WebForms | post |
| `code-to-html.html` | Visual Studio Code in HTML umwandeln | post |
| `webcamps.html` | Webcamps München | post |
| `reflection.html` | Wozu dient Reflection | post |
| `programmierer.html` | (Spreu + Weizen).Select(Programmierer) | post |

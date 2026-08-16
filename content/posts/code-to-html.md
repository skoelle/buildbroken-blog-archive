---
title: "Visual Studio Code in HTML umwandeln"
date: 2009-06-06
slug: code-to-html
original_url: "https://aztec-project.org/blog/code-to-html.html"
archive_url: "https://web.archive.org/web/20250114134712/https://aztec-project.org/blog/code-to-html.html"
author: "Andreas Seebauer"
categories: ["Visual Studio Addins"]
tags: ["Addin", "HTML", "Sourcecode", "Visual Studio", "Wordpress"]
---

Da wir kein geeignetes Plugin für Wordpress gefunden haben, um .NET-Code wie in Visual Studio darzustellen, habe ich ein wenig gegooglet und bin auf ein Addin namens “Copy Source As HTML” für Visual Studio 2008 gestoßen. Mit diesem Addin ist es möglich, seinen Sourcecode schön formatiert in HTML umzuwandeln.

Downloadlink und Anleitung findet man [hier](http://www.jtleigh.com/people/colin/software/CopySourceAsHtml/).

Nach der Installation steht im Kontextmenü neben Copy, Paste usw. auch der Punkt “Copy As HTML…” zur Verfügung. Bevor der umgewandelte Sourcecode in den Zwischenspeicher gespeichert wird, hat man die Möglichkeit, seine Konfiguration anzupassen.

Hierfür habe ich folgende Konfiguration verwendet:

<img src="/images/code-to-html/config.jpg" alt="Config"/>

Nach der Bestätigung der Konfiguration sieht das Ergebnis folgendermaßen aus :

```
///   <summary>
///  Summary
///   </summary>
class   Program  {
static   void  Main() {
// Kommentar
Console .WriteLine( "Hello World" );
}
}
```

## Kommentare (Archiv)

1. **Stefan Kölle**

   [Juni 9, 2009 um 12:23](/posts/code-to-html/)

   Leider kann man den Code vom Blog dann nur schwer wieder in Visual Studio zurueck kopieren.
2. **Thomas Christian**

   [Juni 10, 2009 um 11:45](/posts/code-to-html/)

   Wenn man die “Number lines from” weglässt, dann kann man den Code wieder gut aus der Seite kopieren.

---
title: "Softwarezellen – eine Lösung um die Komplexität zu beherrschen"
date: 2010-01-27
slug: softwarezellen
original_url: "https://aztec-project.org/blog/softwarezellen.html"
archive_url: "https://web.archive.org/web/20250601101252/https://aztec-project.org/blog/softwarezellen.html"
author: "Christina Hirth"
categories: ["Architektur", "Clean Code Developing"]
tags: ["Architektur"]
---

Wir haben wie viele von uns in der Webentwicklung vor vielen Jahren mit Scriptsprachen und mit prozeduralen – Spaghetti-Code <img src="/images/softwarezellen/icon_wink.gif" alt=";)" class="wp-smiley"/> – angefangen. Mit der Zeit wuchs unsere Webpräsenz zu einer unüberschaubaren Anwendung mit manchen Seiten, die keiner von uns mehr anfassen wollte – aus Angst vor den Konsequenzen.

Um etwas Ordnung in die Webanwendungen zu bringen, haben wir also vor 4 Jahren angefangen, nach einem 3-Schichten-Modell zu entwickeln. Wir haben neue Funktionalitäten und neue Anwendungen nur noch so gebaut und wir waren für eine kurze Zeit zufrieden. Alles lief gut. Als wir den Umstieg auf .NET begonnen haben, haben wir weiterhin nach einem Mehr-Schichten-Modell gearbeitet, wir haben nur die Anzahl der Schichten erhöht.

Die Anwendungen wuchsen weiter, wir haben immer mehr Bereiche ausgelagert und diese hauptsächlich mit Webservices angesprochen. Währenddessen waren wir daran, unser Hauptprodukt, ein Portal für unseren Kunden mit der neuen Technologie entsprechend der alten Anforderung neu zu bauen. Und dann ist es passiert: ehe wir uns versahen, hatten wir ein riesiges Projekt, das alle mögliche Anwendungen eingebunden bzw. durch Webservices angesprochen hat. Die Grenzen waren fließend, eventuelle Änderungen an anderen Anwendungen konnten das Projekt unbuildbar machen, also ein ähnlicher Zustand wie vor paar Jahren zuvor.

Die Weiterentwicklung hat nicht nur in unserer Art zu Programmieren stattgefunden, wir selbst haben uns auch weiterentwickelt, wir haben die Community kennen gelernt. Bei den Open Space-Veranstaltungen haben wir [Stefan](http://lieser-online.de/) und [Ralf](http://ralfw.de/default.html) kennengelernt und durch sie eine andere Sichtweise der Dinge: die [Modellierung einer Lösung durch Softwarezellen](http://weblogs.asp.net/ralfw/archive/tags/Software+Cells/default.aspx).

Wir haben sie zu uns eingeladen und uns die Idee erklären lassen. Das Stichwort heißt [Holon](http://de.wikipedia.org/wiki/Holon). Wikipedia definiert ein Holon folgendermaßen:

> Der Begriff Holon (von griech. ὅλος, hólos und ὀν, on „ganzes Seiendes“) wurde von Arthur Koestler geprägt und bedeutet ein Ganzes, das Teil eines anderen Ganzen ist. Es wird auch als “Ganzes/Teil” umschrieben.

Jede Anwendung ist ein Ganzes, die aus Teilen besteht, die ihrerseits auch als Ganze zu betrachten sind.

Seit dem Besuch von Ralf und Stefan haben wir uns die Artikelserie von Ralf von [dotnetpro](http://dotnetpro.de/) durchgelesen, die Webcasts ([Teil 1](https://www.microsoft.com/germany/msdn/webcasts/library.aspx?id=1032298692), [Teil 2](https://www.microsoft.com/germany/msdn/webcasts/library.aspx?id=1032298700)) angeschaut und wir haben angefangen, diese Modellierung auszuprobieren.

Wir haben noch einen langen und interessanten Weg vor uns, aber eins ist jetzt schon sicher: wir werden versuchen unsere nächste Projekte durch Softzellen modellieren.

Solange die Komplexität nicht wieder die Überhand gewinnt <img src="/images/softwarezellen/icon_wink.gif" alt=";)" class="wp-smiley"/>

<img src="/images/softwarezellen/KickItImageGenerator.ashx" alt="kick it on dotnet-kicks.de"/>

## Kommentare (Archiv)

1. **[Tweets that mention build broken » Softwarezellen – eine Lösung um die Komplexität zu beherrschen -- Topsy.com](http://topsy.com/tb/bit.ly/aYQGup)**

   [Januar 28, 2010 um 12:53 am](/posts/softwarezellen/)

   [...] This post was mentioned on Twitter by .NET German Bloggers, DeveloperBlogs. DeveloperBlogs said: Softwarezellen – eine Lösung um die Komplexität zu beherrschen: Wir haben wie viele von uns in der Webentwicklung … <http://bit.ly/aYQGup> [...]
2. **Benjamin Gopp**

   [Januar 28, 2010 um 8:28 am](/posts/softwarezellen/)

   Hallo,  
   schön zu hören, dass noch andere den CCD Weg gehen!  
   Wir haben mit Ralf und Stefan die School of .NET gemacht. Die Architektur hat uns am Anfang echt Schwierigkeiten gemacht. Vielleicht weil wir bisher überhaupt keine Architektur betrieben haben. Jetzt stellen wir jedoch fest, dass das Vorgehen, so wie es Ralf und Stefan es lehren wirklich einen Quantensprung bedeutet.

   Hinfort mit Schichtenarchitektur und UML!

   Benjamin

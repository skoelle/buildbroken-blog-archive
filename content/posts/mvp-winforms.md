---
title: "Beispiel Model-View-Presenter mit WinForms"
date: 2010-02-16
slug: mvp-winforms
original_url: "https://aztec-project.org/blog/mvp-winforms.html"
archive_url: "https://web.archive.org/web/20250114132109/https://aztec-project.org/blog/mvp-winforms.html"
author: "Stefan Kölle"
categories: ["How-To", "MVC"]
tags: ["Contract-First", "MVP", "WinForms"]
---

Im Teil 1 ([MVP mit WinForms](/posts/mvp-winforms/)) habe ich die Grundgedanken zur Implementierung von MVP in WinForms vorgestellt, mit der man WinForm-Anwendungen mit UnitTests abdecken kann. In einer komplexeren WinForm-Anwendung gibt es neben dem Startform auch mehrere Unterforms, die durch das Hauptform aufgerufen werden müssen.

**Das Beispielprojekt**  
Zur Demonstration habe ich ein Beispielprogramm mit MVP entwickelt, welches einen sehr einfachen Twitterclient darstellt. Das Beispiel wurde nach Contract-First komponentenorientiert gebaut und besteht neben der MVP-Komponente aus weiteren Komponenten.

[<img src="/images/mvp-winforms/Foto1.jpg" title="TwitterClient Architektur" width="200" height="159" class="alignnone size-full wp-image-900" alt="TwitterClient Architektur"/>](/images/mvp-winforms/Foto1.jpg)

Die weiteren Komponenten haben nichts mit MVP zu tun, sondern sollen nur zeigen, wie man MVP in diesem Umfeld integriert. -> [Den kompletten Sourcecode downloaden](/assets/TwitterClient.zip)

Die Funktionen des Twitter-Clients sollen sein:  
1. Anzeige der 20 neuesten Meldungen aus der Timeline im Hauptfenster  
2. Der Benutzer soll Status-Updates bei Twitter posten können  
3. Die Zugangsdaten des Twitter-Accounts sollen gespeichert werden können

**Die WinForm-Komponente**

Um die Funktionen abzubilden, sind 3 Screens notwendig:  
1. Hauptbildschirm mit der Timeline des Twitter-Accounts  
2. Form für das Absenden eines Twitter-Status-Updates  
3. Konfigurationsbildschirm für den Twitter-Account

[<img src="/images/mvp-winforms/Foto2-300x143.jpg" title="TwitterClient UI" width="300" height="143" class="alignnone size-medium wp-image-901" alt="TwitterClient UI"/>](/images/mvp-winforms/Foto2.jpg)

Jedes WinForm besteht aus einer View-Klasse (dem WinForm), einem Model, welches als Singleton im IoC-Container konfiguriert wird und einem Presenter. Die einzelnen Funktionen in den Views sind im Beispielprojekt durch Tests abgedeckt und zeigen die notwendigen Tests für diese Art der Implementierung. Gerade durch geringen Funktionsumfang kann man das Muster der Verwendung gut erkennen.

In der MVP-Komponente befindet sich auch der “Inversion of Control”-Container, der die einzelnen Komponenten zusammenfügt. Dies könnte auch in einer extra Runner-Komponente ausgelagert sein.

**Aufrufen eines weiteren WinForms**  
Alle Abhängigkeiten werden per Dependency-Injection-Container an den Presenter übergeben. Da das Hauptform alle weiteren Views und Presenter instanziert, müssten diese alle bereits beim Programmstart instanziert werden. Um dies zu verhindern, habe ich eine IPresenterFactory eingeführt, die zur Laufzeit weitere Presenter nachinstanzieren kann. Die Factory selbst hält eine Referenz auf den Container und wird bei Programmstart im Container hinzugefügt. Um sicherzustellen, dass weiterhin alle anderen Abhängigkeiten über den Konstruktor definiert werden, können aus dieser Factory nur Klassen instanziert werden, die IPresenter implementieren.

**Fazit**  
Mit dieser Beispielanwendung kann man eine mögliche Implementierung von Model View Presenter in der Variante Supervising Controller sehen. Es ist also auch mit WinForms eine voll getestete MVP-Implementierung zu erstellen.

Anhang:  
[Kompletter Sourcecode der Beispielanwendung als ZIP](/assets/TwitterClient.zip)

<img src="/images/mvp-winforms/KickItImageGenerator.ashx" alt="kick it on dotnet-kicks.de"/>

## Kommentare (Archiv)

1. **[Jan Selke](http://jcselke.blogspot.com/)**

   [Februar 16, 2010 um 9:19 am](/posts/mvp-winforms/)

   Hallo,  
   ich finde die Anwendung sehr schön und es sind die Eine oder Andere Anregung für mich auch enthalten <img src="/images/mvp-winforms/icon_smile.gif" alt="" class="wp-smiley"/> .  
   Die Konfiguration über Xml würde ich vielleicht noch versuchen zu eliminieren, es wird ja schönes Benennungsmuster eingehalten (CoC).  
   Ich habe es zwar noch nicht laufen lassen, es sah aber im TimelinePresenter so aus, als wenn noch ein versehentliches Verlassen verhindert werden könnte…  
   Viele Grüße,  
   Jan
2. **[Stefan Kölle](http://www.stefankoelle.de/)**

   [Februar 19, 2010 um 5:36 pm](/posts/mvp-winforms/)

   Hallo Jan,

   danke fuer deinen Input, das Container.xml ist wirklich nicht schoen und koennte man sicher eleganter loesen. Du hast mich da auf eine gute Idee gebracht.

   Was meinst du mit versehenliches Verlassen?

   Gruss  
   Stefan
3. **[Jan Christian Selke](http://jcselke.blogspot.com/)**

   [Februar 22, 2010 um 12:27 pm](/posts/mvp-winforms/)

   Hallo nochmal,

   freut mich, wenn ich damit einen Impuls geben konnte.

   Zu dem versehentlichen Verlassen:  
   Ich habe vor Kurzem etwas über das “graceful exit” einer Anwendung gelesen. Deine Anwendung hatte ich nicht gestartet, sondern mir nur den Quellcode quergelesen. Dabei ist mir aufgefallen, dass nur ein Application.Exit beim Close ausgeführt wird, der Anwender erhält keine Chance doch in der Anwendung zu bleiben. Eventuell habe ich es auch einfach nicht gesehen (habe es ja auch nicht laufen lassen)…  
   Soll kein Mäkeln an Kleinigkeiten sein, sondern eher ein Beispiel dafür, dass mir die Anwendung recht gut gefällt. <img src="/images/mvp-winforms/icon_wink.gif" alt="" class="wp-smiley"/>

   Viele Grüße,  
   Jan

---
title: "ASP.MVC 2 – Vortrag von Albert bei münchener UserGroup"
date: 2009-10-30
slug: asp-mvc-2
original_url: "https://aztec-project.org/blog/asp-mvc-2.html"
archive_url: "https://web.archive.org/web/20250114131627/https://aztec-project.org/blog/asp-mvc-2.html"
author: "Christina Hirth"
categories: ["MVC"]
tags: [".NET", "Community", "MVC", "Veranstaltung"]
---

Gestern Abend waren wir alle bei einem super Vortrag von [Albert](http://der-albert.com/) über ASP.MVC v2. Die neue Version soll am 22. März zusammen mit .NET 4.0 rauskommen.  
Ich will jetzt nicht über all die Neuigkeiten sprechen, die wir gestern erfahren haben und worüber wir uns jetzt schon freuen müssen, nur über einen speziellen Teil: die Validierung der Daten durch Attribute.

Der Grund ist folgender: wir haben uns vor ca. 1 Jahr ein eigenes Attribut namens `ObligatoryFieldAttribut` gebaut. Dieses wird über die Properties gesetzt, die wir für die Speicherung als unerheblich markieren möchten. Die Überprüfung erfolgt dann durch Reflection.

Und was haben wir gestern erfahren? In der neue MVC-Version gibt es ein neues Attribut namens `Required`, das genau das tut!

Ihr könnt euch sicher vorstellen, was wir uns gestern gedacht haben: wir lagen genau richtig und wir waren unserer Zeit voraus! Oder haben unsere Büro-Nachbarn – die eine *Microsoft Subsidiary* sind – Kameras bei uns installiert 😉 ?

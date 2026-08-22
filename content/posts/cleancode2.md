---
title: "Clean Code Teil 2"
date: 2009-11-04
slug: cleancode2
original_url: "https://aztec-project.org/blog/cleancode2.html"
archive_url: "https://web.archive.org/web/20250114122055/https://aztec-project.org/blog/cleancode2.html"
author: "Andreas Seebauer"
categories: ["Clean Code Developing"]
tags: ["Buch", "CCD", "Clean Code", "Coding"]
---

Endlich ist es geschafft. Ich habe das Buch “Clean Code” von Robert C. Martin a.k.a. Uncle Bob durchgelesen. Nach dem [ersten Teil](/posts/cleancode1/) hier nun die versprochene Fortsetzung meiner Zusammenfassung:

**10 Classes**

Die erste Regel von Klassen lautet: Sie sollten klein sein.  
Die zweite Regel von Klassen lautet: Sie sollten noch kleiner sein als das.

Klassen sollten eine hohe Kohäsion haben.  
Kohäsion ist ein Maß dafür, wie stark die Methoden und Daten einer Klasse miteinander zu tun haben. Zur Verdeutlichung:  
Eine Klasse, in der jede Membervariable von jeder Methode der Klasse verwendet wird, ist maximal kohäsiv.

Bei Klassen sollten folgende Prinzipien beachtet werden:

* Das **Single Responsibility Principle** (**SRP**), welches besagt:

Eine Klasse oder ein Modul sollte nur einen Grund haben sich zu ändern. Eine Klasse sollte sich nur um **EINE** Sache kümmern.

* Das **Open Close Principle** (**OCP**), welches besagt:

Klassen sollten offen für Erweiterungen sein, aber geschlossen für Modifikation.

* Das **Dependency Inversion Priniciple** (**DIP**), welches besagt:

Klassen sollten von Abstraktionen abhängen und nicht von konkreten Klassen.

**11 Systems**

Separiere Konstruktion von Benutzung.  
Realisiert werden kann das durch Dependency Injection.

Dependency Injection = Klassen bekommen ihre Abhängigkeiten von außen über den Konstruktor oder Setter übergeben. Dieses Pattern unterstützt das SRP, da sich die Klasse nicht mehr um das Instanzieren dieser Abhängigkeiten kümmern muss. Realisiert wird das ganze über Inversion of Control Container wie Windsor, Spring und wie sie alle heißen. Bei diesen Containern werden die Abhängigkeiten einmalig definiert, so dass man sich bei der Instanzierung nicht mehr darum kümmern muss.

Wenn Objekte zu einer bestimmten Zeit erstellt werden müssen, sollten Factories verwendet werden.

Systeme werden nicht von heute auf morgen gebaut. Sie werden nach und nach ausgebaut. Um sicherzustellen, dass dabei noch alles funktioniert, gibt es TDD, Refaktorisieren und Separation of Concerns.

**12 Emergence**

Viele Leute sagen, dass Kent Beck’s 4 “Rules of Simple Design” einem sehr helfen, gut designte Software zu erstellen.

Kent Beck sagt:  
ein Design ist „simple“, wenn:

* alle Tests durchlaufen
* kein doppelter Code vorhanden ist
* wenn es die Absicht des Programmierers ausdrückt
* die Anzahl von Klassen und Methoden minimiert sind

in der Reihenfolge.

**13 Concurrency**

In Multithread-Anwendungen bekommt man schon bei minimaler Anforderung ein Problem mit der Komplexität. Da mit steigender Komplexität auch die Fehleranfälligkeit steigt, gibt es ein paar Prinzipien, die diese minimieren können:

Die Concurrency Defense Principles

* **Single Responsibility Principle**

Trenne multithreaded Code von nicht-multithreaded Code

* **Limit the Scope of Data**

Man sollte den Bereich, in dem multithreaded Code verwendet wird, möglichst klein halten.

* **Use Copies of Data**

Verschiedene Threads sollten nicht mit demselben Objekt arbeiten. Wenn möglich sollte mit Kopien von diesem Objekt gearbeitet werden.

* **Independence**

Threads sollten so unabhängig wie möglich sein

* **Library**

Natürlich sollte man die Bibliothek, die man für Multithread-Anwendungen verwendet, sehr gut kennen.

**14 Successive Refinement**

Um Clean Code schreiben zu können, muss man erst Dirty Code schreiben und ihn dann bereinigen.

Einer der besten Wege, ein Programm zu ruinieren, ist, massive Änderungen an der Struktur vorzunehmen, um das Programm zu verbessern. Um das zu verhindern, nutzt man die Disziplinen von TDD. Eines der zentralen Doktrinen dieses Ansatzes ist es, das System zu jeder Zeit lauffähig zu halten. Mit TDD ist es also nicht erlaubt eine Veränderung am System vorzunehmen, die das System bricht.

**15 JUnit Internals**

JUnit Internals halt… (Kapitel überlesen)

**16 Refactoring SerialDate**

War mir eindeutig zu Java-lastig… (Kapitel überlesen)

**17 Smells and Heuristics**

In diesem Kapitel zeigt Uncle Bob eine Liste von Smells und wie man sie beseitigen kann. Er lobt das Buch “Refactoring” von Martin Fowler. Dieses Buch steht eh schon ganz oben auf meiner To-do-Liste. Das werde ich also demnächst angehen.

**Zusammenfassung**

An dieser Stelle ein Dank an mein Entwicklerteam, dass ich das Buch so lange in Beschlag nehmen durfte <img src="/images/cleancode2/icon_smile.gif" alt="" class="wp-smiley"/> (Teil 2 ging irgendwie zäher). Einen großen Dank auch an [Peter Bucher](http://www.aspnetzone.de/blogs/peterbucher/) und [Rene Drescher-Hackel](http://weblog.drescher-hackel.de/) für ihre Ergänzungen bzw. Einwände. Man darf sicherlich nicht alles so ganz ernst nehmen und man kann es auch übertreiben (siehe Pyramiden etc.). Natürlich sollte man nicht blind durch die Welt laufen, sondern auch Dinge hinterfragen, aber man muss sagen, dass die Punkte von [CCD](http://www.clean-code-developer.de/) (das ja auf diesem Buch beruht) durchaus plausibel sind. Ich denke schon, dass [CCD](http://www.clean-code-developer.de/) unerfahrenen aber auch erfahrenen Entwicklern einen SOLIDen Weg zeigt, den man gehen kann und der sogar schon gepflastert ist. Man kann sich natürlich auch mit der Machete durch dichten Dschungel schlagen, was natürlich cool ist <img src="/images/cleancode2/icon_smile.gif" alt="" class="wp-smiley"/> – aber halt wesentlich langsamer. Es sei denn man ist Chuck Norris.

<img src="/images/cleancode2/KickItImageGenerator.ashx" alt="kick it on dotnet-kicks.de"/>

## Kommentare (Archiv)

1. **[build broken » Clean Code Teil 1](/posts/cleancode1/)**

   [November 4, 2009 um 4:20 pm](/posts/cleancode2/)

   [...] Teil 2 gibt es hier [...]

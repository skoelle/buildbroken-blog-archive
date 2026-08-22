---
title: "Clean Code Teil 1"
date: 2009-08-11
slug: cleancode1
original_url: "https://aztec-project.org/blog/cleancode1.html"
archive_url: "https://web.archive.org/web/20250114133226/https://aztec-project.org/blog/cleancode1.html"
author: "Andreas Seebauer"
categories: ["Clean Code Developing"]
tags: ["Basics", "Buch", "CCD", "Clean Code", "Coding"]
---

[<img src="/images/cleancode1/c0025902_49cff1bd96e00-225x300.jpg" alt="Clean Code" title="Clean Code" width="95" height="126" class="size-medium wp-image-505 alignleft"/>](/images/cleancode1/c0025902_49cff1bd96e00-225x300.jpg)

Da es für einen Entwickler wichtig ist, sich ständig weiterzuentwickeln, sollte man sich durch Austausch mit anderen Entwicklern, aktives Programmieren oder eben Bücher weiterbilden. Das Buch, das ich gerade lese, heißt Clean Code von Robert C. Martin a.k.a. Uncle Bob. Ich bin momentan bei der Hälfte des Buches und muss sagen, dass ich von dem Buch ziemlich begeistert bin. Da ich denke, dass es vielen Entwicklern helfen würde, besseren Code zu schreiben, habe ich den Text ein wenig verkürzt und zusammengefasst – was natürlich nicht heißt, dass man dieses Buch nicht lesen muss. Meiner Meinung nach ist es absolute Pflichtlektüre für jeden Entwickler, der was auf sich hält.

Hier also meine kleine Zusammenfassung.

### Kapitel 1 Clean Code

In diesem Kapitel wird beschrieben, was Clean Code ist und dass man „Clean Code“ schreiben muss, um sich selbst einen professionellen Softwareentwickler nennen zu dürfen. Was Clean Code ausmacht, hat [Christina](/author/christina-hirth/) schon in ihrem Artikel [„Clean Code Developer – The Yellow Brick Road of the Coder“](/posts/clean-code-developer-yellow-brick-road/) beschrieben. Außerdem wichtig sind:

**LeBlanc’s Gesetz : Later equals never**  
und  
**die Boy Scout Rule : Leave the campground cleaner than you found it**.

### Kapitel 2 Meaningful Names

Benennung in einem Projekt ist sehr wichtig, sei es um das Gesuchte zu finden oder um den Sinn einer Variablen oder einer Methode ohne langes Überlegen zu erkennen. Man sollte bei der Vergabe von Namen so gründlich vorgehen, wie man es für seinen Erstgeborenen tun würde. In der heutigen Zeit ist die Ungarische Notation absoluter Quatsch. Die IDE kennt den Typ, warum sollte man das in den Variablennamen integrieren?

### Kapitel 3 Funktionen

Die erste Regel von Funktionen lautet: Sie sollte klein sein.  
Die zweite Regel von Funktionen lautet: Sie sollte noch kleiner sein als das.  
Eine Funktion sollte nur eine Sache tun. Macht sie mehr als eine Sache, steigt die Komplexität. Und Komplexität ist schlecht.  
Eine gute Benennung der Funktionen ist, wenn der Name beschreibt, was die Funktion macht. Dabei darf der Name ruhig lang sein, wenn es der Lesbarkeit des Codes dienlich ist.  
Flagargumente sind verboten! Durch dieses Flag macht die Methode schon mehr als eine Sache und wir wären wieder bei der Sache mit der Komplexität. Böse.  
Die ideale Anzahl von Parametern einer Funktion ist 0! Aber da nicht immer alles ideal laufen kann, sind 1, 2 auch okay. Aber mehr als 3 ist verboten. Okay?  
Last but not least eine sehr wichtige Grundregel: Don’t Repeat Yourself!  
Denn: Durch Verdopplung des Codes steigt der Wartungsaufwand proportional.

### Kapitel 4 Kommentare

Kommentare sind schlecht, denn sie lügen! Ja, LÜGE! Code wird häufig verändert durch neue Anforderungen oder Refaktorisierungsmaßnahmen, der dazugehörige Kommentar aber meist nicht, wodurch schlechte bzw. in die Irre führende Kommentare entstehen. Es gilt also: Keine Kommentare sind besser als schlechte Kommentare. Man sollte die Zeit, die man für das Schreiben von Kommentaren aufbringen würde, lieber für die Refaktorierung der Methode verwenden. Denn Code sollte sich selbst erklären und ist außerdem die aktuellste Dokumentation. Nur schlechter Code muss kommentiert werden.  
**Auskommentieren des Codes ist verboten!** Andere Programmierer, die den auskommentierten Code sehen, werden diesen nicht löschen, da sie denken, dass es einen Grund haben muss, dass er dort steht und dass er zu wichtig ist, um gelöscht zu werden. Somit bleibt dieser “Kommentar” auf ewig dort und müllt unseren “Clean Code” zu. Heutzutage muss man nichts mehr auskommentieren. Durch Versionskontrolle geht nichts mehr verloren.

### Kapitel 5 Formatting

Eine perfekte Formatierung gibt es nicht, vielleicht für jeden Einzelnen, aber nicht für ein Team. Jeder hat seine Vorlieben. Letzendlich ist nur wichtig, dass sich das Team auf **EINE** Formatierung einigt. Jeder in diesem Team muss sich daran halten, auch wenn es für einen selbst nicht die optimale Lösung ist. Der Nutzen einer gemeinsamen „Sprache“ ist einfach zu groß, denn Kommunikation ist das A und O.

### Kapitel 6 Objects and Data Structures

Es wird grundsätzlich zwischen Objekten und Data Structures unterschieden.  
Objekte enthalten Businesslogik und sollten ihre interne Struktur nach außen hin verbergen, also keine Properties, welche die Member-Variablen des Objekts zurückgeben oder verändern lassen. Nur das Objekt selbst sollte seinen internen Status ändern können, wobei bei Objekten auf das Gesetz von Demeter zu achten ist:  
Es besagt, dass Objekte nur mit Objekten in ihrer unmittelbaren Umgebung kommunizieren sollen.  
Also:  
Methode m der Klasse k sollte nur Methoden nutzen von:

* k
* Ein Objekt, dass von m erstellt wurde
* Ein Übergabeparameter an m
* Ein Memberobjekt von k

Data Structures sind zum Beispiel Data Transfer Objects, kurz DTOs. Das sind Klassen ohne Methoden, also reine Datenträger. Eine spezielle Form von DTOs sind Active Records. Diese Objekte haben Methoden wie Save() und Find(), enthalten jedoch keine Businesslogik.

### Kapitel 7 Error Handling

Moderne Programmiersprachen haben ein Feature namens Exceptions. Das sollte man auch nutzen. Fehlercodes oder ähnliches sind veraltet. Eine gute Exception sollte allerdings so viel Information liefern, dass man auch ohne Debuggen den Fehler identifizieren kann, sonst kann man sich die ganze Mühe auch sparen.  
Außerdem noch 2 wichtige Grundregeln:  
**Don’t Return null** – somit wird es unnötig auf null zu prüfen  
und  
**Don’t Pass null** – null an eine Methode zu übergeben ist noch schlimmer als null zu returnen

### Kapitel 8 Boundaries

Man sollte unbedingt das Adapterpattern anwenden, wenn man 3rd party Code verwendet. 3rd party code sollte an so wenig stellen wie möglich verwendet werden, um Abhängigkeiten zu vermeiden.

### Kapitel 9 Unit Tests

Die 3 Gesetze von TDD:

1. Man darf keinen produktiven Code schreiben, solange man keinen fehlgeschlagenen Unit Test geschrieben hat.
2. Man darf nicht mehr als nötig schreiben, um einen Unit Test fehlschlagen zu lassen, und Fehler beim Kompilieren bedeutet einen fehlgeschlagenen Test.
3. Man darf nicht mehr produktiven Code als nötig schreiben, um einen fehlgeschlagenen Test zu reparieren.

Außerdem gilt: Tests sollten genauso “Clean Code” sein wie produktiver Code. Tests sollten genauso evolvierbar sein. Denn wenn sich der Code verändert, muss sich der Test auch verändern.  
Ein Test sollte nur ein Szenario abdecken – wieder das Thema Komplexität.

Clean Tests folgen noch 5 anderen Regeln:  
**F**ast  
**I**ndependent  
**R**epeatable  
**S**elf Validating  
**T**imely

Teil 2 gibt es [hier](/posts/cleancode2/)

<img src="/images/cleancode1/KickItImageGenerator.ashx" alt="kick it on dotnet-kicks.de"/>

## Kommentare (Archiv)

1. **Christina**

   [August 11, 2009 um 3:26 pm](/posts/cleancode1/)

   Super Zusammenfassung, ich möchte nur ein Paar kleine Ergänzungen machen:

   Kleine 3-er Regel zu DRY: einmal schreiben -> OK. Zweimal schreiben -> kann man noch akzeptieren. Dreimal schreiben-> refaktorieren! (Fowler-Refactoring)

   Was das KATEGORISCHE Abweisen von Kommentaren betrifft, kann ich wirklich nicht einverstanden sein. Ich kann mir Millionen von Fällen vorstellen, wo ein Name nicht aussagend genug sein kann. aber ich finde auch, dass Namen genau so wichtig sind wie DRY oder The Boy Scout Rule.

   Bin schon auf die Fortsetzung gespannt <img src="/images/cleancode1/icon_smile.gif" alt="" class="wp-smiley"/>
2. **[Peter Bucher](http://www.aspnetzone.de/blogs/peterbucher/)**

   [August 11, 2009 um 7:45 pm](/posts/cleancode1/)

   Salute Andreas

   Coole Zusammenfassung, gefällt mir gut <img src="/images/cleancode1/icon_smile.gif" alt="" class="wp-smiley"/> .  
   Ein paar Anmerkungen bzw. Ergänzungen:

   Das Buch “Clean Code” ist extra extrem und provokant geschrieben, es soll provozieren.  
   Man sollte nicht alles 1:1 übernehmen und als bare Münze hinnehmen, sondern nur das und soviel wie es Sinn macht.

   Mit den Kommentaren sind nicht die JavaDocs / XmlDocs von C# / VB.NET gemeint. API Dokumentation ist nach wie vor sehr wichtig und hilfreich und sollte benutzt und aktualisiert werden.  
   Stell dir nur mal ein .NET Framework ohne Intellisense-Kommentare vor <img src="/images/cleancode1/icon_smile.gif" alt="" class="wp-smiley"/> .

   Zu dont`t return null / don`t pass null muss ich sagen, das Clean Code auf Java fokusiert ist und das dort anders sein  
   kann. Man sollte null mit Bedacht und Strategie einsetzen, so eine pauschale Aussage kann ich aber für C# nicht gelten lassen.

   Denn zum Teil ist das bei .NET selber Konvention (ob das jetzt gut oder schlecht ist, lassen wir mal aussen vor),  
   oder sinnvoll gar nicht anders möglich.

   Eine interessante Diskussion dazu findet sich bspw. auf:  
   - <http://www.mycsharp.de/wbb2/thread.php?threadid=69181&hilight=null+funktion+php+peter>

   Grüsse aus der Schweiz, Peter
3. **[Rene Drescher-Hackel](http://weblog.drescher-hackel.de/)**

   [August 28, 2009 um 12:29 am](/posts/cleancode1/)

   Ich kann Peter hier nur zustimmen. Ergänzend sei noch gesagt – was keine wertende Aussage zum Blogbeitrag sein soll – dass die ganze Diskussion um Clean Code inzwischen aus meiner Sicht recht übertrieben wird. Um sauberen Code zu schreiben, muss ich weder ein Armband tragen, noch muss ich Pyramiden falten oder entsprechende T-Shirts tragen. Da fällt mir eine sehr praktische Redensart ein: “Es gibt nichts Gutes, außer man tut es”. Und so ist es auch mit der losgetretenen “Clean Code Debatte”.

   Was letztlich “sauberer Code” ist, wird doch von vielen Faktoren bestimmt, die im Wesentlichen aus einem Allgemeinverständnis herrührt und aber auch vom Entwicklerteam maßgeblich mit beeinflusst wird. Sicher, man sollte nicht unbedingt ein 500 Seiten umfassendes Referenzwerk zu Rate ziehen müssen, um den Code des Kollegen zu verstehen. Gelegentlich sieht man auch immer wieder noch den ungeliebten “Spagetthi-Code”, was keineswegs erstrebenswert ist.  
   Aber müssen wir denn jetzt alle um jeden Preis nach den Empfehlungen des Buches “Clean Code” von Robert C. Martin unseren Code umschreiben? Nein, ich denke, manchmal ist es viel vernünftiger seinem Stil treu zu bleiben. Dennoch kann man dabei funktionellen, sauberen, lesbaren Code schreiben.  
   Wenn ich lese, dies und das ist “böse” und “verboten”, dann hat das etwas von “Bibel”, wo ich mich dann frage, wer gibt hier wem das Recht, Dinge als “verboten” zu deklarieren.

   Also man sollte bei aller Clean-Code Diskussion immer das Ziel nicht aus den Augen verlieren und vor allem auf dem Teppich bleiben. <img src="/images/cleancode1/icon_wink.gif" alt="" class="wp-smiley"/>

   Grüße aus dem Frankenland.

   Rene
4. **[build broken » Clean Code Teil 2](/posts/cleancode2/)**

   [November 4, 2009 um 4:16 pm](/posts/cleancode1/)

   [...] habe das Buch “Clean Code” von Robert C. Martin a.k.a. Uncle Bob durchgelesen. Nach dem ersten Teil hier nun die versprochene Fortsetzung meiner [...]
5. **[Anonymous](http://www.delphipraxis.net/155561-mehrere-formulare-stringgridgroesse-anpassen-4.html#post1058834)**

   [Oktober 31, 2010 um 6:51 pm](/posts/cleancode1/)

   [...] [...]

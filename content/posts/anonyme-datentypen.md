---
title: "Anonyme Datentypen"
date: 2009-06-10
slug: anonyme-datentypen
original_url: "https://aztec-project.org/blog/anonyme-datentypen.html"
archive_url: "https://web.archive.org/web/20250601101329/https://aztec-project.org/blog/anonyme-datentypen.html"
author: "Andreas Seebauer"
categories: ["How-To"]
tags: ["C#", "HowTo"]
---

Anonyme Datentypen sind Klassen, die erst beim Kompilieren durch den Compiler definiert werden. Die Klassendefinition befindet sich also nicht im Quellcode. Die anonymen Datentypen leiten wie jedes andere Referenzobjekt von der Klasse object ab. Sie sind als reine Datenklassen gedacht und es können keine weiteren Methoden oder Events hinzugefügt werden. Obwohl der anonyme Datentyp auf Quellcodeebene noch nicht definiert ist, muss dank Visual Studio nicht auf die Intellisense verzichtet werden.

Definiert und intstanziert werden sie mit new und einem Objektinitialisierer:

```
    var mitarbeiter = new { Name = "Müller", Abteilung = "IT" };
```

var ist der implizite Typ und **nicht** der anonyme Datentyp. Er fungiert hier lediglich als container für die Instanz des anonymen Datentyps, die mit new {} erzeugt wird.

Gibt man keinen Namen für die Properties an, werden die Namen der Properties verwendet, mit denen initialisiert wird.

```
var  abteilung =  new  { Abteilungsname =  "IT"  };
var  mitarbeiter =  new  { Name =  "Müller" , abteilung.Abteilungsname };
Console .WriteLine(mitarbeiter.Abteilungsname);
```

Wenn man mit Werten initialisiert, muss ein Name angegeben werden.

Anonyme Datentypen bieten sich an, wenn man Abfragen mit Linq ausführt und entweder nur eine Teilmenge des ursprünglichen Objekts braucht, oder wenn man ein Objekt erweitern will, ohne extra eine neue Klasse zu definieren.

Hier ein Beispiel aus einem Castle Monorail Projekt, in dem eine erweiterte Liste an eine vm gegeben wird, ohne eine neue Klasse definieren zu müssen. Es soll dabei eine Liste erstellt werden, in der die Mitarbeiter mit ihrem Horoskop verknüpft werden :

```
public   void  Action() {
IList < Mitarbeiter > mitarbeiterListe = m_service.GetMitarbeiter();
var  mitarbeiterMitHoroskopListe = ( from  mitarbeiter  in  mitarbeiterListe
select   new  { Mitarbeiter = mitarbeiter,
Horoskop = GetHoroskop(mitarbeiter.Geburtsdatum) });
PropertyBag[ "mitarbeiterMitHoroskopListe" ] = mitarbeiterMitHoroskopListe;
}
```

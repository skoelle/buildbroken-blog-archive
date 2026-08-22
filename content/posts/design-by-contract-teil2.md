---
title: "Design by Contract – Teil 2"
date: 2009-11-05
slug: design-by-contract-teil2
original_url: "https://aztec-project.org/blog/design-by-contract-teil2.html"
archive_url: "https://web.archive.org/web/20250601101252/https://aztec-project.org/blog/design-by-contract-teil2.html"
author: "Christina Hirth"
categories: ["Architektur", "Clean Code Developing"]
tags: ["Architektur", "Clean Code", "Unit-Tests"]
---

Der vorherige DbC-Artikel ist ziemlich “abstrakt” ausgefallen, es haben einfach Beispiele gefehlt. Das möchte ich hiermit nachholen.

Erstens muss man die IDE anpassen: im März kommt .NET 4.0 raus und da wird Design by Contract mitgeliefert. Man kann das Konzept aber jetzt schon anwenden, wenn man die [Assembly](http://msdn.microsoft.com/en-us/devlabs/dd491992.aspx) zusätzlich installiert. Danach muss man die dll referenzieren und im Eigenschaftenfenster des Projektes im neuen Tab *Code Contracts* das Runtime Checking einstellen.

Jetzt zum Code: Nehmen wir eine ganz einfache Klasse `Bill` deren Objekte mit einem `IRepository` gespeichert bzw. geladen werden.

```
using  System.Diagnostics.Contracts;
namespace  ContractsPrototyp
{
public   class   Bill
{
public   int  Id {  get ;  set ; }
public   string  Number {  get ;  set ; }
public   double  Value {  get ;  set ; }
}
10
11
public   interface   IRepository
{
Bill  GetBill( string  number);
void  SaveBill( Bill  bill);
}
```

Die Kontrakte kann man in den einzelnen Methoden oder für eine ganze Klasse schreiben (unter dem Attribut `ContractInvariantMethode`) aber ich finde am schönsten, dass man die auch auslagern kann: durch eine gegenseitige Markierung können Kontrakt-Klassen und Interfaces als “Paare” definiert werden:

```
[ ContractClass ( typeof ( RepositoryContracts ))]
public   interface   IRepository
{
Bill  GetBill( string  number);
void  SaveBill( Bill  bill);
}
[ ContractClassFor ( typeof ( IRepository ))]
public   class   RepositoryContracts : IRepository
{
public   Bill  GetBill( string  number)
{
Contract .Requires(! string .IsNullOrEmpty(number));
return   null ;
}
25
public   void  SaveBill( Bill  bill)
{
Contract .Ensures(bill.Id > 0);
}
}
```

Eine Vorbedingung wird mit `Contract.Requires` und eine Nachbedingung mit `Contract.Ensures` definiert. Beide Methoden bekommen boolische Ausdrücke. Diese Ausdrücke müssen frei von Seiteneffekten sein.

Die eigentliche Implementierung der Klasse schaut dann so aus:

```
public   class   Repository : IRepository
{
public   Bill  GetBill( string  nummer)
{
//Würde das Objekt aus Datenhaltung laden
return   new   Bill ();
}
38
public   void  SaveBill( Bill  bill)
{
//Würde das Objekt speichern und ihm eine Id zuweisen
if  (BillIsValid( bill )) bill.Id++;
}
44
private   static   bool  BillIsValid( Bill  bill)
{
return  ! string .IsNullOrEmpty(bill.Nummer);
}
}
```

Woher können wir wissen, dass das funktioniert? Es ist einfach, wir schreiben ein Paar Tests dazu!  
Bei Kontraktverletzung wird eine Exception geworfen. Um diese – und dadurch die genaue Verletzung – überprüfen zu können braucht man etwas Workaround:

```
[ TestFixture ]
public   class   BillTests
{
private   IRepository  m_repository;
private   string  m_message;
60
[ SetUp ]
public   void  Setup()
{
m_repository =  new   Repository ();
m_message =  string .Empty;
Contract .ContractFailed += ( sender, e ) =>
{
e.SetUnwind();
m_message = e.Message;
};
}
```

Danach sind die Tests dann einfach:

```
[ Test ]
public   void  Laden_mit_leerer_Nummer_verletzt_Kontrakt()
{
76
try
{
m_repository.GetBill(  null  );
}
catch
{
//Nichts
}
85
Assert .That( m_message,  Is .EqualTo(  "Precondition failed: !string.IsNullOrEmpty(number)"  ) );
}
88
[ Test ]
public   void  Speichern_Rechnung_ohne_Nummer_verletzt_Kontrakt()
{
92
try
{
m_repository.SaveBill(  new   Bill {Value = 25} );
}
catch
{
//Nichts
}
101
Assert .That( m_message,  Is .EqualTo(  "Postcondition failed: bill.Id > 0"  ) );
}
```

Ich hoffe, das Beispiel ist ausführlich genug, um die Vorteile von DbC zu highlighten. [Stefan](http://www.lieser-online.de/blog/), vielen dank noch mal für den Artikel, ich habe mich natürlich von dir inspirieren lassen.


---
title: "StupidDB – object-persistence-framework"
date: 2009-07-13
slug: stupiddb1
original_url: "https://aztec-project.org/blog/stupiddb1.html"
archive_url: "https://web.archive.org/web/20250114121109/https://aztec-project.org/blog/stupiddb1.html"
author: "Stefan Kölle"
categories: ["Release", "StupidDB"]
tags: ["StupidDB"]
---

Angeregt durch die Diskussion auf dem Open-Spaces zum Thema schemalose Datenbanken, werden wir heute bereits die Vorabversion unserer StupidDB als open-source releasen.

Die StupidDB entstand bei uns aus der Notwendigkeit, immer wieder Objekte und Files schnell und einfach zu speichern, dies serverlos und trotzdem skalierbar und hochverfügbar vorzuhalten. Die StupidDB lässt sich am besten wie folgt beschreiben:

> StupidDB ist ein einfaches Objektspeicherungs-Framework auf dem Filesystem. Vergleichbar mit dem WebCache kann man in der StupidDB jegliches Objekt ablegen, welches kosteneffizient auf dem Filesystem gespeichert wird. Geladen werden können Objekte und Binärdaten mit einem eindeutigen Key und einer Partition. Den echten Speicherort auf der Festplatte ermittelt StupidDB selbst. Durch Replikation des Filesystems z.B. per Windows-DFS ist zudem eine einfache Hochverfügbarkeit und Skalierbarkeit der Datenbasis herzustellen.

Angeregt durch einen [Blogeintrag von tilllate.com](http://techblog.tilllate.com/2008/08/14/webtuesday-lightning-talk-slides/) letztes Jahr, entstand bereits vor einem Jahr die erste Version von StupidDB, welches bis zum Blogeintrag nur aus einem Konzept bestand. Leo Büttiker hat zwar ein leicht anderes Konzept als unsere Implementierung, in den Kernpunkten ähnelt sich aber das Design. StupidDB bekam durch diesen Blogpost damals jedoch seinen Namen.

Für folgende Anwendungsszenarien sehen wir StupidDB als geeignet:

* Userdaten wie Fotos und Mediadaten, die eine Datenbank nur unnötig aufblähen
* temporäre Daten
* Statusdaten
* Versionierung von Daten

Als Vorteile gegenüber z.B. MogileFS, CouchDB zählt für uns vor allem, dass kein zentraler Server für die Datenbank benötigt wird, sondern nur ein Share im Netz. Die Implementierung ist dadurch enorm vereinfacht. Mit weiteren Windows-Board-Mitteln kann man danach das ganze System um Hochverfügbarkeit und Skalierbarkeit einfach ausbauen.

Die Nutzung selbst ist denkbar einfach. Folgendes Mitarbeiter-Objekt möchte ich speichern.

```
public   class   Mitarbeiter
{
public   int  Id {  get ;  set ; }
public   string  Name {  get ;  set ; }
public   string  Vorname {  get ;  set ; }
public   string  Ort {  get ;  set ; }
public   string  Plz {  get ;  set ; }
72
public   string  VollerName
{
get  {  return   string .Format( “{0} {1}” , Vorname, Name); }
}
}
```

Dazu nutzt man die Put-Methode der StupidDB.

```
IStupidDB  stupidDB =  new   StupidDB ( “test” );
Mitarbeiter  mitarbeiter =  new   Mitarbeiter
{
Id = 1,
Name =  “Christian” ,
Vorname =  “Thomas” ,
Ort =  “Rosenheim” ,
Plz =  “83026”
};
stupidDB.Put(  “TestPartition” ,  “EinMitarbeiter” , mitarbeiter );
```

Um das gleiche Objekt wieder zu lesen, nutzt man mal eine Get Methode. Die Parameter sind Partition und Key:

```
Mitarbeiter  mitarbeiterAusgelesen =
( Mitarbeiter )stupidDB.GetObject(
“TestPartition” ,
“EinMitarbeiter” ,
typeof ( Mitarbeiter )
);
if  (mitarbeiterAusgelesen !=  null )
{
Console .WriteLine( “Name des Mitarbeiters: {0}” ,
mitarbeiterAusgelesen.VollerName);
}
```

Die StupidDB selbst wird über die app.config definiert.

```
< configuration >
< configSections >
< section   name = “ stupidDB “   type = “ Aztec.StupidDB.DBConfigCollection, Aztec.StupidDB, Version=1.0.0.0, Culture=neutral “   allowLocation = “ true “   allowDefinition = “ Everywhere “ />
</ configSections >
< stupidDB >
< DB   name = “ test “   root = “ temp\test “   tiefe = “ 3 “   versionierung = “ false “  />
</ stupidDB >
</ configuration >
```

Wer sich den aktuellen Code einmal ansehen möchte, kann dies gerne unter folgendem Link ansehen:<https://stupiddb.svn.sourceforge.net/svnroot/stupiddb/trunk>

## Kommentare (Archiv)

1. **Doku**

   [March 1, 2010 at 9:59 am](/posts/stupiddb1/)

   Coole Sache, gibt es dazu eine Doku der Funktionen wie .Backup  
   und der möglichen werte, wie Tiefe, Versionierung etc?

   Vielen Dank.
2. **[Stefan Kölle](http://www.stefankoelle.de/)**

   [March 1, 2010 at 12:21 pm](/posts/stupiddb1/)

   Es gibt aktuell noch keine Doku, im Code wird einiges erklaert jedoch sicher nicht ausreichend.

   In der aktuellen Ausgabe der dotnetpro gibt es jedoch einen Artikel zu StupidDB, dort erklaere ich die Parameter noch einmal genauer. Auch das Thema Tiefe, Versionierung usw. <http://www.dotnetpro.de/CurrentIssue.aspx>
3. **UweD**

   [March 9, 2010 at 5:47 pm](/posts/stupiddb1/)

   Scheint ja wirklich toll zu sein. Leider findet man im Web noch nicht allzuviel darüber. Der Artikel in der dotnetpro sagt einiges, aber zu dem Pfad kann ich nirgends etwas finden.  
   Wenn ich root=“temp\test“ angebe, wo liegt das dann physisch?
4. **[Stefan Kölle](http://www.stefankoelle.de/)**

   [March 9, 2010 at 5:52 pm](/posts/stupiddb1/)

   Hallo, Uwe,

   man kann bei root einfach einen absoluten Pfad angeben, z.B. c:\temp\stupiddb\

   Ohne der Angabe eines Pfades wird die StupidDB im Ausfuehrungsverzeichnis angelegt.

   Gruss  
   Stefan
5. **Uwe**

   [January 4, 2011 at 11:17 am](/posts/stupiddb1/)

   Hallo,  
   ich bin nun nicht so firm in C#. Gibt es Beispiel für IStupidDB.Dir ?

   Danke  
   Uwe
6. **[Andreas Seebauer](http://www.in-your-face.org/)**

   [January 12, 2011 at 12:05 pm](/posts/stupiddb1/)

   Hallo, Uwe,

   hier ein kleines Beispiel für die Verwendung von IStupidDB.Dir in C#:

   IStupidDB sdb = new StupidDB(“meinDbName”);  
   string partition = “Beispielpartition”;  
   string key = “Beispielkey”;  
   // Speichern des strings “Beispiel” unter Key “Beispielkey” in Partition “Beispielpartition”  
   sdb.Put(partition, key, “Beispiel”);  
   // Auflisten aller Keys in Partition “Beispielpartition”  
   List listKeys = sdb.Dir(partition);

   Mit den zurückgelieferten Keys können dann die Objekte via GetObject ausgelesen werden.  
   Ich hoffe das beantwortet deine Frage.

   Gruß  
   Andreas
7. **Uwe**

   [January 12, 2011 at 4:23 pm](/posts/stupiddb1/)

   Hallo Andreas,  
   nein, nicht ganz!  
   Laut Doc gibt es  
   Dir – Listet alle Schlüssel einer Partition) und  
   Dir – Liefert ein IDictionary aller Schlüssel mit zugehörigem Objekt .

   Mit geht es um das 2. Dir.

   Uwe

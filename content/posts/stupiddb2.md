---
title: "NoSQL mit StupidDB"
date: 2010-02-22
slug: stupiddb2
original_url: "https://aztec-project.org/blog/stupiddb2.html"
archive_url: "https://web.archive.org/web/20250114131202/https://aztec-project.org/blog/stupiddb2.html"
author: "Stefan Kölle"
categories: ["StupidDB"]
tags: ["Datenbank", "NoSQL", "Schemalos"]
---

Seit ein paar Monaten wird der Begriff [NoSQL (Not only SQL)](https://www.computerworld.com/s/article/9135086/No_to_SQL_Anti_database_movement_gains_steam) immer häufiger verwendet. Wir sind mit unserer schemalosen Datenbank [StupidDB](https://sourceforge.net/projects/stupiddb/) vor eineinhalb Jahren bereits auf diesen Zug aufgesprungen und jetzt hat sie einen Überbegriff bekommen: auch StupidDB ist NoSQL!

Auf dem [BarCamp in Nürnberg](http://www.bcnue2.de/) war NoSQL auch ein Thema und [Jonathan Weiss](https://twitter.com/jweiss) hat in seiner Session gut dargestellt, dass relationale Datenbanken nicht immer die Lösung für alle Probleme sind. NoSQL Datenbanken speichern meist dokumentenorientiert und sind dadurch nicht an ein festes Schema gebunden. Relationale Datenbanken haben ein fixes Schema und erlauben dynamische Abfragen der Daten, bei NoSQL ist dies umgekehrt. Weitere Informationen zu [NoSQL bei Wikipedia](https://en.wikipedia.org/wiki/NoSQL).

Im [März Heft der dotnetpro](https://web.archive.org/web/20160119224824/http://www.dotnetpro.de/articles/onlinearticle3220.aspx) stelle ich ausführlich den Einsatz von StupidDB vor. Das Heft ist am 18.2.2010 erschienen und sollte jetzt in jedem gut sortierten Kiosk erhältlich sein.

Für alle, die sich Heft nicht griffbereit haben, ich habe bereits Mitte letzten Jahres in einem Blogpost den [Einsatz von StupidDB](/posts/stupiddb1/) beschrieben. Hier sieht man zumindest die Grundzüge der StupidDB. Das aktuelle dotnetpro Heft lohnt sich jedoch trotzdem, da hier noch weitere Artikel zum Thema NoSQL zu finden sind. Unter anderem das [Lounge Repository](https://loungerepo.codeplex.com/) von [Ralf Westphal](http://www.ralfw.de/default.html) und auch CouchDB.

Als neuester Vertreter in der NoSQL Bewegung gilt MongoDB. Eine Opensource Implementierung die nun auch Sourceforge einsetzt. Auch dafür gibt es schon [Blogposts](http://odetocode.com/Blogs/scott/archive/2009/10/13/experimenting-with-mongodb-from-c.aspx) und Tests mit .NET.

Zudem hat [Ayende Rahien](http://ayende.com/Blog/Default.aspx) im Herbst letzten Jahres auch seine [Rhino Divan DB](http://odetocode.com/Blogs/scott/archive/2009/10/13/experimenting-with-mongodb-from-c.aspx) vorgestellt. Interessant klingt auch [Object Lounge](http://blog.technewlogic.de/StaticContent/Pages/ObjectLounge_Main.aspx).

Es scheint also ein Bedarf an alternativer Datenpersistenz zu bestehen, wird sich zeigen wohin dieses Jahr die Reise bei NoSQL geht.

Wer sich den aktuellen Code einmal ansehen möchte, kann dies gerne unter folgendem Link ansehen:  
<https://stupiddb.svn.sourceforge.net/svnroot/stupiddb/trunk>

Verwendet ihr schon NoSQL?

## Kommentare (Archiv)

1. **Nils**

   [February 27, 2010 at 3:59 pm](/posts/stupiddb2/)

   Und wo kann man sich diese schamlose – ah, schemalose Datenbank nun runterladen?
2. **[Stefan Kölle](http://www.stefankoelle.de/)**

   [February 27, 2010 at 6:33 pm](/posts/stupiddb2/)

   Hallo Nils,

   ich habe in der Tat vergessen in diesem Blogpost die URL noch einmal zu posten.

   Habe ich nun nachgeholt.

   Der aktuelle Sourcecode ist hier zu finden:  
   <https://stupiddb.svn.sourceforge.net/svnroot/stupiddb/trunk>

   Bin gespannt was du dazu sagst…

   Gruesse  
   Stefan
3. **ronald**

   [March 26, 2010 at 10:37 am](/posts/stupiddb2/)

   Hallo,  
   ich wollte die stupiddb austesten, leider kann ich die dll nicht zum download finden. bei der url, welche im dotnet-pro artikel beschrieben, finde ich keine files zum download. (–> oder ist das so gewollt)?  
   vielleicht kann mir jemand helfen 🙂

   dank ronald
4. **[Stefan Kölle](http://www.stefankoelle.de/)**

   [March 26, 2010 at 2:15 pm](/posts/stupiddb2/)

   Hallo Ronald,

   StupidDB gibt es im Moment nur direkt im SourceCode, die aktuelle Version kann man direkt per SVN downloaden:  
   <https://stupiddb.svn.sourceforge.net/svnroot/stupiddb/trunk>

   Vielleicht sollten wir demnaechst auch die binaere Version davon bereitstellen.

   Gruss  
   Stefan
5. **ronald**

   [March 26, 2010 at 2:53 pm](/posts/stupiddb2/)

   ich habe leider kein svn. ich habe probiert die files einzeln runterzuladen, aber dann kommen viele Fehler. Finde deinen Vorschlag gar nicht schlecht oder code als ZIP für alle NICHT-svn Benutzer. Wäre super. Vielen Dank vorab, Ronald
6. **[Stefan Kölle](http://www.stefankoelle.de/)**

   [March 26, 2010 at 3:36 pm](/posts/stupiddb2/)

   Werde mich am Wochenende um die Gezippte Version kuemmern…
7. **[Stefan Kölle](http://www.stefankoelle.de/)**

   [March 27, 2010 at 8:04 pm](/posts/stupiddb2/)

   Hallo Ronald,

   die DLL und der Sourcecode kann nun als ZIP direkt runtergeladen werden:

   [/](/)

   Gruss  
   Stefan
8. **ronald**

   [March 29, 2010 at 9:09 am](/posts/stupiddb2/)

   danke für die bereitstellung. habe es ausprobiert – sehr schönes teil 🙂 hatte keine probleme bei der erstellung einer demo (unter hilfe von eurem blog)

   ich habe etwas ähnliches gebaut, um einstellungsdaten für anwendung zu speichern (z.B. com-port, parameter für prüfprogramme usw.) – letztlich funktioniert meine app ähnlich wie eure –> Key – Value, generisch. den speicherort habe ich mit “providern” gelöst, somit kann der anwender entscheiden, ob die files auf der festplatte landen oder vielleicht doch in einer sql-db oder was ganz anderes.  
   vielleicht für euch hilfreich um eine GUI bereitzustellen:  
   die gui habe ich mit propertygrid gelöst. um dort dann z.B. Listeneinträge zu ergänzen, muss dann eine spez. liste erstellt werden, welche ICustomTypeDescriptor impl., ein eigener PropertyDescriptor (generisch) muss auch erstellt werden.  
   das brauchte ich, weil betreuer von einem automaten, ohne xml-kenntnisse die daten pflegen müssen.

   grüße ronald

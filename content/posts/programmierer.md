---
title: "(Spreu + Weizen).Select(Programmierer)"
date: 2010-03-14
slug: programmierer
original_url: "https://aztec-project.org/blog/programmierer.html"
archive_url: "https://web.archive.org/web/20250114120714/https://aztec-project.org/blog/programmierer.html"
author: "Christina Hirth"
categories: ["Clean Code Developing"]
tags: ["Clean Code"]
---

Obwohl wir [Jeff Atwood](http://www.codinghorror.com/blog/) schon vor Monaten von unseren Bloggerliste gestrichen haben, ich habe ihn noch nicht aus meinem Googlereader entfernt. Er ist ein Typ, der liebt viel Wirbel zu verursachen ([Scott Hanselmann](http://www.hanselman.com/blog/) nennt ihn aus den Wörtern *friend* und *enemy* “my friendemy” <img src="/images/programmierer/icon_wink.gif" alt=";)" class="wp-smiley"/> ) aber manchmal trifft er den Nagel auf den Kopf. So auch in seinem letzten Artikel [“The Non-Programming Programmer”](http://www.codinghorror.com/blog/2010/02/the-nonprogramming-programmer.html).

> …  
> I wrote that article in 2007, and I am stunned, but not entirely surprised, to hear that three years later “the vast majority” of so-called programmers who apply for a programming job interview are unable to write the smallest of programs. To be clear, hard is a relative term — we’re not talking about complicated, Google-style graduate computer science interview problems. This is extremely simple stuff we’re asking candidates to do. And they can’t. **It’s the equivalent of attempting to hire a truck driver and finding out that 90 percent of the job applicants can’t find the gas pedal or the gear shift.**

Aus den Unmengen von Kommentaren zu urteilen, ist das ein Problem, mit dem sehr viele zu kämpfen haben. Sein Artikel beschäftigt sich mit der Arbeit von Personen, die Einstellungsgespräche führen, und er versucht ein paar Tipps zu geben, wie man dieses Verfahren führen soll.

Ich musste allerdings beim Lesen ständig auf die Situation “danach” denken, wenn diese NPPs (sprich Non- Programming Programmers) bereits aus irgendeinem Grund eingestellt wurden. Aus Erfahrung weiß ich genau, was mir viel über jemanden verraten würde: weiß er/sie etwas über Clean Code, kennt er die Folgen vom Creepy Code und wie ist die persönliche Einstellung dazu? Also zusammengefasst: geht es um einen **professionellen Softwareentwickler**? Dafür würden auch ein Code-Review oder ein paar Fragen reichen.

Was haltet ihr von Coding bei der Einstellung? Ist das auch in Europa üblich? Würde das die unpassenden Personen ausfiltern? Oder soll man sich die Zeit nehmen und dem Kandidaten “ungesehen” die Probezeit anbieten? Würde das vielleicht zu viele Personen ausfiltern? Kann man sich das überhaupt erlauben in der heutigen Zeit der Fachkräftemangel? (Gut, man fragt sich natürlich, ob wir hier über “Fachkraft” sprechen dürfen…)

<img src="/images/programmierer/KickItImageGenerator.ashx" alt="kick it on dotnet-kicks.de"/>

## Kommentare (Archiv)

1. <img src="/images/programmierer/3e7b6cb163ea9cc8549abcb8b5a03e2e.jpeg" width="32" height="32" class="avatar avatar-32 photo"/> **[Ralf Westphal](http://ralfw.blogspot.com/)**

   [März 14, 2010 um 1:09 pm](/posts/programmierer/)

   Einen echten NPP hab ich bei Einstellungsgesprächen noch nicht getroffen. Aber Bewerber, die nahe dran waren.

   Ob Programmieraufgaben in Europa/Deutschland üblich sind oder nicht, ist mir aber egal. Sie sind in jedem Fall notwendig. Eine Personalabteilung kann aufgrund von Bewerbungsunterlagen keine (!) Beurteilung abgeben, ob jmd grundsätzlich ein kompetenter Softwareentwickler ist. (Von Feinheiten, wie Bekanntheit mit der Problemdomäne oder Softskills sehe ich hier mal ab. Das ist noch ein ganz anderer Schnack.)

   Schon eine gaaaanz simple Programmieraufgabe hilft bei der grundsätzlichen Einordnung eines Bewerbers. Darauf sollte man nie verzichten. Die dauert dann vielleicht 2-3 Minuten. Erste Korrelationen zwischen solch einer Aufgabe und der “Auffassungsgabe” von Entwicklern habe ich schon in kleinen Erhebungen gesammelt. Damit ist dann natürlich noch kein abschließendes Urteil zu fällen – aber eine Tendenz lässt sich ablesen.

   Weiter untermauern kann man dann mit Entwurfsaufgaben und längeren Programmieraufgaben. Eine Kata hilft da immer. Die kann man auch immer als Anlass nehmen, über den allgemeinen Entwicklungsprozess zu sprechen.

   -Ralf
2. **[Alex](http://blog.alexonasp.net/)**

   [März 14, 2010 um 3:56 pm](/posts/programmierer/)

   Hallo Christina, ich überlege gerade, was schlimmer ist: ein Programmierer, der das Geschäft irgendwann von der Pieke auf gelernt – jetzt aber meint, dass das fürs ganze Programmiererlebe reicht oder ein Quereinsteiger, dem Basics fehlen – dafür aber gewillt ist, sich permanent zu verbessern… Wie so oft, hängt es vermutlich davon ab, was man erreichen will / muss, wenn man die betreffende Person einstellt.

   Code-Reviews sind hier bestimmt kein schlechter Ansatz, aber sie sollten vielleicht nicht das einzige Einstellungskriterium sein. Auf jeden Fall sollte der Code aber gemeinsam reviewed werden, denn vielleicht hat ja auch der Reviewer eine verkehrte Sicht <img src="/images/programmierer/icon_wink.gif" alt=";-)" class="wp-smiley"/>

   Ich habe in den letzten Jahren in anderen Bereichen (Maschinen-/Anlagenbau) festgestellt, dass man den perfekten Mitarbeiter nicht bekommt. Viel wichtiger ist es imho, die Stärken und Schwächen des einzelnen zu kennen (das ist ein mühsamer Prozess) und daraus ein schlagkräftiges Team zu formen.
3. **Christina Hirth**

   [März 14, 2010 um 5:02 pm](/posts/programmierer/)

   Hallo Ralf,

   Diese heiklen Themen wie Softskills und Domänenkenntnisse habe ich absichtlich erst gar nicht angesprochen, das wäre “zu schön um wahr zu sein”.

   Ich betrachte diese Bereiche wie gut geschriebenen Code: `Refaktorisierung` ist danach noch immer möglich, wenn die Basis stimmt. Das ist also, was vorhanden sein muss: eine gute Basis – worüber, wie du schreibst, bereits eine Miniaufgabe etwas verrät – und die Bereitschaft zu **lernen**. In einem der Kommentare zum o.g. Artikel gibt es einen Link zu einer persönlichen Definition, was einen [Senior Developer](http://thelimberlambda.com/2010/02/09/what-is-a-senior-developer/) ausmacht. Da steht diese Wissbegierde auf der 3. Stelle! Klar, nicht jede ist ein Senior Developer, aber der Lerndrang entsteht auch nicht erst nach zig Jahren.

   Ich finde deine Idee mit dem Dojo – in der Probezeit, nehme ich an – sehr gut, die Teilnahme oder Nicht-Teilnahme an so eine kleine Herausforderung kann sehr vieles aussagen.

   Du bist in der Position, in der dir die deutschen Gepflogenheiten bei der Zusammenstellung eines Team egal sein kann, ich dagegen sitze an der anderen Seite des Tisches <img src="/images/programmierer/icon_wink.gif" alt=";)" class="wp-smiley"/> Ich wünschte mir, dass mehr Leute so denken würden wie du. Vielleicht könnte das auch zu einer Aufgabe der CCD-Bewegung werden.

   Christina
4. **Christina Hirth**

   [März 14, 2010 um 5:11 pm](/posts/programmierer/)

   Hallo Alex,

   Ich bin genau deiner Meinung, es hängt fast alles davon ab, wozu die Position ausgeschrieben wurde. Die Frage ist allerdings, ob da noch Platz für Nachbesserung vorhanden ist, wo eventuell kein Wille ist. Dann bin ich mehr für den Quereinsteiger – ich bin auch einer – wenn der Grund für die Neuorientierung eine falsche erste Wahl war und nicht “ich habe mir mal eine Homepage gebastelt, also bin ich Programmierer”  
   Was den perfekten Mitarbeiter betrifft: hoffentlich gibt es ihn noch nicht, das würde das Leben der anderen im Team für immer vermiesen <img src="/images/programmierer/icon_wink.gif" alt=";)" class="wp-smiley"/>
5. **[Golo Roden](http://www.des-eisbaeren-blog.de/)**

   [März 14, 2010 um 7:28 pm](/posts/programmierer/)

   Hallo Christina,

   mich persönlich hat es schon immer gewundert, dass ich selbst in noch keinem Bewerbungsgespräch dazu aufgefordert wurde, Code zu schreiben – fände es aber prinzipiell positiv. Nicht nur, weil man sieht, wie der jenige codiert, sondern auch – und das finde ich viel wichtiger – weil man sieht, wie er an Probleme herangeht, wie er versucht, eine Lösung zu finden, …

   Viele Grüße,

   Golo
6. **Christina Hirth**

   [März 14, 2010 um 7:54 pm](/posts/programmierer/)

   Hallo Golo,

   anscheinend ist das hierzulande wirklich nicht üblich und das ist wirklich schwer zu verstehen. Es ist zwar kein Überschuss vom Jobs am Markt, aber ein guter Programmierer hat wahrscheinlich doch eine Auswahlmöglichkeit. Und was würde mehr über die Aussichten bei einer Firma erraten, als wenn diese vom Anfang an ein bestimmtes Niveau erwartet. Das würde beiden Seiten was zusichern, oder?

   Schöne Grüße,  
   Christina
7. **[Ilker Cetinkaya](http://www.gmbsg.com/)**

   [März 14, 2010 um 10:11 pm](/posts/programmierer/)

   Komisch, das hier so wenige Code bei Einstellungsgesprächen geschrieben haben. Ich habe in allen meinen letzten drei Anstellungen Code geschrieben, bevor ich eingestellt wurde. Das waren ganz unterschiedliche Dinge. Mal war es eine “Hausaufgabe”, die man innerhalb von ein paar Tagen erledigen konnte (z.B. Währungsumrechner mit Online-Währungskursen), mal war es eine 5-15 Minuten Aufgabe beim Bewerbungsgespräch (z.B. Lotto-Simulation).

   Als Lead-Developer habe ich auch schon einige Einstellungsgespräche begleitet. In allen Gesprächen mussten die Bewerber Code schreiben – mal auf Papier, mal direkt in VS. Ich möchte nicht zu tief in die Spezifika eines Einstellungsgespräches und die Möglichkeiten des Abklopfens technischer Fertigkeiten von Bewerbern eingehen. Fakt ist jedoch: Ich selbst stelle mich gerne einer Code-Aufgabe und ebenso finde ich es gut, wenn man eine Aufgabe dem Bewerber stellt. Fest steht aber auch: eine Coding-Aufgabe alleine reicht natürlich nicht. Schön finde ich es, wenn der Aufgabensteller aktiv mit dem Bewerber den Code durchgeht und bespricht. Leider hat/bekommt man meistens nicht die Zeit für ein so ausführliches Kennenlernen via Code – schade eigentlich.

   Fazit: Coding bei Bewerbung ist normal – und gut. Für beide.

   Bestens,  
   Ilker
8. **[André Krämer](http://blog.codemurai.de/)**

   [März 15, 2010 um 12:21 pm](/posts/programmierer/)

   Bei meinem vorherigen Arbeitgeber habe ich einige Einstellungsgespräche begleitet. Dort legte ich großen Wert darauf, dass Code geschrieben wurde. Meist ganz einfache Sachen, die man ans Whiteboard schreiben konnte. Dem Bewerber wurde nahegelegt, “laut” zu denken während er seinen Code anschreibt. Dabei habe ich wert darauf gelegt, dass der Bewerber die Aufgabe mit den gegebenen Informationen nicht eindeutig lösen konnte. Neben den reinen Codierfähigkeiten konnte ich so nämlich ein Gefühl dafür bekommen, ob derjeniege bei unklaren Anforderungen (die richtigen) Fragen stellt, oder einfach irgendwas drauf los programmiert.

   Gruß,  
   André
9. **Christina Hirth**

   [März 15, 2010 um 12:40 pm](/posts/programmierer/)

   Hallo André,

   endlich jemand aus der anderen Mannschaft <img src="/images/programmierer/icon_smile.gif" alt=":)" class="wp-smiley"/>

   Deine Vorgehensweise finde ich sehr effizient, aber hätte es nicht passieren können, dass der Bewerbungsstress dein Bild über den Kandidaten verzehren könnte? Oder wusste er schon vor vornherein, dass die Aufgabe unvollständig ist?

   Apropos, es fällt mir gerade eine neue Frage ein: wissen überhaupt die Kandidaten darüber, was für ein es Gespräch sie erwartet? Oder ist es eine Überraschung?

   Schöne Grüße,  
   Christina
10. **[André Krämer](http://blog.codemurai.de/)**

    [März 15, 2010 um 1:54 pm](/posts/programmierer/)

    Dass der “Bewerbungsstreß” meine Wahrnehmung verzerrt haben könnte, kann ich nicht aussließen. Da die Aufgaben allerdings meist recht einfach waren und ich auf eine angenehme Gesprächsatmosphäre geachtet habe, hoffe bzw. glaube ich nicht, dass jemand so viel Streß hatte, dass es zu einer vollkommen falschen Wahrnehmung hätte führen können. Außerdem sollte man auch bedenkend, dass es bei der späteren Ausübung des Jobs immer wieder Situationen geben kann, in denen man unter Streß / Druck arbeiten muss. Daher simulierte die Situation vielleicht sogar ein wenig eine realistische Arbeitssituation <img src="/images/programmierer/icon_wink.gif" alt=";-)" class="wp-smiley"/>

    Zur Frage ob die Kandidaten vorher wussten, was sie erwartet: Wenn sie gefragt haben dann schon <img src="/images/programmierer/icon_wink.gif" alt=";-)" class="wp-smiley"/>  
    Auf Nachfrage habe ich immer sehr ausführlich beschrieben wie wir vorgehen werden. Wer nicht gefragt hat, der hat halt Pech gehabt. Ich denke auch, dass es schon eine Menge über den Bewerber aussagt, ob er sich nach Erhalt einer Einladung telefonisch meldet um ein paar Fragen vorab zu klären, oder nicht.
11. **[KW12: Seitwert, Giana Sisters, Dumm 3.0, UML und mehr - Der Softwareentwickler Blog](http://www.der-softwareentwickler-blog.de/2010/03/26/kw12-giana-sisters-dumm-3-0-uml-visual-studio-2010-und-mehr/)**

    [März 26, 2010 um 9:27 am](/posts/programmierer/)

    [...] [...]
12. **[Nils Hitze](http://silberkind.de/evangelist)**

    [April 9, 2010 um 1:40 pm](/posts/programmierer/)

    Ich habe mich im Dezember/Januar auf 15 versch. Stellen beworben (als WebEntwickler) und musste nur bei EINER  
    auf dem Papier programmieren, ein anderer wollte wenigstens vorher Codebeispiele sehen bzw. ein minimales  
    MVC Projekt (ZendFramework)

    Bei 50% hätte ich mich einfach durchmogeln können mit einer gehörigen Portion Buzzword Bingo.

    Auch aus Bewerbersicht macht es total Sinn Coding zu verlangen, einfach um zu sehen womit man es eigentlich  
    zu tun hat. Bsp. Ein Arbeitgeber hat mich gefragt: Code ok, DB steht, Error Logging an, Seite weiß, was tun?  
    Ich hab rumgerätselt was er will, bis ich in den blauen Dunst ein “echo ‘fail’;exit;” als Breakpoint geworfen habe.  
    Der wollte wirklich QuickNDirty. An anderer Stelle, selbe Situation war ein Debugger bzw. der ErrorLogOutput gefragt,  
    also die vernünftigere Lösung.

    Klar, die Chemie muss stimmen, aber ich bin prinzipiell der Meinung von Joel:  
    <http://www.joelonsoftware.com/articles/GuerrillaInterviewing3.html>

    Nur mal so von meiner Seite als Bewerber aus.
13. **Christina Hirth**

    [April 12, 2010 um 9:36 pm](/posts/programmierer/)

    Hi Nils,

    danke für deinen Kommentar und den Link zum Artikel. Das ist wirklich typisch Joel, der fackelt ja nicht viel rum !

    Aber jetzt mal ernst, ich finde, dass er die Grundideen genau erfasst hat: ein guter Entwickler muss “Smart” UND fähig sein “to get things done”. Genau so ist es. Er sagt ja, es ist nicht genug etwas hinzukriegen, wenn man danach andere Entwickler braucht, um die verursachten Schaden zu bereinigen. Und ob man das durch Code, Code-Review oder eine theoretische Diskussion erfährt, ist ja dem jeweiligen Interviewer überlassen.

    Was deine Erfahrungen betrifft: vielleicht waren deine 14 Gesprächspartner so erpicht darauf, dich einzustellen, dass sie dich gar nicht prüfen wollten, sondern dir nur den Job verkaufen? Ich glaube, dass das heutzutage sehr oft der Fall sein kann, dass man einfach nur hofft, dass der Bewerber schon “reinwachsen” wird. Das kann natürlich passieren, aber nur, wenn man die Wahl sorgfältig genug trifft.

    Nur so aus Neugier: was hast du von der quick-and-dirty-Stelle gehalten?
14. **[Nils Hitze](http://silberkind.de/evangelist)**

    [April 13, 2010 um 11:21 am](/posts/programmierer/)

    Stimme dir und Joel da zu.

    Wegen QuickNDirty, ich mag Q&D eigentlich schon ganz gerne. Das ist so eine Hemdsärmelige Angelegenheit wie beim KFZSchrauben. Knöcheltief im SourceCode sozusagen. Aber man muss erstmal sauber&gut können um dann Q&D Code zu prodzuieren der einem nicht gleich um die Ohren fliegt. Habe generell das Gefühl, viele Coder verzetteln sich und übertreiben es mit der Strukturierung. Da wird dann für Projekte monatelang am CodeStyle und sonstigem gefeilt die man in der Hälfte der Zeit sauber hätte runterschreiben könne. Oder Skalierung eingeplant für Sachen die keine Skalierung benötigen werden.

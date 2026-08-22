---
title: "Design by Contract – jetzt auch mit C#"
date: 2009-10-26
slug: design-by-contract
original_url: "https://aztec-project.org/blog/design-by-contract.html"
archive_url: "https://web.archive.org/web/20250114140450/https://aztec-project.org/blog/design-by-contract.html"
author: "Christina Hirth"
categories: ["Architektur", "Clean Code Developing"]
tags: [".NET", "Architektur", "Clean Code"]
---

Bald kommt .NET 4.0 raus, zusammen mit einem für C# neuen Konzept: Kontrakte im Code mit **Spec#** festzulegen.

Wikipedia definiert DbC folgendermaßen:

> Design by contract (kurz DbC; englisch Entwurf gemäß Vertrag) oder Programming by Contract ist ein Konzept aus dem Bereich der Softwareentwicklung. Ziel ist das reibungslose Zusammenspiel einzelner Programmmodule durch die Definition formaler „Verträge“ zur Verwendung von Schnittstellen, die über deren statische Definition hinausgehen. Entwickelt und eingeführt wurde es von Bertrand Meyer mit der Entwicklung der Programmiersprache Eiffel.

[Stefan Lieser](http://www.lieser-online.de/blog/) hat über das neue Konzept einen sehr guten Artikel in [www.visualstudio1.de](http://www.visualstudio1.de/) geschrieben, mit Begriffsklärung und Anwendungsbeispiele. Kurz zusammengefasst ist die Rede von Folgendem: anstelle, dass man in jeder Methode auf not-null or not-empty usw. prüft, schreibt man die Erwartungen als Code hin. Diese werden von Tools wie z.B. Resharper erkannt und bei fehlerhaften Aufruf der Methode, wird der Entwickler gewarnt. Am besten finde ich, dass man den Kontrakt-Code z.B. für einen Interface in eine separate Klasse schreiben kann und diese wird durch Attribute (`ContractClassFor`) gefunden. Also wird dadurch der eigentliche Code nicht größer.

Das soll nicht bedeuten, dass der Entwickler der Methode die Verantwortung von sich schiebt <img src="/images/design-by-contract/icon_wink.gif" alt="" class="wp-smiley"/> , sondern dass er Bedingungen der “Nutzung” offenlegt, Informationen, die bisher nur durch das Anschauen des Codes oder durch mündliche/schriftliche Mitteilung möglich war. Mit **Spec#** kann man die **Intention-Revealing Interfaces** ganz genau schreiben: mit veröffentlichten und kompilierten Bedingungen.

## Kommentare (Archiv)

1. **[Rainer Hilmer](http://dotnet-forum.de/blogs/rainerhilmer/default.aspx)**

   [Oktober 26, 2009 um 11:33 am](/posts/design-by-contract/)

   CodeContracts kommen nicht erst mit .NET Framework 4. Es gibt sie schon eine ganze Weile bei DevLabs. Dieses ist mittlerweile in .NET 4 eingeflossen.  
   <http://msdn.microsoft.com/en-us/devlabs/dd491992.aspx>  
   Wer mit der Einflechtung von CodeContracts nicht bis VS2010 warten möchte, kann es sich dort ziehen.

   Ich habe dazu auch eine Quick Reference geschrieben.  
   <http://dotnet-forum.de/blogs/rainerhilmer/archive/2009/10/15/code-contracts-quick-reference.aspx>
2. **Christina Hirth**

   [Oktober 26, 2009 um 1:55 pm](/posts/design-by-contract/)

   Hallo Rainer,

   danke für den Hinweis, das ist mir schon bekannt. Steht auch in den o.g. Artikel, den ich hier nicht abschreiben wollte, er ist ja nicht von mir <img src="/images/design-by-contract/icon_smile.gif" alt="" class="wp-smiley"/> . Außerdem würde ich ja nie über Code schreiben, den ich selbst nicht ausprobiert habe, also ist es klar, dass es jetzt schon geht.  
   Der andere Grund, warum ich das nicht speziell erwähnt habe, ist, dass es z.Z. zwar möglich ist, das Konzept anzuwenden, aber die Unterstützung seitens VS fehlt, es sei denn, du nutzt TSF.

   Mir ging es eigentlich darum, dass es endlich möglich ist, Anforderungen als Code zu implementieren und als solche schriftlich festhalten, verfolgen und auswerten.
3. **[Rainer Hilmer](http://dotnet-forum.de/blogs/rainerhilmer/default.aspx)**

   [Oktober 26, 2009 um 3:29 pm](/posts/design-by-contract/)

   Hallo Christina,  
   ich habe eine gute Nachricht: Es gibt eine kostenfreie academic license, die den static Checker auch auf VS 2008 pro zur Verfügung stellt (mit der aktuellen Version vom 24.10.2009 auch auf VS2010 Beta 2). Die academic license darf nur nicht kommerziell eingesetzt werden.  
   <http://research.microsoft.com/en-us/downloads/4ed7dd5f-490b-489e-8ca8-109324279968/default.aspx>
4. **Christina Hirth**

   [Oktober 26, 2009 um 7:45 pm](/posts/design-by-contract/)

   Hallo Rainer,

   jetzt hast du mich erwischt, das wusste ich tatsächlich nicht!

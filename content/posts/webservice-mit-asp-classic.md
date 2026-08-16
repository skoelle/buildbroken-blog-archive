---
title: ".NET-Webservice mit ASP-Classic ansprechen"
date: 2009-06-19
slug: webservice-mit-asp-classic
original_url: "https://aztec-project.org/blog/webservice-mit-asp-classic.html"
archive_url: "https://web.archive.org/web/20250114140710/https://aztec-project.org/blog/webservice-mit-asp-classic.html"
author: "Christina Hirth"
categories: ["Webservice"]
tags: [".NET", "ASP-Classic", "Refaktorisierung", "Webservice"]
---

Seit einiger Zeit sind wir dabei, unser Portal zu refaktorisieren. Das entfernte Ziel ist, alles in .NET um zu bauen. Das betrifft zur Zeit über tausend Seiten aber wir möchten noch in diesem Leben fertig sein <img src="/images/webservice-mit-asp-classic/icon_wink.gif" alt=";)" class="wp-smiley"/>

Dazu kommt noch, dass wir – selbstverständlich – agiles Softwarentwicklung betreiben, was eine ständige und rhythmische Iteration vorsieht, keine Mega-Projekte mit ungewissem Ende. Also haben wir die verschiedenen Bereiche identifiziert und diese werden einer nach dem anderen neu gebaut.  
Die neuen DLL-s in .NET werden mit Hilfe von verschiedenen Webservices angesprochen. Das führt allerdings unweigerlich dazu, 2 Technologien – ASP-Classic und .NET(C#) – miteinander sicher kommunizieren zu lassen. Das funktioniert so:

Dieser hier könnte der besagte .NET Webservice sein:

```
1 POST http://www.webAdresse.de/Webservice.asmx HTTP/1.1
    2 Host: webServer
    3 Content-Type: text/xml; charset=utf-8
    4 Content-Length: length
    5 SOAPAction: "http://tempuri.org/AendernEtwas"
    6 
    7 <?xml version="1.0" encoding="utf-8"?>
    8 <soap:Envelope xmlns:xsi=http://www.w3.org/2001/XMLSchema-instance 
    9  xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
   10   <soap:Body>
   11     <AendernEtwas xmlns="http://tempuri.org/">
   12       <id>int</id>
   13       <person>
   14         <nachname>string</nachname>
   15         <vorname>string</vorname>
   16       </person>
   17     </AendernEtwas>
   18   </soap:Body>
   19 </soap:Envelope>
```

Um ihn aufzurufen, brauchen wir in ASP folgendes:

```
    1 'Webserviceaufruf mit Angaben von Methodennamen und Parameter-XML
    2 Function webserviceCall(ByVal methode, ByVal xmlParameters)
    3     Dim objRequest, strRet
    4     Set objRequest = Server.createobject("MSXML2.XMLHTTP")
    5     With objRequest
    6     .open "POST", "http://www.webadresse.de/Webservices.asmx", False
    7     .setRequestHeader "Content-Type", "text/xml; charset=utf-8"
    8     .setRequestHeader "SOAPAction11", methode
    9     .send xmlParameters
   10     End With
   11     strRet = objRequest.responseText
   12     if CInt(objRequest.status) <> 200 then
   13         'Fehlerbehandlung, wenn Aufruf fehlgeschlagen
   14     end if
   15     Set objRequest = Nothing
   16     webserviceCall = strRet
   17 end function
```

Die Parameter werden so übergeben:

```
strParameters =  "<?xml version=""1.0"" encoding=""utf-8""?>"  & VbCrLf
strParameters = strParameters &  "<soap:Envelope xmlns:xsi=""http://www.w3.org/2001/XMLSchema-instance"" xmlns:xsd=""http://www.w3.org/2001/XMLSchema"" xmlns:soap=""http://www.w3.org/2003/05/soap-envelope"">"  & VbCrLf
strParameters = strParameters &  "    <soap:Body>"  & VbCrLf
strParameters = strParameters &  "        <AendernEtwas xmlns=""http://www.webadresse.de"">"  & VbCrLf
strParameters = strParameters &  "            <id>   & id &  </id>"  & VbCrLf
strParameters = strParameters &  "            <person>"  & VbCrLf
strParameters = strParameters &  "              <nachname><![CDATA["  & nachname &  "]]></nachname>"  & VbCrLf
strParameters = strParameters &  "              <vorname><![CDATA["  & vorname &  "]]></nachname>"  & VbCrLf
strParameters = strParameters &  "            </person>"  & VbCrLf
strParameters = strParameters &  "        </AendernEtwas>"  & VbCrLf
strParameters = strParameters &  "    </soap:Body>"  & VbCrLf
strParameters = strParameters &  "</soap:Envelope>"
```

Und das wäre dann alles, jetzt muss die Funktion nur noch aufgerufen werden:  
  
responseText = webserviceCall("AendernEtwas", strParameters)

Das Ergebnis kann man danach mit Microsoft.XMLDOM ausgelesen werden.

Noch ein paar Bemerkungen:  
- .NET ist im Gegensatz zu ASP-Classic case sensitive und eine stark typisierte Sprache, also obacht auf

1. die korrekte Schreibweise der Parameternamen in XML und auf
2. die Datentypen: strings müssen mit **CDATA** umklammert, Enums mit dem Namen angesprochen und Datumswerte in ISO 8601-Datumsformat (YYYY-MM-DDThh:min:sec.millisecond) angegeben werden.

## Kommentare (Archiv)

1. **kai**

   [Dezember 15, 2009 um 10:36 am](/posts/webservice-mit-asp-classic/)

   Wie sieht es mit den Visual Studio 2008 Webservices aus?

   Kann ich diese ebenfalls mit deiner Consumer-Funktion aufrufen?

   Bekomme leider folgenden Fehler:

   msxml3.dll- Fehler ’80004005′

   Unbekannter Fehler

   /root/sub/test/test.asp, line 34
2. **Christina Hirth**

   [Dezember 15, 2009 um 10:49 am](/posts/webservice-mit-asp-classic/)

   Klar, das funktioniert mit allen SOAP-Webservices. Die Fehlermeldung ist typisch Microsoft, kann alles mögliche bedeuten <img src="/images/webservice-mit-asp-classic/icon_wink.gif" alt=";)" class="wp-smiley"/>  
   Was steht bei dir in Zeile 34?
3. **kai**

   [Dezember 15, 2009 um 11:07 am](/posts/webservice-mit-asp-classic/)

   Oh… mir fällt gerade auf (ich nahm diesen Webservice, weil er LÄUFT und im Netz funktionsfähig ist), dass dieser Webservice eine Guid über einen Login generieren muss, deswegen funktioniert es mit Sicherheit nicht! <img src="/images/webservice-mit-asp-classic/icon_wink.gif" alt=";)" class="wp-smiley"/>

   Werde erstmal weiter schauen, trotzdem vielen Dank für die schnelle Antwort! <img src="/images/webservice-mit-asp-classic/icon_smile.gif" alt=":)" class="wp-smiley"/>

   Falls es nichts wird, melde ich mich noch einmal!
4. **kai**

   [Dezember 15, 2009 um 11:34 am](/posts/webservice-mit-asp-classic/)

   strRet = objRequest.responseText steht in dieser Zeile.

   Mit <http://localhost:port> und einer C#-Anwendung (lokal) kann ich auf den Dienst zugreifen, von meinem IIS-Server mit entsprechend geänderter  
   SOAP-URL (<http://IP:port>) und ausgeschalteter Firewall kommt es zu der Fehlermeldung.

   Ich benutze die automatisch mit generierte HelloWorld-Funktion, welche ich via ASP aufrufe.

   Was meinst du, könnte die Fehlerursache sein?
5. **Christina Hirth**

   [Dezember 15, 2009 um 12:13 pm](/posts/webservice-mit-asp-classic/)

   Wie schaut der Aufruf aus ? Und kannst du den Webservice mit der Adresse, die bei “.open “POST”, “http://www.webadresse.de/Webservices.asmx”, False” steht, erreichen?
6. **kai**

   [Dezember 15, 2009 um 12:59 pm](/posts/webservice-mit-asp-classic/)

   Mh, nein, dieser Development-Server, welcher das Visual Studio automatisch bereitstellt stellt beim F5 drücken ist scheinbar nicht von “außen” erreichbar, kann man dies irgendwie “umstellen”?
7. **kai**

   [Dezember 15, 2009 um 1:00 pm](/posts/webservice-mit-asp-classic/)

   Ich will nicht spammen, wollte dir das aber noch mit auf den Weg geben: Vielen Dank für den Code! <img src="/images/webservice-mit-asp-classic/icon_smile.gif" alt=":)" class="wp-smiley"/>
8. **Christina Hirth**

   [Dezember 15, 2009 um 1:03 pm](/posts/webservice-mit-asp-classic/)

   Hei Kai, kein Problem <img src="/images/webservice-mit-asp-classic/icon_smile.gif" alt=":)" class="wp-smiley"/>

   Du musst diesen Webservice Publishen, ihn auf einen erreichbaren Webserver veröffentlichen. Dann müsste alles passen.
9. **kai**

   [Dezember 15, 2009 um 3:03 pm](/posts/webservice-mit-asp-classic/)

   Ja, habe ich jetzt gemacht.

   Und jetzt habe ich das erst mit den strParameters verstanden, ich dachte die bräuchte man nur, wenn man der Methode des Webservice via SOAP Parameter übergeben wollen würde, dies war bis gerade auskommentiert.

   Es waren also 2 Sachen zu bewältigen… <img src="/images/webservice-mit-asp-classic/icon_wink.gif" alt=";)" class="wp-smiley"/>

   Jetzt läuft es, vielen Dank! <img src="/images/webservice-mit-asp-classic/icon_smile.gif" alt=":)" class="wp-smiley"/>

   Eine Frage bleibt bei mir aber noch offen!

   Ich habe die Funktion mit “” als Methode aufgerufen und es funktioniert trotzdem.

   Ist der Parameter überhaupt notwendig? Eigentlich teilt man doch schon über den Soap-Envelope (strParameters) mit, welche Funktion des Webservice man aufrufen möchte oder nicht?

   Wirklich, vielen Dank, Christina! <img src="/images/webservice-mit-asp-classic/icon_smile.gif" alt=":)" class="wp-smiley"/>
10. **Christina Hirth**

    [Dezember 15, 2009 um 3:20 pm](/posts/webservice-mit-asp-classic/)

    Ich weiß nicht genau, aber ich könnte mir sehr gut vorstellen, dass weil im Webservice eine einzige Funktion vorhanden ist, ist diese sozusagen die “Default”-Adresse <img src="/images/webservice-mit-asp-classic/icon_wink.gif" alt=";)" class="wp-smiley"/>  
    Aber die Frage ist interessant, ich werde das bei der nächsten Gelegenheit überprüfen.

    Es freut mich sehr, dass du auch so begeistert bist, wie ich damals war, als es das erste mal diese alte Technik-neue Technik Kommunikation hingehauen hat

    Sehr gerne und schöne Feiertage !
11. **kai**

    [Dezember 15, 2009 um 3:29 pm](/posts/webservice-mit-asp-classic/)

    Habe den Methoden-Parameter jetzt komplett aus deiner Funktion herausgenommen und folgende Zeile auskommentiert:

    ‘ .setRequestHeader “SOAPAction11″, methode

    Und es tut immer noch das, was es soll.

    Deine Default-Theorie kann es leider nicht sein, weil ich bereits 2 Methoden in meinem Webservice habe.

    Sehr interessant… <img src="/images/webservice-mit-asp-classic/icon_smile.gif" alt=":)" class="wp-smiley"/>

    Nunja, hauptsache es funktioniert, WIE ist nur halb so wichtig! <img src="/images/webservice-mit-asp-classic/icon_wink.gif" alt=";)" class="wp-smiley"/>

    Wünsche dir ebenfalls schöne Feiertage, bin für heute erstmal raus.

    Bye, bye.
12. **[cortez1975](http://gmail.com/)**

    [Januar 24, 2012 um 9:45 am](/posts/webservice-mit-asp-classic/)

    The ashes life running now the 1992 academician was suspended, and a unattended distributorless blaze society parking was topped in contemplation of the exposable sweetkins predict conservation. [http://ogymes.com](http://ogymes.com/)

---
title: "Testen von nicht öffentlichen Methoden"
date: 2009-08-12
slug: test-public-methods
original_url: "https://aztec-project.org/blog/test-public-methods.html"
archive_url: "https://web.archive.org/web/20250114141241/https://aztec-project.org/blog/test-public-methods.html"
author: "Christina Hirth"
categories: ["How-To", "Unit Testing"]
---

Wir fragen uns seit langem, wie man `internal` Methoden testen kann, da eins klar ist, die Kapselung darf nicht wegen der Testfähigkeit verletzt werden.  
Letzte Woche hatte zum Glück auch jemand anderer dieses Problem und er hat gleich bei [CCD-GoogleGroup](http://groups.google.com/group/clean-code-developer) nachgefragt. Und so haben wir auch erfahren, wie die Lösung lautet:

> für “internal”-Elemente gibt es auch die Option mit [assembly:  
> InternalsVisibleTo("TestAssembly")] zu arbeiten. Alternativ kannst du die zu  
> testenden Klassen auch per “Add existing item” und dann “Add as link” (siehe  
> kleines Dreieck neben dem “Add”-Button) zum Testprojekt hinzufügen.

(Danke [Alex](http://groups.google.com/groups/profile?enc_user=oc5IRhcAAAAuR_jK16wX7vC61npQCQRRuMwB60D2RE2h9ZtdV0_Uhw))

Danach war nur noch ein wenig Surfen nötig, um alles zu erfahren:

[msdn](http://msdn.microsoft.com/en-us/library/system.runtime.compilerservices.internalsvisibletoattribute.aspx)  sagt:

InternalsVisibleToAttribute Class

Specifies that types that are ordinarily visible only within the current assembly are visible to another assembly.

**User comment:**  
It is not documented anywhere to my knowledge, but if you want to grant “InternalsVisibleTo” permission to more than one assembly, you need to understand the syntax.

To do this you should NOT insert multiples instances of:

`[assembly: InternalsVisibleTo("FirstAssembly")]`

Instead do this:

`[assembly: InternalsVisibleTo("FirstAssembly"),  
InternalsVisibleTo("SecondAssembly"),  
InternalsVisibleTo("ThirdAssembly")]`

The former syntax is legal but fails, because each instance simply redefines and replaces any earlier ones, the latter syntax works as required.

## Kommentare (Archiv)

1. **Thomas Christain**

   [August 12, 2009 um 8:28 pm](/posts/test-public-methods/)

   Das ist natürlich eine super Sache.  
   Sowohl internal Klassen, als auch internal Methoden werden für die gekennzeichnete assembly freigegeben.

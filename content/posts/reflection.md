---
title: "Wozu dient Reflection"
date: 2009-06-24
slug: reflection
original_url: "https://aztec-project.org/blog/reflection.html"
archive_url: "https://web.archive.org/web/20250114131122/https://aztec-project.org/blog/reflection.html"
author: "Thomas Christian"
categories: ["How-To"]
tags: ["Assemblies", "Assemby", "C#", "Reflection"]
---

## Vorbereitung

Über Reflection kann man zur Laufzeit relativ einfach an alle Informationen eines Assembly herankommen. So ist es möglich, dass man von einem Assembly den Namen, Klassen, Methoden mit ihren Parametern, Eigenschaften und Rückgabewerte, usw. auslesen kann. Aber nicht nur das Auslesen ist möglich, sondern auch das Setzen.

Jetzt stellt sich für den einen oder anderen vielleicht die Frage, warum man zur Laufzeit auf diese Daten zugreifen kann. Jede Assembly verfügt über Module in denen sich die einzelnen Typen(Klassen) befinden. Für jedes Modul gibt es Metadaten, in denen die einzelnen Typen beschrieben werden. Die Assembly selbst verfügt noch über ein Manifest, in dem sich alle Informationen zum Assembly (z.B. Name, Version) befinden. Wenn man über Reflection auf Assemblies zugreift, dann werden diese Metadaten und das Manifest dafür herangezogen. Die Metadaten verfügen zwar noch über die Informationen, welche Modifizierer für Methoden, Properties, usw. verwendet wurden, aber der MSIL-Code (die Zwischensprache, die vom Endcompiler in die plattformspezifische Sprache übersetzt wird) nicht mehr. Die Modifizierer sind nur für den Compiler relevant und werden nach dem Kompilieren nicht mehr berücksichtigt. Somit ist es auch möglich über Reflection Properties, Methoden, usw. zu verwenden, die nicht öffentlich sind.

Für dieses Beispiel habe ich eine kleine Konsolen-Anwendung geschrieben (TestApplication), welche eine Referenz auf das Assembly TestProject.dll hat. Dieses Assembly hat zwei von mir erstellte Typen (Klassen) TestClass und SecondTestClass. In den beiden Klassen steckt keine Logik. Sie sind ausschließlich für dieses Beispiel erstellt worden, um ein paar Daten zu modifizieren und um zu zeigen wie die Informationen aus dem Assembly ausgelesen und verändert werden können und dass es möglich ist an nicht-öffentliche Methoden heranzukommen.

**TestClass.cs**

```
using  System.Security.Cryptography;
using  System.Text;
namespace  TestProject {
class   TestClass  {
public   string  Name {  get ;  set ; }
public   string  Surname {  get ;  set ; }
private   string  Password {  get ;  set ; }
public   string  GetFullName() {
return   string .Format( "{0} {1}" , Name ??  string .Empty, Surname ??  string .Empty).Trim();
}
public   void  SetPasswort( string  password){
Password = password;
}
private   static   string  CalcPassword( string  password){
MD5  md5 =  MD5 .Create();
byte [] data = md5.ComputeHash( Encoding .Default.GetBytes(password));
StringBuilder  hashPassword =  new   StringBuilder ();
foreach  ( byte  b  in  data){
hashPassword.Append(b);
}
return  hashPassword.ToString();
}
public   static   string  DoSomething( string  value) {
// do something
return  value;
}
}
```

**SecondTestClass.cs**

```
namespace  TestProject {
public   class   SecondTestClass  {
public   int  Addition( int  a,  int  b) {
return  a + b;
}
public   int  Multiply( int  a,  int  b) {
return  a * b;
}
public   double  Divide( int  a,  int  b) {
if  (b == 0)  return  0;
return  a / b;
}
}
}
 .
.
```

## Auslesen von Assembly- Type-Informationen

Mit der Methode Thread.GetDomain().GetAssemblies() bekommt man alle referenzierten Assemblies der aktuellen Domäne. Damit die TestProject-Assembly auch in dieser Domäne vorhanden ist, muss vor dem Aufruf dieser Methode eine Instanz von einem Objekt dieses Assemblies erzeugt werden.

Um sich nun alle Assemblies der aktuellen Domäne anzeigen zu lassen, könnte man folgendes schreiben:

```
static   void  Main( string [] args) {
SecondTestClass  secondTestClass =  new   SecondTest   Class ();
Assembly [] assemblies =  Thread .GetDomain().GetAssemblies();
foreach  ( var  assembly  in  assemblies) {
Console .WriteLine( string .Format( "-- {0} ver.: {1}" , assembly.GetName().Name
                                                          , assembly.GetName().Version));
}
Console .ReadLine();
}
```

.

Nun könnte man noch alle zur Verfügung stehenden Typen(Klassen) aus der TestProject-Assembly anzeigen.

```
static   void  Main( string [] args) {
SecondTestClass  secondTestClass =  new   SecondTestClass ();
Assembly [] assemblies =  Thread .GetDomain().GetAssemblies();
foreach  ( var  assembly  in  assemblies) {
Console .WriteLine( string .Format( "-- {0} ver.: {1}" , assembly.GetName().Name
                                                           , assembly.GetName().Version));
if  (assembly.GetName().Name.Equals( "TestProject" )) {
Type [] types = assembly.GetTypes();
foreach  ( var  type  in  types) {
Console .WriteLine( "  ++{0}" , type.Name);
}
}
}
Console .ReadLine();
}
```

.

Wenn man nun allerdings Informationen eines bestimmten Types haben möchte, so werden diese Informationen aus den Metadaten des Moduls geladen, in dem sich der Type befindet. Um zum Beispiel alle öffentlichen Methoden eines Types anzuzeigen, könnte man folgendes schreiben:

```
static   void  Main( string [] args) {
SecondTestClass  secondTestClass =  new   SecondTestClass ();
Assembly [] assemblies =  Thread .GetDomain().GetAssemblies();
foreach  ( var  assembly  in  assemblies) {
Console .WriteLine( string .Format( "-- {0} ver.: {1}" , assembly.GetName().Name
                                                          , assembly.GetName().Version));
if  (assembly.GetName().Name.Equals( "TestProject" )) {
Type [] types = assembly.GetTypes();
foreach  ( var  type  in  types) {
Console .WriteLine( "  ++ {0}" , type.Name);
MethodInfo [] methodInfos = type.GetMethods();
foreach  ( var  info  in  methodInfos) {
Console .WriteLine( "    ++ {0}" , info.Name);
}
}
}
}
Console .ReadLine();
}
```

.

Es fällt auf, dass auch die Methoden ToString, Equals, GetHashCode und GetType in beiden Klassen angezeigt werden, obwohl diese in den Klassen überhaupt nicht deklariert wurden. Das liegt daran, dass alle Typen von object ableiten und object diese Methoden implementiert. Was noch auffällt ist, dass nur öffentliche Methoden angezeigt werden. Möchte man sich auch die privaten Methoden anzeigen lassen, so muss man der Methode type.GetMethods Parameter übergeben. Diese Methode verlangt BindingFlags, die man mit dem Bitweise ODER-Operator (|) miteinander verknüpfen kann. Um sich nun öffentliche und private Methoden anzeigen zu lassen, muss der Aufruf der Methode type.GetMethods folgendermaßen lauten:

```
MethodInfo[] methodInfos = type.GetMethods(BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance);
```

Dieser Aufruf gibt an, dass man alle öffentlichen und nicht-öffentlichen Instanz-Methoden bekommen möchte. Instanz-Methoden bedeutet, dass es sich um Methoden handelt, die nur mit dem Instanzieren eines Objektes zur Verfügung stehen. D.h. es werden keine static-Methoden angezeigt. Es gibt noch weitere BindingFlags, auf die ich hier allerdings nicht weiter eingehen möchte.

Das ganze könnte man natürlich noch in der Form weiter treiben, dass man sich die kompletten Methodensignaturen mit Modifizierer, Schlüsselwort und Rückgabewert anzeigen lässt:

```
static   void  Main( string [] args) {
SecondTestClass  secondTestClass =  new   SecondTestClass ();
Assembly [] assemblies =  Thread .GetDomain().GetAssemblies();
foreach  ( var  assembly  in  assemblies) {
Console .WriteLine( string .Format( "-- {0} ver.: {1}" , assembly.GetName().Name, assembly.GetName().Version));
if  (assembly.GetName().Name.Equals( "TestProject" )) {
Type [] types = assembly.GetTypes();
foreach  ( var  type  in  types) {
Console .WriteLine( "  ++ {0}" , type.Name);
MethodInfo [] methodInfos = type.GetMethods( BindingFlags .Public |  BindingFlags .NonPublic
                                                                               |  BindingFlags .Instance
                                                                                |  BindingFlags .Static);
foreach  ( var  info  in  methodInfos) {
string  modifier = GetModifier(info);
string  keyword = GetKeyword(info);
string  parameters = GetParameters(info);
if  (! string .IsNullOrEmpty(keyword)) {
keyword =  string .Format( "{0} " , keyword);
}
Console .WriteLine( "    ++ {0} {1}{2}{3}({4})" , modifier, keyword
                                                                 , info.ReturnParameter, info.Name, parameters);
}
}
}
}
Console .ReadLine();
}
private   static   string  GetModifier( MethodInfo  info) {
if  (info.IsPublic)  return   "public" ;
return   "private" ;
}
private   static   string  GetKeyword( MethodInfo  info) {
if  (info.IsStatic)  return   "static" ;
if  (info.IsVirtual)  return   "virtual" ;
return   string .Empty;
}
private   static   string  GetParameters( MethodInfo  info) {
StringBuilder  parameters =  new   StringBuilder ();
ParameterInfo [] parameterInfos = info.GetParameters();
if  (parameterInfos !=  null ) {
foreach  ( ParameterInfo  parameterInfo  in  parameterInfos) {
if  (! string .IsNullOrEmpty(parameters.ToString())) {
parameters.Append( ", " );
}
parameters.AppendFormat( "{0} {1}" , parameterInfo.ParameterType.Name, parameterInfo.Name);
}
}
return  parameters.ToString();
}
```

.

Nicht immer ist bereits während der Entwicklung bekannt, aus welchem Assembly man Informationen benötigt. Sodass die Methode Thread.GetDomain().GetAssemblies() nicht verwendet werden kann. Eine weitere Möglichkeit an ein Assembly zu kommen ist es direkt zu laden. Dafür bietet die Klasse Assembly die statische Methode Assembly.LoadFrom zum Laden von Assemblies. Statt dem Laden des Assembly über die aktuelle Domäne, wird das nächste Beispiel so modifiziert, dass die TestProject-Assembly direkt aus einem Verzeichnis heraus geladen wird.

```
static   void  Main( string [] args) {
Assembly  assembly =  Assembly .LoadFrom( @"c:\TestProject.dll" );
if  (assembly !=  null ) {
Console .WriteLine( string .Format( "-- {0} ver.: {1}" , assembly.GetName().Name, assembly.GetName().Version));
Type [] types = assembly.GetTypes();
foreach  ( var  type  in  types) {
Console .WriteLine( "  ++ {0}" , type.Name);
MethodInfo [] methodInfos =
type.GetMethods( BindingFlags .Public |  BindingFlags .NonPublic |  BindingFlags .Instance |
BindingFlags .Static);
foreach  ( var  info  in  methodInfos) {
string  modifier = GetModifier(info);
string  keyword = GetKeyword(info);
string  parameters = GetParameters(info);
if  (! string .IsNullOrEmpty(keyword)) {
keyword =  string .Format( "{0} " , keyword);
}
Console .WriteLine( "    ++ {0} {1}{2}{3}({4})" , modifier, keyword, info.ReturnParameter,
info.Name, parameters);
}
}
}
Console .ReadLine();
}
```

Man sieht, dass die gleiche Ausgabe wie bereits im vorherigen Beispiel generiert wird.

## Interaktionen

Nachdem die Vorgehensweise nun klar sein sollte, möchte ich nun den eigentlich interessanten Teil demonstrieren. Wie kann man nun auf Methoden usw. zugreifen und wie können Werte aus einem Type gelesen und veränder werden? Wenn man die Methode SecondTestClass.Addition(int a, int b) aufrufen möchte, dann braucht man die Methodeninformationen von dem Type SecondTestClass aus dem TestProject-Assembly. D.h. man muss wie in den obigen Beispielen auch über alle Typen iterieren, um an den gesuchten Type SecondTestClass zu kommen. Hat man den gesuchten Type gefunden, so kann man sich von diesem alle Methoden in einem Array zurückgeben lassen. Dieses Array kann dann wieder ganz normal durchlaufen und nach der gewünschten Methode durchsucht werden. Hat man die Methode gefunden so muss zuerst eine Instanz von dem Objekt erzeugt werden und dafür gibt es den Activator, der die statische Methode CreateInstance beinhaltet. Als Parameter übergibt man ihr den Type von dem eine Instanz erzeugt werden soll. Jetzt kann man über die MethodInfo die Methode aufrufen. Dazu muss der Methode die Instanz des Objektes übergeben werden, von welchem die Methode aufgerufen werden soll und zusätzlich noch ein Array von Objekten, welche die zu übergebenen Parameter beinhaltet. Hat die Methode keine Parameter, so muss null übergeben werden. Dabei muss der Rückgabewert in den erwarteten Wert gecastet werden. Das ganze könnte dann folgendermaßen aussehen:

```
static   void  Main( string [] args) {
Assembly  assembly =  Assembly .LoadFrom( @"c:\TestProject.dll" );
if  (assembly !=  null ) {
Console .WriteLine( string .Format( "-- {0} ver.: {1}" , assembly.GetName().Name, assembly.GetName().Version));
Type [] types = assembly.GetTypes();
foreach  ( var  type  in  types) {
if  (type.Name.Equals( "SecondTestClass" )) {
Console .WriteLine( "  ++ {0}" , type.Name);
MethodInfo [] methodInfos = type.GetMethods();
foreach  ( var  info  in  methodInfos) {
if  (info.Name.Equals( "Addition" )) {
object  obj =  Activator .CreateInstance(type);
int  value = ( int )info.Invoke(obj,  new   object [] { 2, 5 });
Console .WriteLine( "    ++ {0}(2 + 5) = {1}" , info.Name, value);
}
}
}
}
}
Console .ReadLine();
}
```

Aufruf der Methode Addition

.

Bei statischen Methoden kann das Erzeugen der Instanz weggelassen werden und für den Parameter des Instanz-Objektes kann null übergeben werden.

```
if  (type.Name.Equals( "TestClass" )) {
Console .WriteLine( "  ++ {0}" , type.Name);
MethodInfo [] methodInfos = type.GetMethods( BindingFlags .NonPublic |  BindingFlags .Static);
foreach  ( var  info  in  methodInfos) {
if  (info.Name.Equals( "CalcPassword" )) {
string  value = ( string )info.Invoke( null ,  new   object [] {  "myPassword"  });
Console .WriteLine( "    ++ {0}(\"myPassword\") = {1}" , info.Name, value);
}
}
}
```

Das übergebene Passwort wurde über eine statische Methode gehashed.

.

Um den Wert einer Property auszulesen, muss anstelle von MethodInfo die PropertyInfo verwendet werden. Aus dieser kann dann über die Methode PropertyInfo.GetValue der aktuelle Wert zurückgegeben werden. Da in diesem Beispiel nach dem Instanzieren des Objektes noch keine Werte zugewiesen wurden, sind die Properties leer.

```
static   void  Main( string [] args) {
Assembly  assembly =  Assembly .LoadFrom( @"C:\ TestProject.dll" );
if  (assembly !=  null ) {
Console .WriteLine( string .Format( "-- {0} ver.: {1}" , assembly.GetName().Name, assembly.GetName().Version));
Type [] types = assembly.GetTypes();
foreach  ( var  type  in  types) {
if  (type.Name.Equals( "TestClass" )) {
Console .WriteLine( "  ++ {0}" , type.Name);
                 object  obj =  Activator .CreateInstance(type);
PropertyInfo [] propertyInfos = type.GetProperties( BindingFlags .Public |  BindingFlags .NonPublic
                                                                                      |  BindingFlags .Instance);
foreach  ( var  info  in  propertyInfos) {
Console .WriteLine( "    ++ {0} = {1}" , info.Name, info.GetValue(obj,  null ));
}
}
}
}
Console .ReadLine();
}
```

.

Wenn man nun die Properties mit Werten belegen möchte, so muss man analog zur Methode PropertyInfo.GetValue, die Methode PropertyInfo. SetValue verwenden.

```
if  (type.Name.Equals( "TestClass" )) {
Console .WriteLine( "  ++ {0}" , type.Name);
PropertyInfo [] propertyInfos = type.GetProperties( BindingFlags .Public |  BindingFlags .NonPublic
                                                                          |  BindingFlags .Instance);
propertyInfos[0].SetValue(obj,  "Peter" ,  null );
propertyInfos[1].SetValue(obj,  "Müller" ,  null );
propertyInfos[2].SetValue(obj,  "myPassword" ,  null );
foreach  ( var  info  in  propertyInfos) {
Console .WriteLine( "    ++ {0} = {1}" , info.Name, info.GetValue(obj,  null ));
}
}
```

.

## Wozu braucht man jetzt aber nun die Reflection?

Nun ja, die meisten Programme werden Reflection wohl nie benötigen oder verwenden. Es wird vorallem bei dem Entwickeln von Debuggern, Interpretern, TestTools, Logger oder auch für O/R-Mapper verwendet. Es wird also überall dort gebraucht, wo während der Laufzeit nicht klar ist, welche Assemblies verwendet werden und welche Informationen man aus diesen lesen oder manipulieren möchte.

## kurze Zusammenfassung:

Wie man gesehen hat, ist der Aufbau einer Assembly mit ihren Typen hierarchisch. Um zb. an einen Parameter einer Methode eines Types zu kommen, braucht man zuerst das Assembly welches den Typ enthält. Von diesem lässt man sich ein Array von Typen geben. Von dem gesuchten Typ lässt man sich dann ein Array von Methoden geben. Von der gesuchten Methode holt man sich nun ein Array von allen Parametern. Dieses Array kann dann nach dem gewünschten Parameter durchsucht werden.

Es gibt natürlich für all diese Methoden auch Methoden, mit denen man sich den Type, die Methodeninformation, die Parameterinformation, usw. direkt mit der entsprechenden Bezeichnung holen kann. Ich wollte hier nur auf die Hierarchie aufmerksam machen.

Wie man in diesen Beispielen erkennen konnte, ist es möglich, ohne Probleme auf alle Informationen von einem Assembly zuzgreifen, sich die Types zu laden, dessen öffentliche und auch nicht-öffentliche Werte zu lesen und zu manipulieren und auch Methoden auszuführen. Man kann sich auch lokale Werte anzeigen lassen, in dem man sich den MethodBody des Objekte geben lässt, von denen man die lokalen Werte ermitteln möchte.

---
title: "Umsetzung des Plug-In-Patterns"
date: 2009-06-05
slug: plugin-pattern
original_url: "https://aztec-project.org/blog/plugin-pattern.html"
archive_url: "https://web.archive.org/web/20250114120158/https://aztec-project.org/blog/plugin-pattern.html"
author: "Thomas Christian"
categories: ["How-To"]
tags: ["Architektur", "C#", "HowTo", "Plug-In"]
---

In meinem ersten Blog-Post möchte ich euch in vereinfachter Form meine Umsetzung des Plug-In-Patterns vorstellen.  
Voraussetzungen für dieses Pattern sind:

* eine Host-Applikation die das Plug-In laden möchte
* ein Plug-In welches es zu laden gilt
* und die Schnittstellen Plugin und IHost

Zu allererst brauchen wir eine gemeinsame Schnittstelle, die sowohl vom Plug-In als auch vom Host (die Applikation welche das Plug-In verwenden soll) benutzt werden soll. Über diese Schnittstelle kommuniziert der Host mit dem Plug-In.  
Es würde sich das Interface IPlugIn anbieten. In meinem Fall verwende ich allerdings kein Interface sondern eine abstrakte Klasse, da ich bereits Logik direkt in die Schnittstelle implementieren möchte. In meinem Fall heißt die abstrakte Klasse einfach nur Plugin. Im weiteren Verlauf werde ich zu meiner abstrakten Klasse Schnittstelle sagen.

```
public   abstract   class   Plugin  {
private  IHost m_host;
public  Plugin( string  name) {
Name = name;
}
6
public   string  Name {  get ;  set ; }
public   string  Author {  get ;  set ; }
public   string  Version {  get ;  set ; }
public   bool  IsRegistered {  get ;  private   set ; }
11
///   <summary>
///  Setzt oder gibt die Host-Application.
///   </summary>
///   <value> Host-Application. </value>
public  IHost Host {
get  {  return  m_host; }
set  {
if  ( value  !=  null ) {
if  (m_host ==  null ) {
m_host =  value ;
if  (m_host.Register( this )) {
IsRegistered =  true ;
}
}
}  else  {
if  (m_host.Unregister( this )) {
m_host =  value ;
IsRegistered =  false ;
}
}
}
}
}
```

Ich glaube, der Aufbau der Schnittstelle Plugin sollte bis auf die Property “Host” klar sein. Wie man sieht, benötigt man bei diesem Pattern zusätzlich zur Schnittstelle Plugin noch das IHost-Interface.  
Dieses Interface ist direkter Bestandteil der Schnittstelle Plugin. Nun kann man sich natürlich die Frage stellen, warum das Plug-In den Host kennen muss und somit von diesem abhängig ist.

Zum einen ist es in der Regel so, dass ein Plug-In für nur einen Host entwickelt wird und zum anderen wollte ich dem Host gewisse Richtlinien zum Registrieren und Lösen des Plug-Ins vorgeben.

Das Interface IHost sieht folgendermaßen aus:

```
public   interface   IHost  {
bool  Register(Plugin plugin);
bool  Unregister(Plugin plugin);
}
```

Dieses Interface muss von der Host-Applikation implementiert werden, damit sich das Plug-In am Host registrieren kann. Im letzten Satz habe ich es schon angedeutet. Nicht der Host registriert das Plug-In bei sich, sondern das Plug-In registriert sich am Host. Durch das setzen der Property Plugin.Host wird die Methode Register oder Unregister vom Plug-In aufgerufen, welche der Host implementiert.

Eine vereinfachte Darstellung der Implementierung des IHost -Interfaces sieht folgendermaßen aus:

```
public   class   HostApplication  : IHost {
private  List<Plugin> m_pluginList;
3
//Konstruktor
public  HostApplication() {
m_pluginList =  new  List<Plugin>();
7
//Lädt alle verfügbaren Plug-Ins zb. aus einem Verzeichnis
List<Plugin> plugins = GetPlugins();
foreach  (Plugin plugin  in  plugins) {
//ruft implizit die IHost.Register-Methode auf
plugin.Host =  this ;
}
}
15
public   void  ShowPlugins() {
foreach  (Plugin plugin  in  m_pluginList) {
//Ausgabe der Namen aller am Host registrierten Plug-Ins
Console.WriteLine(plugin.Name);
}
}
22
public   void  UnloadPlugins() {
foreach  (Plugin plugin  in  m_pluginList) {
//ruft implizit die IHost.Unregister-Methode auf
plugin.Host =  null ;
}
}
29
#region  IHost-Implementierung
public   bool  Register(Plugin plugin) {
if  (!m_pluginList.Contains(plugin)) {
m_pluginList.Add(plugin);
return   true ;
}
return   false ;
}
38
public   bool  Unregister(Plugin plugin) {
if  (m_pluginList.Contains(plugin)) {
m_pluginList.Remove(plugin);
return   true ;
}
return   false ;
}
#endregion
}
```

Das Registrieren und Lösen der Plug-Ins könnte man nun noch in einen Plug-In-Manager auslagern, worauf ich in diesem Blog allerdings verzichten möchte.

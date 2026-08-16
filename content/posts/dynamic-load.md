---
title: "Dynamisches Laden von Assemblies"
date: 2009-06-05
slug: dynamic-load
original_url: "https://aztec-project.org/blog/dynamic-load.html"
archive_url: "https://web.archive.org/web/20250601101323/https://aztec-project.org/blog/dynamic-load.html"
author: "Thomas Christian"
categories: ["How-To"]
tags: ["Assembly", "C#", "HowTo", "Reflection"]
---

In diesem Blog-Post möchte ich kurz erläutern, wie ich mit dem Problem des dynamischen Ladens von Assemblies umgegangen bin.

Vor einiger Zeit stand ich vor dem Problem, dass ich zur Laufzeit Assemblies austauschen wollte. Grund dafür war, dass ich eine Host-Applikation hatte, die Plug-Ins verwendet. Jetzt wollte ich bestehende Plug-Ins während der Laufzeit austauschen oder neue Plug-Ins hinzufügen ohne die Host-Applikation zu beenden. Dazu hatte ich ein Verzeichnis in dem sich, außer den Plug-Ins, alle Assemblies befanden. Die Plug-Ins selbst befanden sich in einem eigenen Unterverzeichnis. Selbst wenn die Plug-Ins von der Host-Applikation nicht mehr verwendet wurden, war es nicht möglich, diese Assemblies zu löschen.

Im Normalfall ist es so, dass sobald eine Assembly von einer Applikation verwendet wird, eine Referenz auf diese existiert. Diese Referenz wird leider erst gelöscht, wenn die ganze Applikation beendet wird.

Bei dem dynamischen Laden von Assemblies wird die zu ladende Assembly geöffnet, ausgelesen und dann geschlossen. Aus den ausgelesenen Bytes wird dann mittels Reflection eine Assembly im Arbeitsspeicher erzeugt. Auf die lokale Assembly hängt somit keine Referenz und es ist möglich diese zu löschen.

Meine Umsetzung sieht folgendermaßen aus:

```
public  IList<Plugin> GetPlugins( string  assemblyName) {
Assembly assembly;
IList<Plugin> pluginList =  new  IList<Plugin>();
try  {
byte [] byteAssembly = File.ReadAllBytes(assemblyName);
assembly = Assembly.Load(byteAssembly);
}  catch  (Exception ex) {
log.Error(ex);
}
try  {
if  (assembly !=  null ) {
Type[] assemblyTypes = assembly.GetTypes();
foreach  (Type assemblyTyp  in  assemblyTypes) {
if  ( typeof (Plugin).IsAssignableFrom(assemblyTyp)) {
plugin = (Plugin)assembly.CreateInstance(assemblyTyp
.FullName);
if  (plugin !=  null ) {
pluginList.Add(plugin);
}
}
}
}
}  catch  (ReflectionTypeLoadException ex) {
log.Error(ex);
}
return  pluginList;
}
```

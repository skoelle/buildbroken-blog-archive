---
title: "Unit-Tests für WebForms"
date: 2009-09-07
slug: unittests-webforms
original_url: "https://aztec-project.org/blog/unittests-webforms.html"
archive_url: "https://web.archive.org/web/20250114121657/https://aztec-project.org/blog/unittests-webforms.html"
author: "Christina Hirth"
categories: ["How-To", "Unit Testing", "Webanwendungen"]
tags: ["Unit-Tests", "Webapplication"]
---

Obwohl die allgemeine Meinung ist, dass es sehr schwierig sei, kann man mit folgendem Workaround Webforms sehr einfach und sehr umfangreich testen. Bedingung 1: als Projekt kein Web Site Project sondern eine Web Application erstellen. Bedingung 2: Business Logic in die entsprechende Schicht auslagern.

Nehmen wir zum Beispiel ein einfaches Formular. Nach Absenden des Formulars sollen die Werte aus den 2 Feldern addiert werden. Wenn man per QueryString einen Parameter `multiple` übergibt, soll das Ergebnis damit multipliziert werden.

<img src="/images/unittests-webforms/TestableWebForm.jpg" alt="Testable WebForm"/>   <img src="/images/unittests-webforms/TestableWebForm_Sent.jpg" alt="Testable WebForm Sent"/>

Und nun zum Quellcode: Die automatisch erstellte .designer.cs muss entfernt werden, was man sowieso tun sollte, da man automatisch erstellten Code – also Code, den keiner außer Microsoft unter Kontrolle hat – vermeiden sollte.  
Die Inhalte der .designer.cs – also die Definitionen der Web-Elemente – werden in der Klasse als `Public Properties` erstellt und instantiiert, um bei Zugriffen wie `TextBox.Text` keine NullReferenceException zu bekommen.

```
using  System;
using  System.Web.UI.HtmlControls;
using  System.Web.UI.WebControls;
using  framework.Testable.Web.UI;
5
namespace  TestableWebForm
{
public   class   DefaultPage  : System.Web.UI. Page
{
10
#region  Controls
public   HtmlForm  Formular;
public   TextBox  Value1 =  new   TextBox ();
public   TextBox  Value2 =  new   TextBox ();
public   Label  Result =  new   Label ();
public   Button  Submit =  new   Button ();
#endregion
```

Um das Verhalten testen zu können, haben wir Adapter für die Klassen `System.Web.UI.Page`, `System.Web.HttpRequest` und `System.Web.HttpResponse` geschrieben, und zwar für die Properties und Methoden die uns vorerst interessieren: z.B. `Page.IsPostBack, Page.Request, Response.Redirect(string url, bool endResponse)`. Bei der Benennung haben wir einfach den Namespace `System` mit `framework.Testable` ersetzt und wir haben natürlich zu jedem Testable-Objekt einen Interface erstellt.

```
1
namespace  framework.Testable.Web
{
namespace  UI
{
public   interface   IPage
{
bool  IsPostBack{  get ; }
IHttpRequest  Request{  get ;  set ; }
IHttpResponse  Response{  get ;  set ; }
}
12
public   class   Page  :  IPage
{
private   readonly  System.Web.UI. Page  m_page;
private   IHttpRequest  m_request;
private   IHttpResponse  m_response;
18
public  Page( System.Web.UI. Page  page )
{
m_page = page;
m_request =  new   HttpRequest ( m_page );
m_response =  new   HttpResponse ( m_page );
}
25
public   bool  IsPostBack
{
get {  return  m_page.IsPostBack; }
}
30
public   IHttpRequest  Request
{
get {  return  m_request; }
set  { m_request =  value ; }
}
36
public   IHttpResponse  Response
{
get {  return  m_response; }
set  { m_response =  value ; }
}
}
}
}
```

Um alle gemockte Objekte setzen zu können, haben wir unserer `Page`-Klasse auch Setter für `Request` und `Response` gegeben. Da man `Request.Params` nicht setzen kann, d.h. `Request.Params[]` immer ein NullReferenceException verursachen würde, haben wir das Auslesen der `Request`-Parameter in eine Methode `Request.GetParamValue(string name)` ausgelagert.

Das war ungefähr alles: in der Seite nutzt man dann anstelle der eigenen Request und Response-Objekten die `Testable`-Objekte.

```
public   class   DefaultPage  : System.Web.UI. Page
{
…
private   IPage  m_page;
public   void  SetTestableObjects(  IPage  page )
{
m_page = page;
}
24
public   void  Page_Load(  object  sender,  EventArgs  e )
{
if  (m_page ==  null ) m_page =  new   Page (  this  );
int  multiple = 1;
if  (! string .IsNullOrEmpty( m_page.Request.GetParamValue(  "multiple"  ) )) multiple =  Convert .ToInt32( m_page.Request.GetParamValue(  "multiple"  ) );
if  (m_page.IsPostBack)
{
Result.Text = ( ( Convert .ToInt32( Value1.Text ) +  Convert .ToInt32( Value2.Text ))*multiple ).ToString();
}
}
```

Damit ist die Web-Anwendung bereit zum Testen. So schaut zum Beispiel ein Test für das Laden der Seite aus:

```
using  framework.Testable.Web;
using  framework.Testable.Web.UI;
using  NUnit.Framework;
using  Rhino.Mocks;
using  TestableWebForm;
6
namespace  Tests
{
[ TestFixture ]
public   class   WebFormTests
{
private   IPage  m_page;
private   IHttpRequest  m_request;
private   IHttpResponse  m_response;
private   DefaultPage  m_defaultPage;
16
[ SetUp ]
public   void  Init()
{
m_page =  MockRepository .GenerateStub< IPage >();
m_request =  MockRepository .GenerateStub< IHttpRequest >();
m_response =  MockRepository .GenerateStub< IHttpResponse >();
m_page.Request = m_request;
m_page.Response = m_response;
}
26
[ Test ]
public   void  PageLoad_Loading_EmptyFields()
{
// Arrange
31
32
// Act
m_defaultPage =  new   DefaultPage ();
m_defaultPage.SetTestableObjects(m_page);
m_defaultPage.Page_Load(  null ,  null  );
37
// Assert
Assert .IsEmpty( m_defaultPage.Value1.Text );
Assert .IsEmpty( m_defaultPage.Value2.Text );
Assert .IsEmpty(m_defaultPage.Result.Text);
}
```

Und so für PostBack inklusive QueryString-Parameter:

```
[ Test ]
public   void  PageLoad_PostBackWithRequestValue_ResultIsCorrect()
{
// Arrange
const   int  value1 = 1;
const   int  value2 = 2;
const   int  value3 = 3;
m_request.Expect( a => a.GetParamValue(  "multiple"  ) ).IgnoreArguments().Repeat.Twice().Return( value3.ToString() );
m_page.Expect( a => a.IsPostBack ).Return(  true  );
72
// Act
m_defaultPage =  new   DefaultPage ();
m_defaultPage.SetTestableObjects( m_page );
m_defaultPage.Value1.Text = value1.ToString();
m_defaultPage.Value2.Text = value2.ToString();
m_defaultPage.Page_Load(  null ,  null  );
79
// Assert
Assert .IsTrue( m_defaultPage.Result.Text == ( (value1 + value2)*value3 ).ToString() );
}
```

Dieses Vorgehen hat uns nicht nur den seit langen gesuchten Weg zum Testen von Webanwendungen geebnet, sondern zwingt auch den Entwickler dazu, alle Funktionalitäten, die nicht in einer Webseite sondern in die dll-s gehören, auszulagern. Damit dürfte es auch der richtige Weg der Clean Code Developers für die Arbeit mit WebForms sein.

Was die Adapter-Klassen betrifft: inzwischen haben wir auch System.IO “adaptiert” und bald werden die anderen System-Klassen folgen, je nach Bedarf.  
[Download VS2008-Projekt](/assets/TestableWebForm.zip)


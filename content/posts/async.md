---
title: "Kommunikation mit dem Async-Pattern"
date: 2010-05-05
slug: async
original_url: "https://aztec-project.org/blog/aync.html"
archive_url: "https://web.archive.org/web/20251110231532/https://aztec-project.org/blog/aync.html"
author: "Thomas Christian"
categories: ["Architektur", "Pattern", "Tipps"]
---

Bevor ich anhand eines Beispiels zeige, wie man mit Hilfe des Async-Pattern ein asynchrone Kommunikation implementieren kann, möchte ich kurz beschreiben, wo der Unterschied zwischen der synchronen und der asynchronen Kommunikation liegt und wofür die asynchrone Kommunikation nützlich ist.

**Synchrone Kommunikation**

Bei der synchronen Kommunikation handelt es sich um eine Echtzeit-Kommunikation. Das bedeutet, dass Anfragen und Antworten jeweils vollständig nacheinander abgearbeitet werden. Kommuniziert ein Prozess mit einem Webserver synchron, so ist der Prozess solange blockiert, bis er die vollständige Antwort vom Webserver erhalten hat.

**Asynchrone Kommunikation**

Im Gegensatz zur synchronen Kommunikation handelt es sich bei der asynchronen Kommunikation nicht um eine Echtzeit-Kommunikation. Das bedeutet, dass bei der Kommunikation eines Prozesses mit einem Webserver der Prozess nicht blockiert. Der Prozess verschickt lediglich die Anfrage an den Webserver und kehrt danach sofort zur weiteren Prozessausführung zurück. Der Prozess geht dabei davon aus, dass die Anfrage an den Webservice korrekt gestellt wurde. Die Antwort wird dann zu einem unbestimmten Zeitpunkt vom Webservice geliefert, und zwar dann, wenn dieser mit der Abarbeitung der Anfrage fertig ist.

**Warum Asynchrone Kommunikation**

Asynchrone Kommunikation bietet sich in unterschiedlichsten Situationen an. So ist es z.B. sinnvoll, dass eine WinForms-Anwendung asynchron mit einem Webservice kommuniziert, da der Haupt-Thread der WinForm-Anwendung sonst so lange blockiert wäre, bis der Webservice die Antwort auf die Anfrage liefert. Die Folge wäre, dass im Titel der Anwendung stehen würde, dass die Anwendung nicht antwortet (s. Abbildung 1). Viele Benutzer denken dass es sich bei dieser Meldung um einen Fehler im Programm handelt und beenden das Programm fix über den Task-Manager. Dabei lag es nur an der etwas länger dauernden Kommunikation zwischen der WinForm-Anwendung und dem Webservice.

[<img src="/images/async/keineRueckmeldung.png" title="keineRueckmeldung" width="308" height="53" class="aligncenter size-full wp-image-973" alt="keineRueckmeldung"/>](/images/async/keineRueckmeldung.png) Abbildung 1

Ein weiterer Grund für eine asynchrone Kommunikation wäre, wenn eine Anwendung nur Nachrichten verschicken möchte und es im Grunde keine Rolle spielt, ob diese Nachricht korrekt verarbeitet wurde. Vorstellbar wäre hier Loggen von Aktionen. Mir wäre es jetzt egal, ob die Nachricht korrekt gespeichert wurde oder nicht. Ich will nur nicht, dass meine Anwendung, nur weil Daten geloggt werden müssen, langsamer wird. Es handelt sich ja bei den Log-Daten nicht um Informationen die für die Abarbeitung notwendig sind.

Ein weiterer Fall wäre z. B. das Skalieren von Datenbankabfragen. So könnten mehrere Threads gleichzeitig Daten von gleichen oder unterschiedlichen Datenbeständen abfragen um schnellere Antwortzeiten zu erhalten.

**Beispiel**

Um die asynchrone Kommunikation zu realisieren gibt es unterschiedliche Möglichkeiten. Ich habe mich allerdings für eine Event-Based-Variante entschieden. Der große Vorteil von einem Event-Based Async-Pattern liegt in meinen Augen darin, dass der Nutzer von asynchrone Methoden sich nicht wirklich mit Multithread-Umgebungen auskennen muss. Für den Nutzer ist es völlig transparent wie die Threads im Hintergrund erzeugt werden und wie die Synchronisation der einzelnen Thread funktioniert. Für den Nutzer ist es nur wichtig zu wissen, dass er eine Methode aufrufen kann die asynchron abläuft und somit nicht den erwarteten Rückgabewert besitzt wie die synchrone Methode und dass ein Event ausgelöst wird, wenn die Methode komplett abgearbeitet wurde und der erwartete Rückgabewert zur Verfügung steht.

Nun aber genug geredet, jetzt wird programmiert. Für das Beispiel habe ich mich für eine WinForm-Anwendung entschieden, die nichts anderes tut, als die eingegebene Zahl zu quadrieren. Diese Berechnung dauert aufgrund eines Thread.Sleep() zehn Sekunden, um eine verzögerte Ausführung zu simulieren. Die Berechnung habe ich dabei in eine extra Komponente ausgelagert, die eine Schnittstelle zur asynchronen Kommunikation bereitstellt. Dabei gilt es eine gewisse Namenskonvention einzuhalten. Neben der synchronen Methode „Calc“, wird die asynchrone Methode mit dem Zusatz „Async“ bezeichnet („CalcAsync“). Da das Async-Pattern Event-Based ist, muss ein Event bereitgestellt werden, welches ausgelöst wird, wenn die asynchrone Verarbeitung beendet wurde. Laut Namenskonvention muss solch ein Event „<Methodenname>Completed“ heißen. Mein Event heißt somit „CalcCompleted“.

Die Abbildung 2 zeigt die UI der Anwendung. Bei dem Drücken des „Run“-Buttons, soll die eingegebene Zahl asynchron quadriert werden und im Anschluss in das Feld „Ergebnis“ ausgegeben werden.

[<img src="/images/async/Form1.png" title="Form1" width="300" height="200" class="aligncenter size-full wp-image-980" alt="Form1"/>](/images/async/Form1.png)Abbildung 2

Der Code hinter der UI sieht folgendermaßen aus. Beim instanziieren des Forms, wird eine Instanz des Calculators erstellt und ein Delegate auf das „CalcCompleted“-Event registriert. Dieses Event wird aufgerufen sobald der Calculator mit der Berechnung fertig ist.

Bei dem Drücken des „Run“-Buttons, wird die Methode Calculator.CalcAsync(…) aufgerufen.

```
public   partial   class   Form1  :  Form  {
private   ICalculator  m_calculator;
public  Form1() {
InitializeComponent();
m_calculator =  new   Calculator ();
m_calculator.CalcCompleted += Calculator_CalcCompleted;
}

private   void  Run_Click( object  sender,  EventArgs  e) {
int  number;
if  ( Int32 .TryParse(txbEingabe.Text,  out  number)) {
m_calculator.CalcAsync(number, number);
}
}

void  Calculator_CalcCompleted( object  sender,  CalcEventArgs  eventArgs) {
lblCounter.Text = eventArgs.Result.ToString();
}
}
```

Sobald die Berechnung fertig ist, wird das CalcCompleted-Event ausgelöst und somit die Calculator\_CalcComplete-Methode aufgerufen und das Ergebnis der Berechnung in ein Label geschrieben. Der große Vorteil ist, dass man sich an dieser Stelle nicht mehr um die Synchronisierung der Threads kümmern muss, sodass man direkt auf das Label schreiben darf und es nicht zu einem threadübergreifenden Zugriff kommt.

Der Calculator sieht wie folgt aus:

```
public   interface   ICalculator  {
event   Calculator . CalcCompletedEventHandler  CalcCompleted;
int  Calc( int  number);
void  CalcAsync( int  number,  object  userState);
}

public   class   Calculator  :  ICalculator  {
public   delegate   void   CalcCompletedEventHandler ( object  sender,  CalcEventArgs  eventArgs);
public   event   CalcCompletedEventHandler  CalcCompleted;
private   AsyncOperation  m_asyncOperation;
private   bool  m_isRunning;

public   int  Calc( int  number) {
Thread .Sleep(10000);
return  number * number;
}

public   void  CalcAsync( int  number,  object  userState) {
lock  ( this ) {
if  (m_isRunning) {
throw   new   InvalidOperationException ( "Diese Operation wird bereits ausgeführt" );
}
m_isRunning =  true ;
m_asyncOperation =  AsyncOperationManager .CreateOperation(userState);
ThreadPool .QueueUserWorkItem(ExecuteCalc, number);
}
}
```

        .

        .

        .

```
}
```

Wie man im Interface des Calculator sieht, gibt es eine synchrone und eine asynchrone Methode für die Berechnung. Uns interessiert allerdings nur die asynchrone Methode. Das lock und die Prüfung auf m\_isRunning verhindern lediglich, dass die asynchrone Methode während ihrer Ausführung öfter aufgerufen wird. Das Wesentliche an dieser Methode ist der Aufruf von AsyncOperationManager.CreateOperation, denn dieser Aufruf stellt einen Synchronisationskontext bereit, der die Threads miteinander synchronisiert.  Für die eigentliche Berechnung wird sich über den ThreadPool ein neuer Thread besorgt, der sich dann um die Abarbeitung der ExecuteCalc in einem eigenen Thread kümmert.

```
public   class   Calculator  :  ICalculator  {
```

        .

        .

        .

```
private   void  ExecuteCalc( object  state) {
int  result = Calc(( int )state);
m_asyncOperation.PostOperationCompleted(CalcCompletedSuccessful, result);
}

private   void  CalcCompletedSuccessful( object  result) {
if  (CalcCompleted !=  null ) {
CalcCompleted( this ,  new   CalcEventArgs ( null ,  false , ( int )result, result));
}
}
}
public   class   CalcEventArgs  :  AsyncCompletedEventArgs  {
public  CalcEventArgs( Exception  error,  bool  cancelled,  int  result,  object  userState)
:  base (error, cancelled, userState) {
Result = result;
}
public   int  Result {  get ;  private   set ; }
}
```

Sobald die Berechnung abgeschlossen ist, wird der Thread mit dem MainThread über den Aufruf von PostOperationCompleted synchronisiert und das CalcCompleted-Event ausgelöst und das Ergebnis in das Label geschrieben (s. o.).

6 public partial class Form1 : Form {

7 private ICalculator m\_calculator;

8 public Form1() {

9 InitializeComponent();

10 m\_calculator = new Calculator();

11 m\_calculator.CalcCompleted += Calculator\_CalcCompleted;

12 }

13

14 private void Run\_Click(object sender, EventArgs e) {

15 int number;

16 if (Int32.TryParse(txbEingabe.Text, out number)) {

17 m\_calculator.CalcAsync(number, number);

18 }

19 }

20

21 void Calculator\_CalcCompleted(object sender, CalcEventArgs eventArgs) {

22 lblCounter.Text = eventArgs.UserState.ToString();

23 }

24 }

## Kommentare (Archiv)

1. <img src="/images/async/3e7b6cb163ea9cc8549abcb8b5a03e2e.jpeg" width="32" height="32" class="avatar avatar-32 photo" alt="Avatar"/> **[Ralf Westphal](http://ralfw.blogspot.com/)**

   [Mai 6, 2010 um 10:34 am](/posts/async/)

   Statt eines Kommentars ein Blogartikel, der eine alternative Implementation mit Event-Based Components zeigt:

   <http://ralfw.blogspot.com/2010/05/asynchrone-kommunikation-mit-ebcs-statt.html>
2. **[build broken » Asynchrone Kommunikation mit dem Async-Pattern (Refactored)](/posts/async-refactored/)**

   [Mai 6, 2010 um 2:37 pm](/posts/async/)

   [...] « Asynchrone Kommunikation mit dem Async-Pattern Mai 06 2010 [...]
3. **[Tweets that mention build broken » Asynchrone Kommunikation mit dem Async-Pattern -- Topsy.com](/posts/async/)**

   [Mai 6, 2010 um 9:17 pm](/posts/async/)

   [...] This post was mentioned on Twitter by .NET German Bloggers. .NET German Bloggers said: Asynchrone Kommunikation mit dem Async-Pattern: Bevor ich anhand eines Beispiels zeige, wie man mit Hilfe des Asyn… <http://bit.ly/dfCLjB> [...]

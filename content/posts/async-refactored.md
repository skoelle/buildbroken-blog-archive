---
title: "Async-Pattern (Refactored)"
date: 2010-05-06
slug: async-refactored
original_url: "https://aztec-project.org/blog/async-refactored.html"
archive_url: "https://web.archive.org/web/20250114134342/https://aztec-project.org/blog/async-refactored.html"
author: "Thomas Christian"
categories: ["Architektur", "Pattern", "Tipps"]
---

Nach dem ich meinen vorherigen Artikel zum Thema [“Asynchrone Kommunikation mit dem Async-Pattern”](/posts/async/) vorgestellt hatte, hat Ralf Westphal auf seinem Blog [“One Man Think Tank Gedanken”](http://ralfw.blogspot.com/2010/05/asynchrone-kommunikation-mit-ebcs-statt.html) das Vorgehen zur Implementierung einer asynchronen Kommunikation mit Hilfe von Event-Based-Components vorgestellt, welches eine sehr gute Alternative zum Async-Pattern ist. Seinen Eintrag nehme ich zum Anlass, um meine Beispiel-Implementierung des Async-Pattern zu refaktorisieren, um eine bessere Trennung der Verantwortlichkeiten und somit eine bessere Lesbarkeit zu erreichen.

In das Form wird die Abhängigkeit “CalcProxy” injected.

static void Main()

{

CalcProxy calcProxy = new CalcProxy(new Calculator());

Application.EnableVisualStyles();

Application.SetCompatibleTextRenderingDefault(false);

Application.Run(new Form1(calcProxy));

}

Im Gegensatz zur vorherigen Version wird in der Form nun nicht mehr der Calculator direkt erzeugt und verwendet, sondern auf den injekteten CalcProxy zugegriffen.

public partial class Form1 : Form {

private readonly ICalcProxy m\_calcProxy;

public Form1(ICalcProxy calcProxy) {

        InitializeComponent();

        m\_calcProxy = calcProxy;

        m\_calcProxy.CalcCompleted += CalculatorCalcCompleted;

    }

private void Run\_Click(object sender, EventArgs e) {

int number;

if (Int32.TryParse(txbEingabe.Text, out number)) {

            m\_calcProxy.CalcAsync(number, number);

        }

    }

void CalculatorCalcCompleted(object sender, CalcEventArgs eventArgs) {

        lblCounter.Text = eventArgs.UserState.ToString();

    }

}

Der CalcProxy wiederum bekommt die Abhängigkeit zum Calculator injected und stellt für die Calculator.Calc-Methode sowohl eine synchrone als auch eine asynchrone Methode zur Verfügung.

public class CalcProxy : ICalcProxy {

private readonly ICalculator m\_calculator;

public event CalcCompletedEventHandler CalcCompleted;

private AsyncOperation m\_asyncOperation;

private bool m\_isRunning;

public CalcProxy(ICalculator calculator) {

        m\_calculator = calculator;

    }

public int Calc(int number) {

return m\_calculator.Calc(number);

    }

public void CalcAsync(int number, object userState) {

lock (this) {

if (m\_isRunning) {

throw new InvalidOperationException("Diese Operation wird bereits ausgeführt");

            }

            m\_isRunning = true;

            m\_asyncOperation = AsyncOperationManager.CreateOperation(userState);

ThreadPool.QueueUserWorkItem(ExecuteCalc, number);

        }

    }

private void ExecuteCalc(object state) {

var result = Calc((int)state);

        m\_asyncOperation.PostOperationCompleted(CalcCompletedSuccessful, result);

    }

private void CalcCompletedSuccessful(object result) {

if (CalcCompleted != null) {

            CalcCompleted(this, new CalcEventArgs(null, false, (int)result, result));

        }

    }

}

Nun enthält der Calculator nur noch die Methode die für den Calculator notwendig ist, nämlich die Calc-Methode.

public class Calculator : ICalculator {

public int Calc(int number) {

Thread.Sleep(10000);

return number \* number;

    }

}

## Kommentare (Archiv)

1. <img src="/images/async-refactored/3e7b6cb163ea9cc8549abcb8b5a03e2e.jpeg" width="32" height="32" class="avatar avatar-32 photo" alt="Avatar"/> **[Ralf Westphal](http://ralfw.blogspot.com/)**

   [Mai 6, 2010 um 3:02 pm](/posts/async-refactored/)

   Freut mich, dass du meinen Blogartikel hilfreich fandest. Du hast jetzt den Async-Infrastrukturcode herausgezogen. Die Businesslogik ist wieder deutlich sichtbar. Super.

   Aber ich frage mich: Was machst du, wenn du drei verschiedene Klassen wir Kalkulator in der Weise async machen willst? Willst du dann drei Proxies basteln?

   -Ralf
2. **[Tweets that mention build broken » Asynchrone Kommunikation mit dem Async-Pattern (Refactored) -- Topsy.com](/posts/async-refactored/)**

   [Mai 6, 2010 um 4:38 pm](/posts/async-refactored/)

   [...] This post was mentioned on Twitter by .NET German Bloggers, DeveloperBlogs. DeveloperBlogs said: Asynchrone Kommunikation mit dem Async-Pattern (Refactored): Nach dem ich meinen vorherigen Artikel zum Thema “Asy… <http://bit.ly/9eV2kr> [...]
3. **[Rainer Hilmer](http://dotnet-forum.de/blogs/rainerhilmer/default.aspx)**

   [Juli 24, 2010 um 1:56 pm](/posts/async-refactored/)

   Hallo,  
   ich hab ein paar Fragen zu deinem Demo.

   1. Warum benutzt du immer noch m\_ als Prefix für lokale Objekte?

   2. Warum benutzt du englische UND deutsche Membernamen?

   3. Warum hat der CalcEventArgs-Constructor vier Parameter, obwohl de Facto nur eines im Demo benutzt wird? Ist das YAGNI oder spielt das in anderen Szenarien eine Rolle? Wofür wären dann die anderen Parameter gedacht? Kannst du das mal erläutern?

   4. Wo ist der ganze Rest von dem Code?
4. **Thomas Christian**

   [Juli 27, 2010 um 8:41 am](/posts/async-refactored/)

   Hallo,

   um deine Fragen zu beantworten:

   zu 1) Das ist halt alles eine Frage des Geschmacks. Ich persönlich mag es, wenn ich auf dem ersten Blick erkennen kann, dass es sich um eine globale Variable handelt.  
   zu 2) Ich gehe mal davon aus, dass du auf das txtEingabe anspielst. Naja, abgesehen, von den Controls, sind alle Variablen englisch. Die Controls sind das Frontend und dort wollte ich eigentlich deutsch bleiben. In der eile ist mir wohl der lblCounter als englischer Name durchgerutscht.  
   zu 3) Das liegt daran, dass CalcEventArgs von AsyncCompletedEventArgs ableitet und die zusätzlichen Parameter benötigt.  
   zu 4) Ich weiß zwar nicht genau welchen Code du vermisst, aber ich denke mal du meinst CalcEventArgs. Bei diesem Blogeintrag handelt es sich um eine refaktorisierte Version meines vorherigen Eintrags. Dort ist auch das CalcEventArgs vorhanden. `/posts/async/`

   Ich hoffe ich konnte dir die Fragen ausreichend beantworten.

   Gruß Tom

# Schulungsanmeldung

Aktuellere Information in der .odp

## Beschreibung

Wir wollen den JuLeis aus Baden-Württemberg einfacher, fairer und weniger arbeitsintensiv für die GS
einen Platz in einer Schulung zuweisen, die sie mögen.

## Bisher

Die JDAV BaWü ordanisiert zwischen 50 udn 100 Schulungen im Jahr.
Jede Schulung hat circa 12 Plätze.
Circa 700 JuLeis nehmen an diesen Schulungen teil.

First-Come-First-Serve.
Anschließend per Hand sortieren, wer welche Präferenzen hat, wer aus Baden-Württemberg kommt und wer nicht
und ggf. andere Beweggründe, wie bspw. tauschen mit anderer Person.

Entgegen mancher Behauptung weiß man auch jetzt nicht direkt,
ob man einen Platz in einer Schulung bekommen hat oder nicht
- insbesondere nicht, während man die Schulungen zum ersten mal durchgeht und sich die interessantesten Schulungen raussucht.

## Abgrenzung

First-Come-First-Serve brauchen wir auf jeden Fall - als das Prinzip, welches nach einem eventuellen anderen Prozess beginnt.

Es geht nicht darum, einen komplexen Prozess zu erschaffen,
sondern darum, den wie man die GS dabei unterstützen kann, den an sich komplexen Prozess leichter, schneller, transparenter und fairer zu bearbeiten.

Um immer wieder auf das aktuelle System (First-Come-First-Serve) zurückwechseln zu können,
würde sich bspw. follgender Arbeitsablauf anbieten:

1. GS- oder LJL-Mensch drückt "Zulegung berechnen"
2. Odoo generiert eine vorschau bspw. in Odoo oder als Excel
3. GS- oder LJL-Mensch kann auf bestätigen drücken  (oder auch nicht)
4. Wenn Bestätigt wurde, wird der Vorschlag umgesetzt und den JuLeis angezeigt

Ich habe mir keine Gedanken dazu gemacht, ob die JuLeis, die keinen Platz bekommen haben,
auf die Wartelisten gesetzt werden sollen oder nur eine Mail bekommen sollen.

## JDAV BaWü Regeln

- ein JuLeis aus BaWü haben immer Vorrang vor Juleis, die nicht aus BaWü kommen
- in der ersten Phase bekommen alle JuLeis max. einen Platz
- möglichst viele JuLeis sollen einen Platz bekommen

## JuLei-Präferenzen

Umso weniger genau die Präferenzen der JuLeis abgefragt werden,
umso mehr Spielraum hat die JDAV BaWü, um allen JuLeis einen guten Platz zu geben.

Für mich ist der Sweet-Spot, dass alle JuLeis
beliebig viele Schulungen in 2, 3 oder mehr Kategorien einteilen, bspw:

- "Lieblingsschulungen"
- "bevorzugte Schulungen"
- "Notlösungen"

Ich freue mich über bessere Namen:
das "Lieblingsschulung" höhergestellt ist als "bevorzugte Schulungen" wird vllt nicht ganz klar
und "Notlösung" klingt sehr abwertend - insbesondere wenn die Wünsche ggf. Mal den Teamerinnen gezeigt werden.

Es darf keine negativen Effekte geben, wenn JuLeis mehrere Schulungen zur gleichen Kategorie oder zu anderen Kategorien hinzufügen.

Daher werden die Zuweisungen bspw. in sechs getrennten Schritten vorgenommen:

1. Die Lieblingsschulungen der JuLeis aus BaWü
2. Die verbleibenden Plätze auf die "bevorzugten Schulungen" der JuLeis aus BaWü
3. Die Notlösungen der JuLeis aus BaWü
4. Die Lieblingsschulungen der JuLeis nicht aus BaWü
5. Die bevorzugten Schulungen der JuLeis nicht aus BaWü
6. Die Notlösungen der JuLeis nacht aus BaWü

Technisch macht es keinen Unterschied, wieviele Kategorien es sind, wie diese heißen und
wieviele Schulungen jeweils in der Kategorie sind - auch nicht, ob JuLeis unterschiedlich viele Schulungen angeben.

Meines Erachtens ist das die Lösung, bei der die JuLeis am besten ihre Präferenzen mitteilen können ohne nervige Einschränkungen und
die JDAV BaWü dennoch einigermaßen frei zuordnen kann.

## Quoten

Es gibt bereits ein paar Quoten und es werden sich auch welche gewünscht,
bspw. eine Geschlechterquote oder das maximal 3 JuLeis einer Schulung aus der gleichen Sektion stammen dürfen.

Im Gegensatz zu der Regel, das JuLeis aus BaWü immer Vorrang haben müssen,
weil wir ansonsten ggf. keine Gelder vom Land bekommen,
sind wir zu diesen Quoten meines Wissens nach nicht verpflichtet.

Daher ist meine Empfehlung diese Quoten erstmal nur mitzudenken und nicht zu implementieren,
weil es die Implementierung unverhältnissmäßig komplex macht,
man danach an unverfälschten Daten gezielter nachbessern kann
und kritische Fragen damit erstmal vertagt werden (sodass sie auch nicht das große ganze infrage stellen).

Kritische Fragen sind bspw. ob JuLei wegen einer Quote in Schulungen gesteckt werden können,
obwohl sie eine andere Schulung lieber hätten.
Oder ob JuLeis andere JuLeis verdrängen dürfen, obwohl
es eine Lösung gibt, bei der alle einen Platz bekommen, mit dem sie zufrieden sind.

## Lösungen

### Vorschlag 0: Per PDF und per Hand

Die JuLeis geben weiterhin PDFs ab, die die GS von Hand durchgeht.

### Vorschlag 1: Random

Aus allen, die in die Schulung wollen, werden zufällig welche ausgewählt.

Schnell und Simple

Falls gewünscht kann man in Zukunft erst nach Quoten auswählen/sortieren.
Dabei kann man so weit gehen, das man sicher gehen kann, dass alle Quoten immer erfüllt sind.

### Vorschlag 2: Optimale Lösuung

Mithilfe von
[Maximum Flow](https://en.wikipedia.org/wiki/Maximum_flow_problem#Maximum_cardinality_bipartite_matching)
wird die optimale Zuordnung berechnet.
Klingt sehr kompliziert, ist jedoch überraschend einfach und robust implementierbar (circa 20 Zeilen).

Sehr elegante Lösung, mein Favorit :)

Falls gewünscht kann man in Zukunft aus den optimalen Lösungen die auswählen, die die etwaige Quoten am besten erfüllt.
Dabei werden die Quoten jedoch nur sehr nachrangig betrachtet.

Der Wechsel von Vorschlag 1 zu diesem Vorschlag geht sehr einfach,
weil beides die gleiche digitale Infrastruktur braucht (JuLei Abfrage, Vorschau zeigen, Zuweisung umsetzen...).

## Zeitplan

Über die genauen Zeiträume kann man auf jeden Fall noch reden,
dass wäre ein erster Vorschlag.

- 4 Wochen: Schulungen werden sichtbar geschalten und JuLeis geben ihre Präferenzen an
- 1 Woche: Optimale Belegung wird berechnet, geprüft und umgesetzt oder es wird kommuniziert, dass es nicht geklappt hat und am dd.mm.yyyy wie früher First-Come-First-Serve startet
- Danach: First-Come-First-Serve

## Kommunikation zu den JuLeis

Die folgenden Infos auf jeder Schulungsseite könnten zur Kommmunikation reichen.
Ansonsten sollte man das in den Folgejahren nochmal anpassen.

Hinweise:

- "Du kannst so viele Schulungen zu Lieblingsschulungen, bevorzugte Schulungen und Notlösungen hinzufügenen, wie du möchtest."
- "In deinem Profil kannst du das wieder rückgängig machen."
- "Am dd.mm.yyyy bekommst du mitgeteilt, in welche Schulung du reingekommen bist."

Drei Knöpfe:

- "Zu Lieblingsschulungen hinzufügen"
- "Zu bevorzugte Schulungen hinzufügen"
- "Zu Notlösungen hinzufügen"

Ich freue mich über bessere Namen:
das "Lieblingsschulung" höhergestellt ist als "bevorzugte Schulungen" wird vllt nicht ganz klar
und "Notlösung" klingt sehr abwertend - insbesondere wenn die Wünsche ggf. Mal den Teamerinnen gezeigt werden.


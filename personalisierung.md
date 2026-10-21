# ChatGPT – Personalisierung

Sicherung der persönlichen Einstellungen für die Wiederherstellung in einem anderen ChatGPT-Account.

## Benutzerdefinierte Anweisungen

Ich entwickle wartbare Java-Software nach Clean Code- und Architekturprinzipien. Bitte beachte bei allen Antworten folgende Leitlinien:

- Strukturiere Code strikt nach den SOLID-Prinzipien (SRP, OCP, LSP, ISP, DIP).
- Verwende intentionalen Code: Der Code soll die fachliche Absicht ausdrücken, nicht nur technische Abläufe. Namen sollen sprechend und erklärend sein.
- Bevorzuge kurze, fokussierte Methoden mit präzisem Methodennamen, wie von Uncle Bob empfohlen. Eine Methode = eine Aufgabe.
- Arbeite konsequent schichtengerecht (z. B. UI → UseCase → Domain → Infrastruktur). Vermeide Verletzungen dieser Trennung.
- Gib mir immer vollständige Methoden oder kleine, austauschbare Klassen – kein diffartiger oder fragmentierter Code.
- Bevorzuge Design Patterns (GoF), wo sie Modularität, Testbarkeit oder Erweiterbarkeit fördern (z. B. Observer, Strategy, Command).
- Verwende lose Kopplung durch Interfaces, Events oder das Observer-Pattern, keine direkte Instanzabhängigkeit.
- Strukturiere Code wie ein Lego-System: kombinierbar, verständlich, wiederverwendbar. Jeder Teil sollte einzeln funktionieren können.
- Wenn du bestehenden Code änderst, refactore ihn automatisch nach diesen Prinzipien – nicht nur anpassen, sondern verbessern.
- Erkläre Designentscheidungen gern kurz mit einem Satz, aber zeige mir den vollständigen, übernehmbaren Code.

## Über mich

Ich habe Erfahrung als Java-Backendentwickler. Außerdem verwende ich meist das Spring-Framework und Gradle. Für UIs verwende ich Swing, JavaFx und React.

Beruflich habe ich die Funktion als Produktverantwortlicher inne.

Ich Programmiere nur in Java 8! Daher bitte keine Sprachfeatures wie `var`, `record` oder `List.of()` vorschlagen, die es nicht in Java 8 gibt.

Auf Deutsch, auch wenn ich andere Sprachen eingebe. Kommentare in Sourcode, den ChatGPT ausgibt, sollen hingegen IMMER englisch und im imperativen Stil (niemals Sie oder DU) sein.

Ich möchte grundsätzlich geduzt werden!

Damit Du meine Gradle Projekte in der Sandbox starten kannst, braucht es einige Vorbereitung:

1. `chatgpt-build.sh` ins Repo legen
2. Gradle immer über `bash "$ROOT_DIR/gradlew"` starten
3. `GRADLE_USER_HOME` auf `"$ROOT_DIR/.chatgpt/gradle-home"` setzen
4. in GitHub Actions mit Internet einmal `clean build` / `refresh-dependencies` ausführen
5. danach `.chatgpt/gradle-home` ins Release-ZIP packen
6. Lock-/Daemon-/Worker-Dateien aus dem Cache entfernen
7. ZIP in ein temporäres Verzeichnis außerhalb von `build/` entpacken
8. `gradlew` absichtlich `chmod -x` setzen
9. `bash chatgpt-build.sh` aus der frischen Extraktion testen
10. erst dann das Rolling-Release-Asset löschen und neu hochladen

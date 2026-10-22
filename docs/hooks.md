---
layout: default
title: Browser-Hook-Spezifikation
permalink: hooks.html
---

# Browser-Hook-Spezifikation

## Zweck und Abgrenzung

Diese Spezifikation beschreibt, wie ein Browser Event Hub Aktivitäten der ChatGPT-Weboberfläche erkennt und in einen stabilen, eigenen Event-Vertrag überführt.

- **OpenAPI** beschreibt HTTP-Aufrufe, Methoden, Parameter und HTTP-Responses.
- **AsyncAPI** beschreibt Nachrichtenvarianten innerhalb der Chat- und Datei-Streams.
- **Diese Hook-Spezifikation** beschreibt die lokale Instrumentierung des Browsers, DOM-Änderungen, Navigation und die Normalisierung der erkannten Ereignisse.
- Das [Schema für normalisierte Events](./schemas/normalized-event.schema.json) definiert den Event-Hub-Vertrag.

## Instrumentierungspunkte

### 1. `fetch`

Erfasse Request-Start, Response-Header, Stream-Nachrichten, Abschluss und Fehler.

- Bewahre Signatur, `this`, Argumente, Rückgabewert, Promise-Semantik und Fehlerverhalten des Originals.
- Erzeuge eine Request-ID und verwende sie für alle zugehörigen Events.
- Lies Streamdaten nur über einen geklonten Response-Body und begrenze Pufferung und Parsing-Aufwand. Verändere nicht den Body, den die Anwendung konsumiert.
- Behandle Abbruch, Netzwerkfehler, ungültige JSON-Daten und unvollständige Streams als getrennte Fälle.
- Fange Fehler des Hooks intern ab; ein Hook-Fehler darf den eigentlichen Request nicht scheitern lassen.

### 2. `XMLHttpRequest`

Instrumentiere `open`, `send`, `setRequestHeader` und die relevanten Lifecycle-Ereignisse, ohne das sichtbare Verhalten des ursprünglichen XHR-Objekts zu verändern.

- Ordne `readystatechange`, `load`, `loadend`, `error`, `abort` und `timeout` dem Request zu.
- Lies den Response-Body nur, wenn der Zustand und der Response-Typ dies zulassen.
- Vermeide doppelte normalisierte Events, falls eine Anwendung denselben fachlichen Vorgang über mehrere Instrumentierungspunkte sichtbar macht.

### 3. Stream-Parsing

Unterscheide Transport-Framing und Payload-Schema:

- `POST /backend-api/f/conversation`: Content-Type: `text/event-stream`. `delta` und `delta_encoding` sind explizite SSE-Event-Namen. Weitere Ereignisse werden überwiegend über das JSON-Feld `type` erkannt; `[DONE]` ist eine Abschlussmarkierung.
- `POST /backend-api/files/process_upload_stream`: Content-Type: `text/event-stream`; Body-Framing: zeilenweise getrennte JSON-Objekte.
- Leite keine vollständigen Payload-Schemas aus bloßen Event-Namen ab. Erhalte unbekannte Felder und protokolliere Parsefehler ohne den Originalstream zu blockieren.

### 4. WebSocket-Lifecycle

Erfasse, soweit erforderlich und zulässig, `open`, `message`, `error` und `close`. Dokumentiere Richtung, Zeitpunkt, Frame-Größe und Verbindungskorrelation nur dann, wenn diese Informationen tatsächlich erfasst werden.

WebSocket-Handshakes: vorhanden. Nachrichtenframes: keine.

### 5. Navigation

Erfasse `popstate` und `hashchange`. Falls `history.pushState` und `history.replaceState` instrumentiert werden, rufe die Originalfunktion mit identischem Kontext und denselben Argumenten auf und veröffentliche erst danach das normalisierte Navigationsevent.

### 6. DOM-Ereignisse

Verwende gezielte Event-Listener und `MutationObserver` zur Erfassung von DOM-Änderungen. Bevorzuge stabile Rollen, zugängliche Namen und klar definierte Selektoren gegenüber fragilen CSS-Klassen.

- Scanne nicht fortlaufend den vollständigen DOM-Baum.
- Veröffentliche keine kompletten DOM-Snapshots.
- Behandle UI-Signale nicht als Beweis für einen erfolgreichen Backend-Vorgang.
- Vermeide doppelte Ereignisse durch Debouncing oder zustandsbasierte Deduplizierung, wo es fachlich gerechtfertigt ist.

## Normalisierte Events

Alle Events verwenden das äußere Schema `schemas/normalized-event.schema.json`.

| Event-Typ | Auslöser | Inhalt |
|---|---|---|
| `network.request.started` | `fetch` / XHR startet | Methode, bereinigter Pfad, Request-ID |
| `network.response.headers` | Response-Header verfügbar | Status, bereinigter Content-Type |
| `network.response.completed` | Response abgeschlossen | Dauer und Ergebnis-Metadaten |
| `network.request.failed` | Request scheitert oder wird abgebrochen | Fehlerkategorie, keine Credentials |
| `conversation.stream.event` | Chat-Stream-Nachricht empfangen | Event-Name oder `type`, allowlist-basierte Payload |
| `conversation.stream.completed` | `message_stream_complete` oder `[DONE]` erkannt | Abschlussart und Request-ID |
| `file.processing.progress` | Datei-Verarbeitungsereignis erkannt | Ereignisname, Fortschritt sofern vorhanden |
| `websocket.opened` | WebSocket-Verbindung geöffnet | bereinigter Endpunkt und Verbindungs-ID |
| `websocket.message` | Frame empfangen oder gesendet | Richtung und Payload nur nach expliziter Freigabe |
| `websocket.closed` | Verbindung geschlossen | Close-Code und Verbindungs-ID |
| `navigation.changed` | URL oder History-Zustand geändert | bereinigter Pfad |
| `dom.action` | Definierte UI-Aktion erkannt | Aktionstyp und minimal nötige Metadaten |
| `hook.error` | Instrumentierung oder Parsing scheitert | Hook-Punkt und Fehlerkategorie |

Payload-Felder bleiben ereignisspezifisch. Benenne Felder nur bei eindeutigem fachlichem Mapping um. Füge keine vermeintlich universellen Felder hinzu, nur weil ein Beispiel sie enthält.

## Reihenfolge und Korrelation

1. Vergib für jedes Event eine eindeutige `eventId` und eine monoton steigende `sequence` innerhalb einer Event-Hub-Instanz.
2. Verwende `requestId` für den Request und alle daraus abgeleiteten Stream-Events.
3. Bewahre die Empfangsreihenfolge der Frames innerhalb eines Streams.
4. Erzwinge keine globale Kausalreihenfolge zwischen unabhängigen Requests, DOM-Ereignissen und Telemetrie. Zeitstempel allein beweisen keine Kausalität.
5. Ein UI-Ereignis wie „Nachricht angezeigt“ ist kein Ersatz für einen bestätigten HTTP- oder Stream-Abschluss.

## Fehler, Lebenszyklus und Leistung

- Installiere Hooks idempotent und gib eine Abmeldefunktion zurück.
- Stelle beim Deaktivieren die ursprünglichen Browserfunktionen wieder her, sofern keine weitere Instrumentierung sie ersetzt hat.
- Lasse Hook-Ausnahmen nicht in die Anwendung durchschlagen.
- Begrenze Stream-Puffer, DOM-Listener und Event-Queues.
- Kennzeichne unvollständige oder nicht parsebare Nachrichten; verwirf nicht stillschweigend den gesamten Stream.
- Unterstütze einen expliziten Deaktivierungsmodus und verhindere mehrfach installierte Wrapper.

## Datenschutz und Veröffentlichung

- Speichere keine Cookies, Authorization-Header, Session- oder Resume-Tokens, signierten URL-Parameter, Rohtranskripte oder Audio-Asset-URLs.
- Entferne sensible Query-Parameter und IDs aus Logs, sofern sie nicht zwingend für die lokale Korrelation benötigt werden.
- Erfasse Nachrichtentext nur, wenn die Integration ihn ausdrücklich benötigt, und behandle ihn als vertraulichen Inhalt.
- Sende keine Nutzdaten an externe Validatoren oder Telemetriedienste.

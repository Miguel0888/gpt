---
layout: default
title: HAR-Beobachtungen und Evidenz
permalink: observations.html
---

# HAR-Beobachtungen und Evidenz

Diese Seite trennt direkt beobachtete Tatsachen von abgeleiteten oder noch unbekannten Details. Die Zahlen beziehen sich ausschließlich auf die bereitgestellten und bereinigten HAR-Auswertungen; sie sind keine vollständige Inventarisierung aller ChatGPT-Endpunkte.

## Evidenzklassen

- **Beobachtet:** im HAR oder in der bereinigten Mitschnittauswertung enthalten.
- **Abgeleitet:** Normalisierung oder technische Interpretation einer Beobachtung.
- **Unbekannt:** durch den Mitschnitt nicht belegt; keine Struktur oder Semantik hinzuerfinden.

## Chat-Antwortstream

| Merkmal | Beobachtung | Status |
|---|---|---|
| HTTP-Endpunkt | `POST /backend-api/f/conversation` | Beobachtet |
| Response Content-Type | `text/event-stream` | Beobachtet |
| Vollständige Antwortstreams | 4 | Beobachtet |
| Explizite SSE-Event-Namen | `delta`, `delta_encoding` | Beobachtet |
| `delta`-Ereignisse | 53 über die vier vollständigen Streams | Beobachtet |
| `delta_encoding`-Ereignisse | 4; der Wert `v1` wurde berichtet | Beobachtet |
| JSON-`type`-Werte | `resume_conversation_token`, `input_message`, `title_generation`, `message_marker`, `server_ste_metadata`, `message_stream_complete`, `conversation_detail_metadata` | Beobachtet |
| `message_marker` | 16 Ereignisse; berichtete Markerwerte: `cot_token`, `user_visible_token`, `final_channel_token`, `last_token` | Beobachtet |
| Abschluss | `[DONE]` in allen vier vollständigen Streams | Beobachtet |
| Vollständige Feldschemas aller Event-Payloads | Nicht durch die bereinigte Zusammenfassung belegt | Unbekannt |

`delta` und `delta_encoding` sind explizite SSE-Event-Namen. Die übrigen aufgeführten Ereignisse werden überwiegend über das JSON-Feld `type` unterschieden. Der konkrete Feldname, der die Markerwerte trägt, wird nicht behauptet. Siehe [AsyncAPI](./asyncapi.html) und [OpenAPI](./openapi.yaml).

## Datei-Verarbeitungsstream

| Merkmal | Beobachtung | Status |
|---|---|---|
| HTTP-Endpunkt | `POST /backend-api/files/process_upload_stream` | Beobachtet |
| Response Content-Type | `text/event-stream` | Beobachtet |
| Body-Framing | Zeilenweise getrennte JSON-Objekte statt üblicher SSE-`data:`-Frames | Beobachtet |
| Ereignisse | `file.processing.started`, `file.processing.file_ready`, `file.indexing.completed`, `file.processing.completed` | Beobachtet |
| Fortschritt | 0, 20 und 100 für einige Ereignisse; kein Prozentwert bei `file.indexing.completed` | Beobachtet |
| Vollständiges, dauerhaftes Schema | Noch nicht belegt; die aktuelle JSON-Schema-Definition lässt unbekannte Felder zu | Offen |

Das Framing ist ein wichtiger Prüfpunkt: Der HTTP-Content-Type allein beweist nicht, dass der Body dem üblichen SSE-Framing folgt. Der aktuelle Adaptervorschlag verwendet deshalb einen eigenen Parser für zeilenweise JSON-Objekte.

## WebSockets

| Host / Pfad | Beobachtung | Status |
|---|---|---|
| `codex-cloud-backend.chatgpt.com/` | 1 Handshake mit Status `101` | Beobachtet |
| `chatgpt.com/backend-api/dictation/stream` | WebSocket-Handshake; Query-Parameter `dictation_surface` beobachtet | Beobachtet |
| `ws.chatgpt.com/p33/ws/user/{userId}` | 3 Handshakes mit Status `101` | Beobachtet |
| WebSocket-Nachrichtenframes und Payloads | Nicht in den HAR-Aufzeichnungen enthalten | Unbekannt |

OpenAPI beschreibt hier ausschließlich den HTTP-Upgrade-Handshake. Die AsyncAPI-Datei enthält absichtlich keine WebSocket-Nachrichtenkanäle, solange keine Frames vorliegen, aus denen Nachrichtenformat und Richtung belastbar abgeleitet werden können.

## Realtime / SDP-Signalisierung

- `POST /realtime/wm`: 8 beobachtete Aufrufe mit Status `201`.
- Request und Response verwenden `application/sdp`.
- Das ist eine HTTP-Signalisierung zur Aushandlung einer Realtime-Sitzung; sie belegt nicht das Format der späteren WebRTC-Medien- oder Datenkanäle.
- Die HTTP-Signalisierung bleibt in [OpenAPI](./openapi.yaml). Nicht beobachtete Datenkanal-Nachrichten werden nicht als AsyncAPI-Payloads erfunden.

## Grenzen und Aktualisierung

- Die OpenAPI-Inventarisierung umfasst 69 normalisierte HTTP-Operation-Muster und 245 zugehörige Request-Einträge aus den bereitgestellten Inventaren.
- Die Beobachtungen beziehen sich auf die HAR-Aufzeichnungen vom 16. und 22. Oktober 2026.
- Dynamische IDs werden normalisiert. Authentifizierungswerte, signierte URLs und Nachrichteninhalte gehören nicht in das Repository.
- Interne Endpunkte können sich ohne Vorankündigung ändern. Prüfe bei neuen Mitschnitten zuerst die Header, das tatsächliche Body-Framing und die vorhandenen Payloads, bevor Schemas erweitert werden.

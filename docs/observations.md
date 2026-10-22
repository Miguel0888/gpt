---
layout: default
title: HAR-Beobachtungen
permalink: observations.html
---

# HAR-Beobachtungen

## Chat-Antwortstream

| Merkmal | Beobachtung | Status |
|---|---|---|
| HTTP-Endpunkt | `POST /backend-api/f/conversation` | Beobachtet |
| Response Content-Type | `text/event-stream` | Beobachtet |
| Vollständige Antwortstreams | 4 | Beobachtet |
| Explizite SSE-Event-Namen | `delta`, `delta_encoding` | Beobachtet |
| `delta`-Ereignisse | 53 über vier Streams | Beobachtet |
| `delta_encoding`-Ereignisse | 4; Wert `v1` | Beobachtet |
| JSON-`type`-Werte | `resume_conversation_token`, `input_message`, `title_generation`, `message_marker`, `server_ste_metadata`, `message_stream_complete`, `conversation_detail_metadata` | Beobachtet |
| `message_marker` | 16 Ereignisse; Markerwerte `cot_token`, `user_visible_token`, `final_channel_token`, `last_token` | Beobachtet |
| Abschluss | `[DONE]` in allen vier vollständigen Streams | Beobachtet |
| Vollständige Feldschemas | Nicht vollständig erfasst | Unbekannt |

## Datei-Verarbeitungsstream

| Merkmal | Beobachtung | Status |
|---|---|---|
| HTTP-Endpunkt | `POST /backend-api/files/process_upload_stream` | Beobachtet |
| Response Content-Type | `text/event-stream` | Beobachtet |
| Body-Framing | Zeilenweise getrennte JSON-Objekte statt SSE-`data:`-Frames | Beobachtet |
| Ereignisse | `file.processing.started`, `file.processing.file_ready`, `file.indexing.completed`, `file.processing.completed` | Beobachtet |
| Fortschritt | 0, 20 und 100 bei einigen Ereignissen; kein Wert bei `file.indexing.completed` | Beobachtet |

## WebSockets

| Host / Pfad | Beobachtung | Status |
|---|---|---|
| `codex-cloud-backend.chatgpt.com/` | 1 Handshake mit Status `101` | Beobachtet |
| `chatgpt.com/backend-api/dictation/stream` | WebSocket-Handshake; Query-Parameter `dictation_surface` | Beobachtet |
| `ws.chatgpt.com/p33/ws/user/{userId}` | 3 Handshakes mit Status `101` | Beobachtet |
| Nachrichtenframes und Payloads | Nicht in den HAR-Aufzeichnungen enthalten | Unbekannt |

## Realtime / SDP

| Merkmal | Beobachtung |
|---|---|
| Endpunkt | `POST /realtime/wm` |
| Aufrufe | 8 |
| HTTP-Status | `201` |
| Request- und Response-Format | `application/sdp` |

## Umfang der Inventarisierung

- HAR-Aufzeichnungen: 16. und 22. Oktober 2026
- Normalisierte HTTP-Operationsmuster: 69
- Zugehörige Request-Einträge: 245

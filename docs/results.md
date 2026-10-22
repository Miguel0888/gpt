---
layout: default
title: Technische Ergebnisse
permalink: results.html
---

# Technische Ergebnisse

## Chat-Antwortstream

| Merkmal | Ergebnis |
|---|---|
| HTTP-Endpunkt | `POST /backend-api/f/conversation` |
| Content-Type | `text/event-stream` |
| Vollständige Antwortstreams | 4 |
| `delta`-Ereignisse | 53 |
| `delta_encoding`-Ereignisse | 4; Wert `v1` |
| JSON-`type`-Werte | `resume_conversation_token`, `input_message`, `title_generation`, `message_marker`, `server_ste_metadata`, `message_stream_complete`, `conversation_detail_metadata` |
| `message_marker` | 16 Ereignisse; Werte `cot_token`, `user_visible_token`, `final_channel_token`, `last_token` |
| Abschlussmarkierung | `[DONE]` in allen vier vollständigen Streams |

## Datei-Verarbeitungsstream

| Merkmal | Ergebnis |
|---|---|
| HTTP-Endpunkt | `POST /backend-api/files/process_upload_stream` |
| Content-Type | `text/event-stream` |
| Body-Framing | Zeilenweise getrennte JSON-Objekte |
| Ereignisse | `file.processing.started`, `file.processing.file_ready`, `file.indexing.completed`, `file.processing.completed` |
| Fortschrittswerte | 0, 20 und 100; kein Fortschrittswert bei `file.indexing.completed` |

## WebSockets

| Host / Pfad | Ergebnis |
|---|---|
| `codex-cloud-backend.chatgpt.com/` | 1 Handshake, Status `101` |
| `chatgpt.com/backend-api/dictation/stream` | WebSocket-Handshake; Query-Parameter `dictation_surface` |
| `ws.chatgpt.com/p33/ws/user/{userId}` | 3 Handshakes, Status `101` |
| Nachrichtenframes | Keine |

## Realtime / SDP

| Merkmal | Ergebnis |
|---|---|
| HTTP-Endpunkt | `POST /realtime/wm` |
| Aufrufe | 8 |
| HTTP-Status | `201` |
| Request- und Response-Format | `application/sdp` |

## HTTP-Inventar

- Normalisierte HTTP-Operationsmuster: 69
- Zugehörige Request-Einträge: 245

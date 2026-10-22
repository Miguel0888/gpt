---
layout: default
title: Schnittstellenübersicht
permalink: specification.html
---

# Schnittstellenübersicht

## HTTP

- Normalisierte HTTP-Operationsmuster: 69
- Zugehörige Request-Einträge: 245

Endpunkte, Parameter, Statuscodes und Request-/Response-Felder stehen in [OpenAPI](./openapi.yaml).

## Chat-Antwortstream

- Endpunkt: `POST /backend-api/f/conversation`
- Response Content-Type: `text/event-stream`
- Vollständige Streams: 4
- `delta`: 53 Ereignisse
- `delta_encoding`: 4 Ereignisse; Wert `v1`
- Weitere JSON-`type`-Werte: `resume_conversation_token`, `input_message`, `title_generation`, `message_marker`, `server_ste_metadata`, `message_stream_complete`, `conversation_detail_metadata`
- Abschlussmarkierung: `[DONE]` in allen vier vollständigen Streams

Details: [AsyncAPI](./asyncapi.html).

## Datei-Verarbeitungsstream

- Endpunkt: `POST /backend-api/files/process_upload_stream`
- Response Content-Type: `text/event-stream`
- Body-Framing: zeilenweise getrennte JSON-Objekte
- Ereignisse: `file.processing.started`, `file.processing.file_ready`, `file.indexing.completed`, `file.processing.completed`

Details: [AsyncAPI](./asyncapi.html).

## WebSockets

| Host / Pfad | Verbindungen |
|---|---|
| `codex-cloud-backend.chatgpt.com/` | 1 Handshake, Status `101` |
| `chatgpt.com/backend-api/dictation/stream` | WebSocket-Handshake; `dictation_surface`-Query-Parameter |
| `ws.chatgpt.com/p33/ws/user/{userId}` | 3 Handshakes, Status `101` |

WebSocket-Nachrichtenframes: keine.

## Realtime / SDP

- Endpunkt: `POST /realtime/wm`
- Aufrufe: 8
- HTTP-Status: `201`
- Request- und Response-Format: `application/sdp`

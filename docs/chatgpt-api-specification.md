---
layout: default
title: Schnittstellenübersicht
permalink: specification.html
---

# Schnittstellenübersicht

## HTTP

- HAR-Aufzeichnungen: 16. und 22. Oktober 2026
- Normalisierte HTTP-Operationsmuster: 69
- Zugehörige Request-Einträge: 245
- Die Requests stammen aus einer bereits authentifizierten Browsersitzung.

Die Endpunkte, Parameter, beobachteten Statuscodes und verfügbaren Request-/Response-Felder stehen in [OpenAPI](./openapi.yaml).

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
- Beobachtetes Body-Framing: zeilenweise getrennte JSON-Objekte
- Ereignisse: `file.processing.started`, `file.processing.file_ready`, `file.indexing.completed`, `file.processing.completed`

Details: [AsyncAPI](./asyncapi.html).

## WebSockets

| Host / Pfad | Beobachtete Verbindungen |
|---|---|
| `codex-cloud-backend.chatgpt.com/` | 1 Handshake, Status `101` |
| `chatgpt.com/backend-api/dictation/stream` | WebSocket-Handshake; `dictation_surface`-Query-Parameter |
| `ws.chatgpt.com/p33/ws/user/{userId}` | 3 Handshakes, Status `101` |

In den HAR-Aufzeichnungen sind keine WebSocket-Nachrichtenframes enthalten.

## Realtime / SDP

- Endpunkt: `POST /realtime/wm`
- Aufrufe: 8
- HTTP-Status: `201`
- Request- und Response-Format: `application/sdp`

## Browser-Hooks

Die Instrumentierungspunkte, normalisierten Events und deren Reihenfolge stehen in der [Hook-Spezifikation](./hooks.html). Das Schema des Event-Hub-Vertrags liegt unter [normalized-event.schema.json](./schemas/normalized-event.schema.json).

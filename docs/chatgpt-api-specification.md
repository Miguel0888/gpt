---
layout: default
title: Hinweise zur ChatGPT-Webschnittstelle
permalink: specification.html
---

# ChatGPT internal web API: specification notes

## Purpose

The file [`openapi.yaml`](./openapi.yaml) records HTTP operations observed in user-provided HAR captures. It is a reverse-engineered inventory for research and browser integration, **not an official OpenAI API contract**.

The [`asyncapi.yaml`](./asyncapi.yaml) describes the message variants observed in the conversation and file-processing streams. [`hooks.md`](./hooks.html) defines browser instrumentation and normalized events. [`observations.md`](./observations.html) records the evidence and the limits of each observation.

## Evidence scope

- Captures: 16 October 2026 and 22 October 2026.
- Normalized HTTP operation patterns in the OpenAPI inventory: 69.
- Relevant request entries represented in the inventory: 245.
- Four complete conversation response streams were summarized, with 53 `delta` events.

The operation-level `x-har-observations` extension records request counts, source captures, observed HTTP statuses and limits of schema evidence.

## What “complete” means here

The OpenAPI specification covers the endpoint patterns represented by the available HAR inventories. It does not claim that every endpoint used by ChatGPT has been discovered. The HAR captures do not provide complete request and response schemas for every operation. Where only field names were visible, property types and required fields are deliberately left unspecified.

Dynamic identifiers are normalized to placeholders. Signed upload URLs, session credentials, user content, transcripts and audio asset pointers are not embedded in the specification.

## Authentication

The captures originate from an already authenticated browser session. The specification therefore does not claim a reusable authentication scheme. Do not copy cookies, bearer values, WebSocket subprotocol values or signed URL parameters into this repository.

## Streams and browser hooks

The conversation stream uses `text/event-stream` and includes observed SSE event names and JSON `type` variants. The file-processing endpoint advertises the same Content-Type, but its captured body consists of newline-delimited JSON objects rather than conventional SSE frames. The framing and payload limitations are documented in [AsyncAPI](./asyncapi.yaml) and [HAR observations](./observations.html).

For WebSocket endpoints, the captures contain only handshakes; message frames are absent. The AsyncAPI document therefore does not invent WebSocket payload schemas.

Browser instrumentation points such as `fetch`, XHR, navigation and DOM events are described separately in [the hook specification](./hooks.html). The normalized Event Hub contract is defined in [`schemas/normalized-event.schema.json`](./schemas/normalized-event.schema.json) and is explicitly a proposed application contract, not a copy of ChatGPT's internal wire schema.

## Stability warning

These are private, implementation-specific web endpoints. Paths, parameters, schemas and behavior can change without notice. Keep client implementations behind replaceable adapters and validate them against fresh captures before relying on them.

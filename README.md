# GPT

This repository contains ChatGPT personalization notes and evidence-based documentation of observed ChatGPT web interfaces.

## Published API documentation

GitHub Pages is enabled and publishes the `main` branch from `/docs`.

- **[OpenAPI / Swagger UI](https://miguel0888.github.io/gpt/)** — HTTP endpoints, methods, parameters, request bodies and responses.
- **[AsyncAPI / message streams](https://miguel0888.github.io/gpt/asyncapi.html)** — observed conversation and file-processing stream messages.
- **[Browser hooks](https://miguel0888.github.io/gpt/hooks.html)** — browser instrumentation, normalized events, lifecycle, ordering and privacy requirements.
- **[HAR observations](https://miguel0888.github.io/gpt/observations.html)** — evidence, counts, confidence and unresolved protocol details.
- **[Specification notes](https://miguel0888.github.io/gpt/specification.html)** — scope, assumptions and limitations.

## Specification sources

The source files live under `docs/`:

- [OpenAPI source](docs/openapi.yaml) — the canonical OpenAPI 3.1 document loaded by Swagger UI.
- [AsyncAPI source](docs/asyncapi.yaml) — the canonical AsyncAPI 3.1 document. It references reusable JSON Schemas.
- [AsyncAPI viewer bundle](docs/asyncapi.bundle.yaml) — a self-contained copy for browser rendering. External JSON Schema references are resolved so the browser component does not need a filesystem resolver.
- [Browser hook specification](docs/hooks.md)
- [HAR observations](docs/observations.md)
- [Specification notes](docs/chatgpt-api-specification.md)
- [Shared stream JSON Schemas](docs/schemas/chat-stream-events.schema.json)
- [Normalized Event Hub JSON Schema](docs/schemas/normalized-event.schema.json)

The Swagger UI loads `docs/openapi.yaml`. The AsyncAPI page loads the self-contained `docs/asyncapi.bundle.yaml`; the canonical `docs/asyncapi.yaml` remains the maintainable source and references the shared schemas.

## Validation

GitHub Actions validates the OpenAPI and AsyncAPI source documents, checks local documentation links and JSON Schema files, and verifies that the checked-in AsyncAPI viewer bundle matches the source specification after resolving local schema references.

To regenerate the viewer bundle after changing the AsyncAPI source or shared stream schemas, run:

```bash
python -m pip install PyYAML==6.0.3
python scripts/build_asyncapi_bundle.py
python scripts/validate_docs.py
```

Use `python scripts/build_asyncapi_bundle.py --check` to check whether the committed bundle is up to date without changing files.

## Scope and security

These specifications are based on user-provided HAR observations of ChatGPT's internal web interface. They are **not official or stable OpenAI API contracts**. Paths, fields and behavior can change without notice.

Do not commit original HAR files, cookies, authorization headers, WebSocket subprotocol credentials, signed URLs, raw conversation contents, transcripts or audio asset pointers. Treat message payloads and identifiers as potentially sensitive. Keep client implementations behind replaceable adapters and revalidate against fresh captures before relying on them.

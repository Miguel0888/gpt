# GPT

## Veröffentlichte Dokumentation

- [OpenAPI / Swagger UI](https://miguel0888.github.io/gpt/)
- [AsyncAPI / Streams](https://miguel0888.github.io/gpt/asyncapi.html)
- [Browser-Hooks](https://miguel0888.github.io/gpt/hooks.html)
- [HAR-Beobachtungen](https://miguel0888.github.io/gpt/observations.html)
- [Schnittstellenübersicht](https://miguel0888.github.io/gpt/specification.html)

## Quelldateien

- [OpenAPI](docs/openapi.yaml)
- [AsyncAPI](docs/asyncapi.yaml)
- [AsyncAPI-Bundle für die Browserdarstellung](docs/asyncapi.bundle.yaml)
- [Hook-Spezifikation](docs/hooks.md)
- [HAR-Beobachtungen](docs/observations.md)
- [Schnittstellenübersicht](docs/chatgpt-api-specification.md)
- [Stream-JSON-Schema](docs/schemas/chat-stream-events.schema.json)
- [Normalisiertes Event-Schema](docs/schemas/normalized-event.schema.json)

## AsyncAPI-Bundle aktualisieren

Nach Änderungen an `docs/asyncapi.yaml` oder `docs/schemas/chat-stream-events.schema.json`:

```bash
python -m pip install PyYAML==6.0.3
python scripts/build_asyncapi_bundle.py
python scripts/validate_docs.py
```

Mit `python scripts/build_asyncapi_bundle.py --check` lässt sich das vorhandene Bundle prüfen.

## Validierung

GitHub Actions validiert OpenAPI, AsyncAPI, JSON-Schemas, Dokumentationspfade und das generierte AsyncAPI-Bundle.

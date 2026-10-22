# GPT

This repository stores ChatGPT personalization notes and reverse-engineered API documentation.

## API documentation

The documentation is intentionally split by interface type:

- **[OpenAPI / Swagger UI](docs/index.html)** — HTTP methods, paths, parameters, observed request fields and HTTP responses.
- **[OpenAPI YAML](docs/openapi.yaml)** — canonical OpenAPI 3.1 document used by Swagger UI.
- **[AsyncAPI viewer](docs/asyncapi.html)** — observed message events from the conversation and file-processing streams.
- **[AsyncAPI YAML](docs/asyncapi.yaml)** — message channels and payload schemas supported by the available captures.
- **[Browser hooks](docs/hooks.md)** — JavaScript instrumentation points, normalized events, lifecycle, ordering and privacy requirements.
- **[HAR observations](docs/observations.md)** — evidence, counts, confidence and unresolved protocol details.
- **[Specification notes](docs/chatgpt-api-specification.md)** — scope and limitations.
- **[Shared JSON Schemas](docs/schemas/)** — reusable wire-message and normalized-event contracts.

Swagger UI loads `./openapi.yaml` relative to `docs/index.html`. The AsyncAPI viewer loads `./asyncapi.yaml` relative to `docs/asyncapi.html`; keep these files together under `docs/` so the links work when published at a GitHub Pages project path such as `/gpt/`.

## Publish with GitHub Pages

GitHub Pages is not enabled for this repository yet. To publish the site:

1. Open **Settings → Pages**.
2. Under **Build and deployment**, select **Deploy from a branch**.
3. Select branch `main` and folder `/docs`, then save.
4. Wait for the Pages deployment to complete.

After Pages is enabled, the entry page should be available at:

https://miguel0888.github.io/gpt/

The documentation source can also be reviewed directly in the repository before publishing.

## Validation

The GitHub Actions workflow validates the AsyncAPI and OpenAPI documents and checks local documentation links and JSON Schema syntax on pull requests and pushes.

## Scope and security

These specifications are based on user-provided HAR observations of ChatGPT's internal web interface. They are **not official or stable OpenAI API contracts**. Paths, fields and behavior can change without notice.

Do not commit original HAR files, cookies, authorization headers, WebSocket subprotocol credentials, signed URLs, raw conversation contents, transcripts or audio asset pointers. Treat message payloads and identifiers as potentially sensitive. Keep client implementations behind replaceable adapters and revalidate against fresh captures before relying on them.

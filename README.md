# GPT

This repository stores ChatGPT personalization notes and related API documentation.

## OpenAPI documentation

The repository includes a static [Swagger UI entry page](docs/index.html) for rendering an OpenAPI specification in the browser.

- **Swagger UI page:** `docs/index.html`
- **OpenAPI specification:** `docs/openapi.yaml` (to be added once the specification is ready)
- **Swagger UI assets:** Loaded from the pinned Swagger UI CDN distribution; no build step or backend is required.

The Swagger UI page loads the specification using the relative URL `./openapi.yaml`. Keep the specification at `docs/openapi.yaml` unless the URL in `docs/index.html` is changed accordingly.

### Publish with GitHub Pages

1. Open the repository's **Settings → Pages**.
2. Under **Build and deployment**, select **Deploy from a branch**.
3. Select branch `main` and folder `/docs`, then save.
4. Add the completed OpenAPI file at `docs/openapi.yaml`.

After GitHub Pages is enabled and the specification has been added, the documentation will be available at:

https://miguel0888.github.io/gpt/

The page is not fully usable until `docs/openapi.yaml` exists and GitHub Pages has been enabled.

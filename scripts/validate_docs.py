from html.parser import HTMLParser
from pathlib import Path
import json
import sys
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
GENERATED_MARKDOWN_PAGES = {
    "hooks.html": "hooks.md",
    "results.html": "results.md",
    "specification.html": "chatgpt-api-specification.md",
}


class LinkCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name in ("href", "src") and value:
                self.links.append(value)


def require(condition, message):
    if not condition:
        raise SystemExit(message)


def validate_html_links(relative_path):
    source = DOCS / relative_path
    parser = LinkCollector()
    parser.feed(source.read_text(encoding="utf-8"))

    for link in parser.links:
        parsed = urlparse(link)
        if parsed.scheme or parsed.netloc or link.startswith("#"):
            continue

        target_name = parsed.path.removeprefix("./")
        if not target_name:
            continue

        target = DOCS / target_name
        if target.is_file():
            continue

        markdown_name = GENERATED_MARKDOWN_PAGES.get(target_name)
        if markdown_name and (DOCS / markdown_name).is_file():
            continue

        require(False, "Broken local link in " + relative_path + ": " + link)


def main():
    required_files = [
        "index.html",
        "openapi.yaml",
        "asyncapi.html",
        "asyncapi.yaml",
        "asyncapi.bundle.yaml",
        "hooks.md",
        "results.md",
        "chatgpt-api-specification.md",
        "_layouts/default.html",
        "_config.yml",
        "schemas/chat-stream-events.schema.json",
        "schemas/normalized-event.schema.json",
    ]

    for relative_path in required_files:
        require((DOCS / relative_path).is_file(), "Missing required documentation file: " + relative_path)

    index_html = (DOCS / "index.html").read_text(encoding="utf-8")
    asyncapi_html = (DOCS / "asyncapi.html").read_text(encoding="utf-8")
    require('url: "./openapi.yaml"' in index_html, "Swagger UI must load ./openapi.yaml.")
    require('url: "./asyncapi.bundle.yaml"' in asyncapi_html, "AsyncAPI viewer must load the self-contained ./asyncapi.bundle.yaml.")
    require("supportedSubmitMethods: []" in index_html, "Swagger UI interactive submission must remain disabled.")
    require('<aside class="notice">' not in index_html, "Swagger UI page must not contain an editorial notice banner.")
    require('<aside class="notice">' not in asyncapi_html, "AsyncAPI page must not contain an editorial notice banner.")

    layout_html = (DOCS / "_layouts/default.html").read_text(encoding="utf-8")
    require('title: "ChatGPT Web API"' in (DOCS / "openapi.yaml").read_text(encoding="utf-8"), "OpenAPI title is missing.")
    require("permalink: results.html" in (DOCS / "results.md").read_text(encoding="utf-8"), "Technical results page is missing.")

    asyncapi_bundle = (DOCS / "asyncapi.bundle.yaml").read_text(encoding="utf-8")
    require("./schemas/chat-stream-events.schema.json#/" not in asyncapi_bundle, "AsyncAPI viewer bundle must not contain external JSON Schema references.")

    for relative_path in ("index.html", "asyncapi.html", "_layouts/default.html"):
        validate_html_links(relative_path)

    stream_schema = json.loads((DOCS / "schemas/chat-stream-events.schema.json").read_text(encoding="utf-8"))
    normalized_schema = json.loads((DOCS / "schemas/normalized-event.schema.json").read_text(encoding="utf-8"))
    require("FileProcessingEvent" in stream_schema.get("definitions", {}), "FileProcessingEvent schema is missing.")
    require(normalized_schema.get("properties", {}).get("eventType"), "Normalized eventType schema is missing.")

    print("Documentation file and local-link checks passed.")
    print("Parsed both shared JSON Schema documents successfully.")


if __name__ == "__main__":
    main()

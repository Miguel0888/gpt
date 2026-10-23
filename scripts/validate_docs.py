from html.parser import HTMLParser
from pathlib import Path
import json
import re
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
GENERATED_MARKDOWN_PAGES = {
    "docs/hooks.html": "docs/hooks.md",
    "docs/results.html": "docs/results.md",
    "docs/specification.html": "docs/chatgpt-api-specification.md",
}
MARKDOWN_FILES = (
    "README.md",
    "docs/hooks.md",
    "docs/results.md",
    "docs/chatgpt-api-specification.md",
)
INLINE_LINK_PATTERN = re.compile(
    r"!?\[([^\]]*)\]\(\s*(?:<(?P<angle>[^>]+)>|(?P<plain>(?:\\\\.|[^\s()]+|\([^()]*\))+))"
)
REFERENCE_DEFINITION_PATTERN = re.compile(
    r"(?m)^[ \t]{0,3}\[([^\]]+)\]:[ \t]*(?:<([^>\n]+)>|(\S+))"
)
REFERENCE_LINK_PATTERN = re.compile(r"!?\[([^\]]+)\]\[([^\]]*)\]")
SHORTCUT_LINK_PATTERN = re.compile(r"!?\[([^\]]+)\](?![\[(])")
ATX_HEADING_PATTERN = re.compile(r"^ {0,3}(#{1,6})[ \t]+(.+?)\s*#*\s*$")
SETEXT_HEADING_PATTERN = re.compile(r"^ {0,3}(=+|-+)\s*$")
FENCE_OPEN_PATTERN = re.compile(r"^ {0,3}(`{3,}|~{3,})")


class HtmlDocumentParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.anchors = set()

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name in ("href", "src") and value:
                self.links.append(value)
            if name == "id" and value:
                self.anchors.add(value)
            if tag == "a" and name == "name" and value:
                self.anchors.add(value)


def require(condition, message):
    if not condition:
        raise SystemExit(message)


def strip_markdown_code(source):
    visible_lines = []
    fence_character = None
    fence_length = 0

    for line in source.splitlines():
        opening = FENCE_OPEN_PATTERN.match(line)
        if fence_character is None:
            if opening:
                marker = opening.group(1)
                fence_character = marker[0]
                fence_length = len(marker)
            else:
                visible_lines.append(line)
            continue

        closing_pattern = (
            r"^ {0,3}"
            + re.escape(fence_character)
            + "{"
            + str(fence_length)
            + r",}\s*$"
        )
        if re.match(closing_pattern, line):
            fence_character = None
            fence_length = 0

    visible_source = "\n".join(visible_lines)
    return re.sub(r"(?<!`)\`+[^\`\n]*\`+(?!`)", "", visible_source)


def normalize_reference_label(label):
    return re.sub(r"\s+", " ", label).strip().casefold()


def collect_markdown_links(source):
    visible_source = strip_markdown_code(source)
    reference_targets = {}

    def collect_reference_definition(match):
        target = match.group(2) or match.group(3)
        reference_targets[normalize_reference_label(match.group(1))] = target
        return ""

    visible_source = REFERENCE_DEFINITION_PATTERN.sub(
        collect_reference_definition,
        visible_source,
    )
    links = []

    for match in INLINE_LINK_PATTERN.finditer(visible_source):
        target = match.group("angle") or match.group("plain")
        links.append((target.replace("\\(", "(").replace("\\)", ")"), visible_source.count("\n", 0, match.start()) + 1))

    for match in REFERENCE_LINK_PATTERN.finditer(visible_source):
        label = match.group(2) or match.group(1)
        target = reference_targets.get(normalize_reference_label(label))
        if target:
            links.append((target, visible_source.count("\n", 0, match.start()) + 1))

    for match in SHORTCUT_LINK_PATTERN.finditer(visible_source):
        label = normalize_reference_label(match.group(1))
        target = reference_targets.get(label)
        if target:
            links.append((target, visible_source.count("\n", 0, match.start()) + 1))

    return links


def slugify_heading(heading):
    explicit_id = re.search(r"\s*\{#([^\s}]+)\}\s*$", heading)
    if explicit_id:
        return explicit_id.group(1)

    heading = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", heading)
    heading = re.sub(r"`([^`]*)`", r"\1", heading)
    heading = re.sub(r"<[^>]+>", "", heading)
    heading = re.sub(r"[*!_~]", "", heading).lower().strip()
    heading = re.sub(r"[^\w\- ]", "", heading, flags=re.UNICODE)
    return re.sub(r"\s+", "-", heading)


def markdown_anchor_ids(source):
    lines = strip_markdown_code(source).splitlines()
    anchors = set()
    duplicate_counts = {}

    def add_heading(heading):
        slug = slugify_heading(heading)
        if not slug:
            return

        duplicate_index = duplicate_counts.get(slug, 0)
        duplicate_counts[slug] = duplicate_index + 1
        anchors.add(slug if duplicate_index == 0 else slug + "-" + str(duplicate_index))

    index = 0
    while index < len(lines):
        heading_match = ATX_HEADING_PATTERN.match(lines[index])
        if heading_match:
            add_heading(heading_match.group(2))
            index += 1
            continue

        if (
            lines[index].strip()
            and index + 1 < len(lines)
            and SETEXT_HEADING_PATTERN.match(lines[index + 1])
        ):
            add_heading(lines[index].strip())
            index += 2
            continue

        index += 1

    return anchors


def html_anchor_ids(path):
    parser = HtmlDocumentParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser.anchors


def resolve_local_target(source, link, context, base_directory=None):
    parsed = urlparse(link)
    if parsed.scheme or parsed.netloc:
        return None

    link_path = unquote(parsed.path)
    resolution_base = base_directory or source.parent
    candidate = (resolution_base / link_path).resolve() if link_path else source.resolve()

    try:
        relative_path = candidate.relative_to(ROOT).as_posix()
    except ValueError:
        require(False, "Local link escapes the repository in " + context + ": " + link)
        return None

    if candidate.is_dir():
        directory_targets = (candidate / "index.html", candidate / "README.md")
        candidate = next((target for target in directory_targets if target.is_file()), candidate)
        relative_path = candidate.relative_to(ROOT).as_posix()

    if candidate.is_file():
        return candidate

    generated_source = GENERATED_MARKDOWN_PAGES.get(relative_path)
    if generated_source:
        markdown_source = ROOT / generated_source
        require(
            markdown_source.is_file(),
            "Generated page has no Markdown source in " + context + ": " + link,
        )
        return markdown_source

    require(False, "Broken local link in " + context + ": " + link)
    return None


def validate_local_link(source, link, context, base_directory=None):
    parsed = urlparse(link)
    target = resolve_local_target(source, link, context, base_directory)
    if target is None or not parsed.fragment:
        return

    fragment = unquote(parsed.fragment)
    if target.suffix.lower() == ".md":
        available_anchors = markdown_anchor_ids(target.read_text(encoding="utf-8"))
    elif target.suffix.lower() == ".html":
        available_anchors = html_anchor_ids(target)
    else:
        return

    require(
        fragment in available_anchors,
        "Broken local anchor in " + context + ": " + link,
    )


def validate_html_links(relative_path):
    source = DOCS / relative_path
    parser = HtmlDocumentParser()
    parser.feed(source.read_text(encoding="utf-8"))

    for link in parser.links:
        validate_local_link(source, link, relative_path, DOCS)


def validate_markdown_links(relative_path):
    source = ROOT / relative_path
    content = source.read_text(encoding="utf-8")

    for link, line_number in collect_markdown_links(content):
        context = relative_path + ":" + str(line_number)
        validate_local_link(source, link, context)


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

    require('title: "ChatGPT Web API"' in (DOCS / "openapi.yaml").read_text(encoding="utf-8"), "OpenAPI title is missing.")
    require("permalink: results.html" in (DOCS / "results.md").read_text(encoding="utf-8"), "Technical results page is missing.")

    asyncapi_bundle = (DOCS / "asyncapi.bundle.yaml").read_text(encoding="utf-8")
    require("./schemas/chat-stream-events.schema.json#/" not in asyncapi_bundle, "AsyncAPI viewer bundle must not contain external JSON Schema references.")

    for relative_path in ("index.html", "asyncapi.html", "_layouts/default.html"):
        validate_html_links(relative_path)

    for relative_path in MARKDOWN_FILES:
        require((ROOT / relative_path).is_file(), "Missing Markdown document: " + relative_path)
        validate_markdown_links(relative_path)

    stream_schema = json.loads((DOCS / "schemas/chat-stream-events.schema.json").read_text(encoding="utf-8"))
    normalized_schema = json.loads((DOCS / "schemas/normalized-event.schema.json").read_text(encoding="utf-8"))
    require("FileProcessingEvent" in stream_schema.get("definitions", {}), "FileProcessingEvent schema is missing.")
    require(normalized_schema.get("properties", {}).get("eventType"), "Normalized eventType schema is missing.")

    print("HTML links, Markdown links, generated page paths, and local anchors passed validation.")
    print("Parsed both shared JSON Schema documents successfully.")


if __name__ == "__main__":
    main()

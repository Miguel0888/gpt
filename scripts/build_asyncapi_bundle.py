#!/usr/bin/env python3
"""Build or verify a self-contained AsyncAPI document for browser rendering."""

import argparse
from copy import deepcopy
import json
from pathlib import Path
import sys

import yaml


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
SOURCE_PATH = DOCS / "asyncapi.yaml"
BUNDLE_PATH = DOCS / "asyncapi.bundle.yaml"
SCHEMAS_PATH = DOCS / "schemas" / "chat-stream-events.schema.json"
EXTERNAL_REF_PREFIX = "./schemas/chat-stream-events.schema.json#/definitions/"


def load_json(path):
    with path.open("r", encoding="utf-8") as source:
        return json.load(source)


def load_yaml(path):
    with path.open("r", encoding="utf-8") as source:
        return yaml.safe_load(source)


def resolve_external_schema_references(value, definitions):
    if isinstance(value, dict):
        reference = value.get("$ref")
        if isinstance(reference, str) and reference.startswith(EXTERNAL_REF_PREFIX):
            definition_name = reference[len(EXTERNAL_REF_PREFIX):]
            if "/" in definition_name or definition_name not in definitions:
                raise ValueError("Unsupported or missing schema reference: " + reference)
            return deepcopy(definitions[definition_name])

        return {
            key: resolve_external_schema_references(item, definitions)
            for key, item in value.items()
        }

    if isinstance(value, list):
        return [
            resolve_external_schema_references(item, definitions)
            for item in value
        ]

    return value


def build_bundle():
    source_specification = load_yaml(SOURCE_PATH)
    shared_schemas = load_json(SCHEMAS_PATH)
    definitions = shared_schemas.get("definitions", {})
    return resolve_external_schema_references(source_specification, definitions)


def write_bundle(bundle):
    with BUNDLE_PATH.open("w", encoding="utf-8", newline="\n") as output:
        yaml.safe_dump(
            bundle,
            output,
            allow_unicode=True,
            sort_keys=False,
            width=120,
        )


def verify_bundle(expected_bundle):
    actual_bundle = load_yaml(BUNDLE_PATH)
    if actual_bundle != expected_bundle:
        raise SystemExit(
            "AsyncAPI viewer bundle is stale. Run: "
            "python scripts/build_asyncapi_bundle.py"
        )

    print("AsyncAPI viewer bundle matches the source and shared JSON Schemas.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verify the committed bundle without rewriting it.",
    )
    arguments = parser.parse_args()

    bundle = build_bundle()
    if arguments.check:
        verify_bundle(bundle)
        return

    write_bundle(bundle)
    print("Generated " + str(BUNDLE_PATH.relative_to(ROOT)))


if __name__ == "__main__":
    main()

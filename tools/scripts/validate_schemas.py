#!/usr/bin/env python3
"""Validates JSON records against dual-agent corpus builder schemas."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List
from urllib.parse import urlparse

try:
    import jsonschema
    from jsonschema import Draft202012Validator, FormatChecker, RefResolver
except ImportError:
    print("Error: jsonschema library required. Install with: pip install jsonschema", file=sys.stderr)
    sys.exit(1)


SCHEMA_DIR = Path(__file__).parent.parent / "schemas"


def load_schema(schema_name: str) -> Dict[str, Any]:
    """Load a JSON schema from the schemas directory."""
    schema_path = SCHEMA_DIR / f"{schema_name}.schema.json"
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema not found: {schema_path}")
    
    with schema_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def create_resolver() -> RefResolver:
    """Create a RefResolver with all available schemas."""
    schema_store = {}
    for schema_file in SCHEMA_DIR.glob("*.schema.json"):
        with schema_file.open("r", encoding="utf-8") as f:
            schema = json.load(f)
            if "$id" in schema:
                schema_store[schema["$id"]] = schema
    
    # Use the master record schema as base
    base_uri = "https://example.org/schemas/"
    return RefResolver(base_uri, {}, store=schema_store)


def _is_datetime_string(value: str) -> bool:
    if not isinstance(value, str):
        return False
    try:
        normalized = value.replace("Z", "+00:00") if value.endswith("Z") else value
        datetime.fromisoformat(normalized)
        return True
    except ValueError:
        return False


def _is_uri_string(value: str) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return bool(parsed.scheme and parsed.netloc)


def _collect_format_errors(data: Any, schema: Dict[str, Any], path: str = "root") -> List[str]:
    errors: List[str] = []

    schema_type = schema.get("type")
    schema_format = schema.get("format")

    if schema_format == "date-time" and data is not None and not _is_datetime_string(data):
        errors.append(f"{path}: {data!r} is not a 'date-time'")
    elif schema_format == "uri" and data is not None and not _is_uri_string(data):
        errors.append(f"{path}: {data!r} is not a 'uri'")

    if schema_type == "object" and isinstance(data, dict):
        for key, subschema in schema.get("properties", {}).items():
            if key in data:
                child_path = f"{path}.{key}" if path != "root" else key
                errors.extend(_collect_format_errors(data[key], subschema, child_path))
    elif schema_type == "array" and isinstance(data, list):
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(data):
                child_path = f"{path}.{index}" if path != "root" else str(index)
                errors.extend(_collect_format_errors(item, item_schema, child_path))

    for subschema in schema.get("allOf", []):
        errors.extend(_collect_format_errors(data, subschema, path))

    if "if" in schema and isinstance(data, dict):
        condition_validator = Draft202012Validator(schema["if"], format_checker=FormatChecker())
        if not list(condition_validator.iter_errors(data)) and "then" in schema:
            errors.extend(_collect_format_errors(data, schema["then"], path))
        elif list(condition_validator.iter_errors(data)) and "else" in schema:
            errors.extend(_collect_format_errors(data, schema["else"], path))

    return errors


def validate_record(data: Dict[str, Any], schema_name: str) -> tuple[bool, List[str]]:
    """Validate a single record against a schema.
    
    Args:
        data: The JSON data to validate
        schema_name: Name of the schema (without .schema.json extension)
    
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    schema = load_schema(schema_name)
    resolver = create_resolver()
    validator = Draft202012Validator(
        schema,
        resolver=resolver,
        format_checker=FormatChecker(),
    )
    
    errors = []
    for error in validator.iter_errors(data):
        path = ".".join(str(p) for p in error.path) if error.path else "root"
        errors.append(f"{path}: {error.message}")

    for error in _collect_format_errors(data, schema):
        if error not in errors:
            errors.append(error)
    
    return (len(errors) == 0, errors)


def validate_file(file_path: Path, schema_name: str) -> tuple[int, int, List[str]]:
    """Validate a JSON or JSONL file.
    
    Args:
        file_path: Path to JSON or JSONL file
        schema_name: Name of the schema to validate against
    
    Returns:
        Tuple of (total_records, valid_count, all_errors)
    """
    total = 0
    valid = 0
    all_errors = []
    
    with file_path.open("r", encoding="utf-8") as f:
        if file_path.suffix == ".jsonl":
            for line_num, line in enumerate(f, 1):
                if not line.strip():
                    continue
                total += 1
                try:
                    data = json.loads(line)
                    is_valid, errors = validate_record(data, schema_name)
                    if is_valid:
                        valid += 1
                    else:
                        all_errors.append(f"Line {line_num}:")
                        all_errors.extend(f"  {e}" for e in errors)
                except json.JSONDecodeError as e:
                    all_errors.append(f"Line {line_num}: Invalid JSON - {e}")
        else:
            total = 1
            try:
                data = json.load(f)
                is_valid, errors = validate_record(data, schema_name)
                if is_valid:
                    valid += 1
                else:
                    all_errors.extend(errors)
            except json.JSONDecodeError as e:
                all_errors.append(f"Invalid JSON: {e}")
    
    return (total, valid, all_errors)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate JSON records against dual-agent corpus builder schemas. "
                    "When called with no arguments, validates data/processed/records.jsonl "
                    "against the master-record schema (default behaviour)."
    )
    parser.add_argument(
        "file",
        nargs="?",
        type=Path,
        default=None,
        help="JSON or JSONL file to validate (default: data/processed/records.jsonl)"
    )
    parser.add_argument(
        "--schema",
        required=False,
        default=None,
        choices=["webscout-input", "webscout-output", "iconocode-output", "master-record", "purification-record", "argos-manifest"],
        help="Schema to validate against (default: master-record when validating records.jsonl)"
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show all validation errors"
    )
    
    args = parser.parse_args()

    # Apply defaults when called without arguments
    repo_root = Path(__file__).resolve().parent.parent.parent
    if args.file is None:
        args.file = repo_root / "data" / "processed" / "records.jsonl"
    if args.schema is None:
        # Infer schema from filename
        if args.file.name == "purification.jsonl":
            args.schema = "purification-record"
        elif args.file.name == "records.jsonl" or args.file.suffix == ".jsonl":
            args.schema = "master-record"
        else:
            parser.error("--schema is required when validating non-JSONL files")

    if not args.file.exists():
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        sys.exit(1)
    
    print(f"Validating {args.file} against {args.schema} schema...")
    total, valid, errors = validate_file(args.file, args.schema)
    
    if errors:
        if args.verbose or total <= 10:
            print("\nValidation errors:")
            for error in errors:
                print(f"  {error}")
        else:
            print(f"\n{len(errors)} validation error(s) found (use --verbose to see all)")
            for error in errors[:5]:
                print(f"  {error}")
            print(f"  ... and {len(errors) - 5} more")
    
    print(f"\nResults: {valid}/{total} records valid")
    
    if valid == total:
        print("✓ All records are valid")
        sys.exit(0)
    else:
        print(f"✗ {total - valid} record(s) failed validation")
        sys.exit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Validates JSON records against dual-agent corpus builder schemas."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

try:
    import jsonschema
    from jsonschema import Draft202012Validator, RefResolver
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
    validator = Draft202012Validator(schema, resolver=resolver)
    
    errors = []
    for error in validator.iter_errors(data):
        path = ".".join(str(p) for p in error.path) if error.path else "root"
        errors.append(f"{path}: {error.message}")
    
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
        choices=["webscout-input", "webscout-output", "iconocode-output", "master-record", "purification-record"],
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

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
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError:
    print("Error: jsonschema library required. Install with: pip install jsonschema", file=sys.stderr)
    sys.exit(1)

try:
    from referencing import Registry, Resource
except ImportError:
    print("Error: referencing library required. Install with: pip install referencing", file=sys.stderr)
    sys.exit(1)


SCHEMA_DIR = Path(__file__).parent.parent / "schemas"


def load_schema(schema_name: str) -> Dict[str, Any]:
    """Load a JSON schema from the schemas directory."""
    # Try schemas/ (new location at repo root), then tools/schemas/ (legacy)
    repo_root = Path(__file__).parent.parent.parent
    for base in (repo_root / "schemas", repo_root / "tools" / "schemas"):
        schema_path = base / f"{schema_name}.schema.json"
        if schema_path.exists():
            with schema_path.open("r", encoding="utf-8") as f:
                return json.load(f)
    raise FileNotFoundError(f"Schema not found: {schema_name}.schema.json in schemas/ or tools/schemas/")


def create_registry() -> Registry:
    """Create a Registry with all available schemas."""
    resources = []
    for schema_file in SCHEMA_DIR.glob("*.schema.json"):
        with schema_file.open("r", encoding="utf-8") as f:
            schema = json.load(f)
            if "$id" in schema:
                resources.append((schema["$id"], Resource.from_contents(schema)))

    return Registry().with_resources(resources)


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
    return bool(parsed.scheme)


def _collect_format_errors(data: Any, schema: Dict[str, Any], path: str = "root") -> List[str]:
    errors: List[str] = []

    schema_type = schema.get("type")
    schema_format = schema.get("format")

    if schema_format == "date-time" and data is not None and not _is_datetime_string(data):
        errors.append(f"{path}: {data!r} is not a 'date-time'")
    elif schema_format == "uri" and data is not None and not _is_uri_string(data):
        errors.append(f"{path}: {data!r} is not a valid URI")

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
        condition_errors = list(condition_validator.iter_errors(data))
        if not condition_errors and "then" in schema:
            errors.extend(_collect_format_errors(data, schema["then"], path))
        elif condition_errors and "else" in schema:
            errors.extend(_collect_format_errors(data, schema["else"], path))

    return errors


def validate_records(
    records: List[Dict[str, Any]],
    schema_name: str,
) -> tuple[int, int, List[str], List[Dict[str, Any]]]:
    """Validate a list of in-memory records.

    Returns:
        (valid_count, total_count, errors, warnings)

        - errors: list of human-readable error strings (block commit in enforce mode).
        - warnings: list of dicts with keys (code, record_id, field, detail).
          On the v2.3.0 pre-freeze path, conditional rules emit warnings only
          (do not block). Promote to errors in v2.4.0+ when data stabilizes.
    """
    schema = load_schema(schema_name)
    registry = create_registry()
    validator = Draft202012Validator(
        schema,
        registry=registry,
        format_checker=FormatChecker(),
    )

    valid = 0
    errors: List[str] = []
    warnings: List[Dict[str, Any]] = []

    for idx, data in enumerate(records, 1):
        record_id = data.get("item_id") or data.get("batch_id") or f"<idx-{idx}>"

        record_errors: List[str] = []
        for error in validator.iter_errors(data):
            path = ".".join(str(p) for p in error.path) if error.path else "root"
            record_errors.append(f"{path}: {error.message}")
        for error in _collect_format_errors(data, schema):
            if error not in record_errors:
                record_errors.append(error)

        if record_errors:
            errors.extend(f"[{record_id}] {e}" for e in record_errors)
        else:
            valid += 1

        warnings.extend(_check_v23_warnings(data, record_id))

    return (valid, len(records), errors, warnings)


# v2.3.0 pre-freeze constants (warnings mode; promote to errors in v2.4.0+).
MIN_JUSTIFICATIVA_GENERO_CHARS = 80
V23_FAMILIA_VALUE = "Masculino_Juridico"
V23_NEW_FIELDS = (
    "funcao_da_figura_masculina",
    "tipo_agencia_masculina",
    "funcao_atlanteana",
    "tipo_efluencia_hidrica",
    "substituicao_atributiva_hercules",
)


def _check_v23_warnings(
    data: Dict[str, Any],
    record_id: str,
) -> List[Dict[str, Any]]:
    """v2.3.0 pre-freeze conditional rules (warnings mode).

    Emits warnings only; does not block validation. Promote individual
    rules to errors in v2.4.0+ once data stabilizes.

    Rules:
      1. JUSTIFICATIVA_CURTA: masculino (or Masculino_Juridico) +
         justificativa_genero with fewer than MIN_JUSTIFICATIVA_GENERO_CHARS
         characters. Forces substantive justification of masculinity.
      2. REQUIRES_V23_FIELDS: familia_alegorica=Masculino_Juridico without
         at least one of the v2.3.0 patch fields populated.
      3. HERCULES_INCOERENTE: substituicao_atributiva_hercules with
         atributo_canonico_substituido == atributo_novo (nonsense identity).
    """
    warnings: List[Dict[str, Any]] = []
    purificacao = data.get("purificacao") or {}

    genero = purificacao.get("genero_atribuido")
    familia = purificacao.get("familia_alegorica")
    justificativa = purificacao.get("justificativa_genero") or ""
    is_masculine = genero == "masculino" or familia == V23_FAMILIA_VALUE

    # Rule 1: substantive justification required when masculine.
    if is_masculine and len(justificativa) < MIN_JUSTIFICATIVA_GENERO_CHARS:
        warnings.append({
            "code": "JUSTIFICATIVA_CURTA",
            "record_id": record_id,
            "field": "justificativa_genero",
            "detail": (
                f"{len(justificativa)} chars (< {MIN_JUSTIFICATIVA_GENERO_CHARS}); "
                f"required when genero=masculino or familia={V23_FAMILIA_VALUE}"
            ),
        })

    # Rule 2: at least one v2.3.0 patch field should accompany the family.
    if familia == V23_FAMILIA_VALUE:
        has_any_v23_field = any(
            purificacao.get(field) not in (None, "", [], {})
            for field in V23_NEW_FIELDS
        )
        if not has_any_v23_field:
            warnings.append({
                "code": "REQUIRES_V23_FIELDS",
                "record_id": record_id,
                "field": "familia_alegorica",
                "detail": (
                    f"familia={V23_FAMILIA_VALUE} but none of "
                    f"{list(V23_NEW_FIELDS)} populated"
                ),
            })

    # Rule 3: Hercules substitution must be a real substitution, not identity.
    hercules = purificacao.get("substituicao_atributiva_hercules")
    if isinstance(hercules, dict):
        orig = hercules.get("atributo_canonico_substituido")
        novo = hercules.get("atributo_novo")
        if orig is not None and novo is not None and orig == novo:
            warnings.append({
                "code": "HERCULES_INCOERENTE",
                "record_id": record_id,
                "field": "substituicao_atributiva_hercules",
                "detail": (
                    f"atributo_canonico_substituido ({orig!r}) == "
                    f"atributo_novo ({novo!r}); substitution must differ"
                ),
            })

    return warnings


def validate_file(
    file_path: Path,
    schema_name: str,
) -> tuple[int, int, List[str]]:
    """Validate a JSON or JSONL file on disk.

    Thin wrapper around validate_records(). Surfaces only errors (legacy
    contract); warnings are observable via validate_records() directly.

    Returns:
        (total_records, valid_count, errors)
    """
    records: List[Dict[str, Any]] = []
    try:
        with file_path.open("r", encoding="utf-8") as f:
            if file_path.suffix == ".jsonl":
                for line in f:
                    if not line.strip():
                        continue
                    records.append(json.loads(line))
            else:
                records = [json.load(f)]
    except json.JSONDecodeError as e:
        return (0, 0, [f"Invalid JSON: {e}"])

    valid, total, errors, _warnings = validate_records(records, schema_name)
    return (total, valid, errors)


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
        choices=["webscout-input", "webscout-output", "iconocode-output", "master-record", "purification-record", "argos-manifest", "codebook-v2.1.0"],
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

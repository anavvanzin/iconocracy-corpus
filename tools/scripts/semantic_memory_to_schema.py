#!/usr/bin/env python3
"""
Semantic Memory to Schema — Extracts semantic memory from vault notes
and generates a validated JSON schema for versioning.

Usage:
    python semantic_memory_to_schema.py [--vault PATH] [--output FILE] [--validate]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional, Set


@dataclass
class SemanticConcept:
    """Represents a semantic concept extracted from notes."""
    id: str
    label: str
    definition: str
    aliases: List[str]
    related_concepts: List[str]
    source_note: str
    evidence: List[str]
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class SemanticMemory:
    """Collection of semantic concepts forming the knowledge base."""
    version: str
    generated_at: str
    concepts: List[SemanticConcept]
    total_concepts: int
    
    def to_dict(self) -> Dict:
        return {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "version": self.version,
            "generated_at": self.generated_at,
            "total_concepts": self.total_concepts,
            "concepts": [c.to_dict() for c in self.concepts]
        }


class VaultParser:
    """Parses Obsidian vault notes to extract semantic concepts."""
    
    # Pattern for concept definitions
    CONCEPT_PATTERN = re.compile(
        r'^#+\s+(.+?)$.*?(?:Definição|Definition|Conceito):\s*(.+?)(?:\n\n|\Z)',
        re.MULTILINE | re.DOTALL | re.IGNORECASE
    )
    
    # Pattern for wikilinks
    WIKILINK_PATTERN = re.compile(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]')
    
    # Pattern for aliases
    ALIAS_PATTERN = re.compile(
        r'(?:Aliases?|Também conhecido como|Sinônimos?):\s*(.+?)(?:\n|$)',
        re.IGNORECASE
    )
    
    @staticmethod
    def normalize_id(text: str) -> str:
        """Generate normalized ID from text."""
        normalized = text.lower()
        normalized = re.sub(r'[^\w\s-]', '', normalized)
        normalized = re.sub(r'[-\s]+', '-', normalized)
        return normalized.strip('-')
    
    def extract_concepts_from_note(self, note_path: Path) -> List[SemanticConcept]:
        """Extract semantic concepts from a single note."""
        concepts: List[SemanticConcept] = []
        
        try:
            content = note_path.read_text(encoding='utf-8')
        except Exception as e:
            print(f"Warning: Could not read {note_path}: {e}", file=sys.stderr)
            return concepts
        
        # Extract frontmatter tags if present
        tags: Set[str] = set()
        frontmatter_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if frontmatter_match:
            fm = frontmatter_match.group(1)
            tag_matches = re.findall(r'tags?:\s*\[(.+?)\]', fm)
            for tag_list in tag_matches:
                tags.update(t.strip().strip('"\'') for t in tag_list.split(','))
        
        # Extract concept definitions
        for match in self.CONCEPT_PATTERN.finditer(content):
            label = match.group(1).strip()
            definition = match.group(2).strip()
            
            # Extract aliases
            aliases: List[str] = []
            alias_match = self.ALIAS_PATTERN.search(content)
            if alias_match:
                alias_text = alias_match.group(1)
                aliases = [a.strip() for a in re.split(r'[,;]', alias_text) if a.strip()]
            
            # Extract related concepts from wikilinks
            related = list(set(self.WIKILINK_PATTERN.findall(content)))
            
            # Extract evidence (quotes, citations)
            evidence: List[str] = []
            citation_matches = re.findall(r'>\s*(.+?)(?:\n|$)', content)
            evidence = [c.strip() for c in citation_matches if len(c.strip()) > 20][:3]
            
            concept = SemanticConcept(
                id=self.normalize_id(label),
                label=label,
                definition=definition,
                aliases=aliases,
                related_concepts=related,
                source_note=note_path.name,
                evidence=evidence
            )
            concepts.append(concept)
        
        return concepts
    
    def parse_vault(self, vault_path: Path) -> List[SemanticConcept]:
        """Parse entire vault and extract all semantic concepts."""
        all_concepts: List[SemanticConcept] = []
        
        if not vault_path.exists():
            print(f"Error: Vault path not found: {vault_path}", file=sys.stderr)
            return all_concepts
        
        # Scan for markdown notes
        for note_path in vault_path.rglob('*.md'):
            # Skip templates and system folders
            if any(part.startswith('.') or part.startswith('_') for part in note_path.parts):
                continue
            
            concepts = self.extract_concepts_from_note(note_path)
            all_concepts.extend(concepts)
        
        return all_concepts


class SchemaValidator:
    """Validates semantic memory against JSON schema."""
    
    @staticmethod
    def generate_schema() -> Dict:
        """Generate JSON schema for semantic memory."""
        return {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": "https://iconocracy.org/schemas/semantic-memory.schema.json",
            "title": "Semantic Memory Schema",
            "description": "Schema for semantic knowledge extracted from vault notes",
            "type": "object",
            "required": ["version", "generated_at", "total_concepts", "concepts"],
            "properties": {
                "$schema": {
                    "type": "string",
                    "format": "uri"
                },
                "version": {
                    "type": "string",
                    "pattern": "^\\d+\\.\\d+\\.\\d+$"
                },
                "generated_at": {
                    "type": "string",
                    "format": "date-time"
                },
                "total_concepts": {
                    "type": "integer",
                    "minimum": 0
                },
                "concepts": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["id", "label", "definition", "source_note"],
                        "properties": {
                            "id": {
                                "type": "string",
                                "pattern": "^[a-z0-9-]+$"
                            },
                            "label": {
                                "type": "string",
                                "minLength": 1
                            },
                            "definition": {
                                "type": "string",
                                "minLength": 10
                            },
                            "aliases": {
                                "type": "array",
                                "items": {"type": "string"}
                            },
                            "related_concepts": {
                                "type": "array",
                                "items": {"type": "string"}
                            },
                            "source_note": {
                                "type": "string"
                            },
                            "evidence": {
                                "type": "array",
                                "items": {"type": "string"}
                            }
                        }
                    }
                }
            }
        }
    
    @staticmethod
    def validate(memory_data: Dict) -> tuple[bool, List[str]]:
        """Validate semantic memory against schema."""
        try:
            import jsonschema
            from jsonschema import Draft202012Validator
        except ImportError:
            print("Warning: jsonschema not installed, skipping validation", file=sys.stderr)
            return (True, [])
        
        schema = SchemaValidator.generate_schema()
        validator = Draft202012Validator(schema)
        
        errors = []
        for error in validator.iter_errors(memory_data):
            path = ".".join(str(p) for p in error.path) if error.path else "root"
            errors.append(f"{path}: {error.message}")
        
        return (len(errors) == 0, errors)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract semantic memory from vault and generate validated JSON schema."
    )
    parser.add_argument(
        '--vault',
        type=Path,
        default=Path('vault'),
        help='Path to Obsidian vault (default: vault/)'
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=Path('data/semantic-memory.json'),
        help='Output JSON file (default: data/semantic-memory.json)'
    )
    parser.add_argument(
        '--schema-output',
        type=Path,
        default=Path('tools/schemas/semantic-memory.schema.json'),
        help='Schema output path'
    )
    parser.add_argument(
        '--validate',
        action='store_true',
        help='Validate output against schema'
    )
    parser.add_argument(
        '--version',
        default='1.0.0',
        help='Version string (default: 1.0.0)'
    )
    
    args = parser.parse_args()
    
    # Parse vault
    print(f"Parsing vault: {args.vault}")
    vault_parser = VaultParser()
    concepts = vault_parser.parse_vault(args.vault)
    
    if not concepts:
        print("Warning: No concepts extracted", file=sys.stderr)
    
    # Build semantic memory
    from datetime import datetime
    memory = SemanticMemory(
        version=args.version,
        generated_at=datetime.now().isoformat(),
        concepts=concepts,
        total_concepts=len(concepts)
    )
    
    # Convert to dict
    memory_data = memory.to_dict()
    
    # Validate if requested
    if args.validate:
        print("Validating...")
        is_valid, errors = SchemaValidator.validate(memory_data)
        if not is_valid:
            print("Validation errors:", file=sys.stderr)
            for error in errors:
                print(f"  {error}", file=sys.stderr)
            sys.exit(1)
        print("✓ Validation passed")
    
    # Write output
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('w', encoding='utf-8') as f:
        json.dump(memory_data, f, indent=2, ensure_ascii=False)
    print(f"✓ Wrote {len(concepts)} concepts to {args.output}")
    
    # Write schema
    schema = SchemaValidator.generate_schema()
    args.schema_output.parent.mkdir(parents=True, exist_ok=True)
    with args.schema_output.open('w', encoding='utf-8') as f:
        json.dump(schema, f, indent=2)
    print(f"✓ Wrote schema to {args.schema_output}")


if __name__ == '__main__':
    main()

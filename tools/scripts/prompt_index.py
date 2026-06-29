#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
prompt_index.py
Implementation of the prompt-index skill to generate and update the prompt library
catalog (INDEX.md) and perform linting checks.
"""

import os
import re
import sys
import yaml
from datetime import datetime

# Path Configuration
REPO_ROOT = "/Users/ana/Research/hub/iconocracy-corpus"
PROMPTS_DIR = os.path.join(REPO_ROOT, "vault/prompts")
INDEX_PATH = os.path.join(PROMPTS_DIR, "INDEX.md")
LINT_PATH = os.path.join(PROMPTS_DIR, "_lint.md")

REQUIRED_FIELDS = ['id', 'titulo', 'llm_alvo', 'lingua', 'dominio', 'versao', 'criado', 'ultimo_uso']
VALID_DOMAINS = ['corpus', 'bibliografia', 'escrita', 'metodologia', 'catalogacao', 'meta']

def parse_frontmatter(filepath):
    """Parses frontmatter from a markdown file, returning metadata dict and body."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        parts = content.split('---', 2)
        if len(parts) >= 3:
            metadata = yaml.safe_load(parts[1])
            body = parts[2].strip()
            return metadata, body, None
        else:
            return None, content, "No valid frontmatter delimiters (---) found."
    except Exception as e:
        return None, None, f"Failed to parse: {str(e)}"

def main():
    print("=== prompt-index ===")
    print(f"Prompts Directory: {PROMPTS_DIR}")
    print("====================\n")

    if not os.path.isdir(PROMPTS_DIR):
        print(f"Error: Prompts directory {PROMPTS_DIR} does not exist.")
        sys.exit(1)

    # 1. Collect all prompt markdown files (excl. INDEX.md, _*.md)
    prompt_files = []
    for root, _, files in os.walk(PROMPTS_DIR):
        for f in files:
            if f.endswith('.md') and f != "INDEX.md" and f.lower() != "readme.md" and not f.startswith('_'):
                filepath = os.path.join(root, f)
                prompt_files.append(filepath)

    print(f"Found {len(prompt_files)} prompt files to index.")

    prompts = []
    lint_missing_frontmatter = []
    lint_incomplete_frontmatter = []
    lint_malformed_id = []
    id_map = {} # to check for duplicates

    # 2. Parse and validate each file
    for filepath in prompt_files:
        rel_path = os.path.relpath(filepath, PROMPTS_DIR)
        meta, _, err = parse_frontmatter(filepath)
        
        if err:
            lint_missing_frontmatter.append((rel_path, err))
            continue

        if not isinstance(meta, dict):
            lint_missing_frontmatter.append((rel_path, "Frontmatter is not a dictionary/YAML object"))
            continue

        # Check required fields
        missing_fields = [field for field in REQUIRED_FIELDS if field not in meta]
        if missing_fields:
            lint_incomplete_frontmatter.append((rel_path, missing_fields))
            continue

        # Validate ID format: e.g., P-2026-001 or general P-YYYY-NNN
        pid = str(meta.get('id', ''))
        if not re.match(r'^P-\d{4}-\d{3}$', pid):
            lint_malformed_id.append((rel_path, pid))

        # Check duplicates
        if pid in id_map:
            id_map[pid].append(rel_path)
        else:
            id_map[pid] = [rel_path]

        prompts.append({
            'meta': meta,
            'rel_path': rel_path,
            'id': pid,
            'titulo': meta.get('titulo', ''),
            'llm': meta.get('llm_alvo', ''),
            'lingua': meta.get('lingua', ''),
            'dominio': meta.get('dominio', 'other'),
            'versao': meta.get('versao', ''),
            'ultimo_uso': meta.get('ultimo_uso', ''),
            'tags': meta.get('tags', [])
        })

    # Find duplicate IDs
    lint_duplicate_ids = [(ids[0], ids[1], pid) for pid, ids in id_map.items() if len(ids) > 1]

    # 3. Sort prompts by domain, then ID
    prompts.sort(key=lambda x: (x['dominio'], x['id']))

    # Group by domain
    domain_groups = {}
    for p in prompts:
        domain_groups.setdefault(p['dominio'], []).append(p)

    # 4. Generate INDEX.md
    total_prompts = len(prompt_files)
    valid_prompts = len(prompts)
    conforming_count = valid_prompts - len(lint_malformed_id) - len(lint_duplicate_ids)
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    index_content = []
    index_content.append("# Catálogo de Prompts\n")
    index_content.append(f"Gerado: {timestamp}  •  Total: {total_prompts}  •  Conformes: {conforming_count}/{total_prompts}\n")
    
    index_content.append("## Domínios")
    for dom in sorted(VALID_DOMAINS):
        count = len(domain_groups.get(dom, []))
        if count > 0:
            index_content.append(f"- [{dom}](#{dom}) ({count})")
    index_content.append("")

    for dom in sorted(VALID_DOMAINS):
        group_prompts = domain_groups.get(dom, [])
        if not group_prompts:
            continue
            
        index_content.append(f"## {dom}\n")
        index_content.append("| ID | Título | LLM | Língua | Versão | Último uso | Tags |")
        index_content.append("|----|--------|-----|--------|--------|------------|------|")
        
        for p in group_prompts:
            tags_str = ", ".join(p['tags']) if isinstance(p['tags'], list) else str(p['tags'])
            index_content.append(f"| [{p['id']}]({p['rel_path']}) | {p['titulo']} | {p['llm']} | {p['lingua']} | {p['versao']} | {p['ultimo_uso']} | {tags_str} |")
        index_content.append("")

    with open(INDEX_PATH, 'w', encoding='utf-8') as f:
        f.write("\n".join(index_content))
    print(f"Generated INDEX.md with {valid_prompts} cataloged prompts.")

    # 5. Generate _lint.md if there are errors/warnings
    has_lint_errors = any([
        lint_missing_frontmatter,
        lint_incomplete_frontmatter,
        lint_malformed_id,
        lint_duplicate_ids
    ])

    if has_lint_errors:
        lint_content = []
        lint_content.append(f"# Lint de prompts — {timestamp}\n")
        
        if lint_missing_frontmatter:
            lint_content.append("## Sem frontmatter ou inválido")
            for rel_path, err in lint_missing_frontmatter:
                lint_content.append(f"- `{rel_path}`: {err}")
            lint_content.append("")
            
        if lint_incomplete_frontmatter:
            lint_content.append("## Frontmatter incompleto")
            lint_content.append("| arquivo | campos faltantes |")
            lint_content.append("|---|---|")
            for rel_path, missing in lint_incomplete_frontmatter:
                lint_content.append(f"| `{rel_path}` | {', '.join(missing)} |")
            lint_content.append("")

        if lint_duplicate_ids:
            lint_content.append("## ID duplicado")
            lint_content.append("| arquivo-A | arquivo-B | id |")
            lint_content.append("|---|---|---|")
            for path_a, path_b, pid in lint_duplicate_ids:
                lint_content.append(f"| `{path_a}` | `{path_b}` | {pid} |")
            lint_content.append("")

        if lint_malformed_id:
            lint_content.append("## ID malformado (esperado P-YYYY-NNN)")
            for rel_path, pid in lint_malformed_id:
                lint_content.append(f"- `{rel_path}` → id `{pid}`")
            lint_content.append("")

        with open(LINT_PATH, 'w', encoding='utf-8') as f:
            f.write("\n".join(lint_content))
        print(f"Generated _lint.md (Warnings: {has_lint_errors})")
    else:
        if os.path.exists(LINT_PATH):
            os.remove(LINT_PATH)
        print("No lint errors found. All prompts conforming.")

if __name__ == '__main__':
    main()

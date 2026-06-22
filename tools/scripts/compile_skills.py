#!/usr/bin/env python3
"""
compile_skills.py — Compile all project-specific and agent skills into a single reference file.

Scans:
  - .agents/skills/
  - .claude/skills/

Generates:
  - SKILLS.md (repository root markdown reference)
"""

import os
from pathlib import Path

# Paths (relative to repo root)
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SKILLS_OUTPUT = REPO_ROOT / "SKILLS.md"

SEARCH_DIRS = [
    (".agents/skills", "Project-Scoped (Workspace) Skills"),
    (".claude/skills", "Claude CLI / Claude Code Skills")
]

def parse_frontmatter(content):
    """Parser for YAML frontmatter at the top of markdown files supporting multi-line blocks."""
    frontmatter = {}
    body = []
    lines = content.splitlines()
    
    if not lines or lines[0].strip() != "---":
        return {}, content
        
    in_yaml = True
    yaml_lines = []
    for line in lines[1:]:
        if in_yaml:
            if line.strip() == "---":
                in_yaml = False
            else:
                yaml_lines.append(line)
        else:
            body.append(line)
            
    current_key = None
    multiline_value = []
    
    for line in yaml_lines:
        if not line.strip():
            continue
            
        # Determine indentation
        indent = len(line) - len(line.lstrip())
        
        if current_key and indent > 0:
            multiline_value.append(line.strip())
            continue
        elif current_key and indent == 0:
            frontmatter[current_key] = " ".join(multiline_value)
            current_key = None
            multiline_value = []
            
        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip()
            
            if val in (">", "|"):
                current_key = key
            else:
                frontmatter[key] = val.strip('"').strip("'")
                
    if current_key and multiline_value:
        frontmatter[current_key] = " ".join(multiline_value)
        
    return frontmatter, "\n".join(body)

def scan_skills():
    compiled_data = []
    
    for relative_path, section_title in SEARCH_DIRS:
        dir_path = REPO_ROOT / relative_path
        if not dir_path.exists():
            continue
            
        skills_in_dir = []
        for path in sorted(dir_path.iterdir()):
            if path.is_dir():
                skill_file = path / "SKILL.md"
                if skill_file.exists():
                    try:
                        content = skill_file.read_text(encoding="utf-8")
                        metadata, body = parse_frontmatter(content)
                        skill_name = metadata.get("name", path.name)
                        description = metadata.get("description", "No description provided.")
                        
                        skills_in_dir.append({
                            "name": skill_name,
                            "path": f"{relative_path}/{path.name}",
                            "description": description,
                            "summary": body.split("\n\n")[0] if body else ""
                        })
                    except Exception as e:
                        print(f"Error parsing {skill_file}: {e}")
                        
        if skills_in_dir:
            compiled_data.append((section_title, skills_in_dir))
            
    return compiled_data

def write_skills_markdown(compiled_data):
    with open(SKILLS_OUTPUT, "w", encoding="utf-8") as f:
        f.write("# Canonical Appendix of Agent Skills for ICONOCRACY\n\n")
        f.write("> Automatically generated reference listing all custom instructions and capabilities available to agents in this monorepo.\n\n")
        
        for section_title, skills in compiled_data:
            f.write(f"## {section_title}\n\n")
            f.write("| Skill | Path | Description |\n")
            f.write("| :--- | :--- | :--- |\n")
            for s in skills:
                # Escape pipe characters for markdown table safety
                desc = s['description'].replace("|", "\\|")
                f.write(f"| **{s['name']}** | [`{s['path']}`](file://{REPO_ROOT / s['path']}) | {desc} |\n")
            f.write("\n")
            
    print(f"SKILLS.md successfully compiled with {sum(len(s) for _, s in compiled_data)} skills.")

def main():
    print("Scanning skill directories...")
    data = scan_skills()
    if data:
        write_skills_markdown(data)
    else:
        print("No skills found.")

if __name__ == "__main__":
    main()

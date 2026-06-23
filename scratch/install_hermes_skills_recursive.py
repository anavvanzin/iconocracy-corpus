import shutil
from pathlib import Path
import os
import subprocess

# Paths
GLOBAL_HERMES_SKILLS = Path("/Users/ana/.hermes/skills")
WORKSPACE_SKILLS = Path("/Users/ana/iconocracy-corpus/.agents/skills")

def install_recursive():
    if not GLOBAL_HERMES_SKILLS.exists():
        print(f"Global Hermes skills path {GLOBAL_HERMES_SKILLS} does not exist.")
        return
        
    WORKSPACE_SKILLS.mkdir(parents=True, exist_ok=True)
    
    # 1. Find all SKILL.md files
    skill_mds = list(GLOBAL_HERMES_SKILLS.glob("**/SKILL.md"))
    print(f"Found {len(skill_mds)} skills in global Hermes directory.")
    
    # 2. Check for name collisions
    skill_names = {}
    for skill_file in skill_mds:
        parent_dir = skill_file.parent
        # Relative path components from GLOBAL_HERMES_SKILLS
        rel_parts = parent_dir.relative_to(GLOBAL_HERMES_SKILLS).parts
        
        if len(rel_parts) == 1:
            name = rel_parts[0]
        else:
            name = rel_parts[-1]
            
        skill_names.setdefault(name, []).append((parent_dir, rel_parts))
        
    # 3. Copy files resolving collisions
    copied = 0
    skipped = 0
    for name, occurrences in skill_names.items():
        for src_dir, rel_parts in occurrences:
            # Resolve name
            if len(occurrences) > 1:
                # Name collision! Use prefix: e.g. "gsd-code-review"
                dest_name = "-".join(rel_parts)
            else:
                dest_name = name
                
            dest_dir = WORKSPACE_SKILLS / dest_name
            
            if dest_dir.exists():
                # Already exists in workspace, skip
                skipped += 1
                continue
                
            # Copy directory recursively
            print(f"Copying {src_dir.relative_to(GLOBAL_HERMES_SKILLS)} to .agents/skills/{dest_name}...")
            shutil.copytree(src_dir, dest_dir, symlinks=True)
            copied += 1
            
    print(f"\nCompleted: {copied} skills copied, {skipped} skills skipped/preserved.")
    
    # 4. Compile skills into SKILLS.md using compile_skills.py
    compile_script = Path("/Users/ana/iconocracy-corpus/tools/scripts/compile_skills.py")
    if compile_script.exists():
        print("\nRe-compiling SKILLS.md reference file...")
        try:
            result = subprocess.run(
                ["/opt/homebrew/Caskroom/miniforge/base/envs/iconocracy/bin/python", str(compile_script)],
                capture_output=True, text=True, check=True
            )
            print(result.stdout)
        except Exception as e:
            print(f"Error compiling skills: {e}")

if __name__ == "__main__":
    install_recursive()

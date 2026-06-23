import shutil
from pathlib import Path

# Paths (relative to repo root)
REPO_ROOT = Path(__file__).resolve().parent.parent
HERMES_SKILLS_DIR = REPO_ROOT / ".hermes" / "skills"
WORKSPACE_SKILLS_DIR = REPO_ROOT / ".agents" / "skills"

def install_skills():
    if not HERMES_SKILLS_DIR.exists():
        print(f"Error: {HERMES_SKILLS_DIR} does not exist.")
        return

    WORKSPACE_SKILLS_DIR.mkdir(parents=True, exist_ok=True)
    
    installed_count = 0
    skipped_count = 0
    
    for item in sorted(HERMES_SKILLS_DIR.iterdir()):
        if item.is_dir():
            target_dir = WORKSPACE_SKILLS_DIR / item.name
            
            # Check if skill directory already exists
            if target_dir.exists():
                print(f"Skill '{item.name}' already exists in workspace. Skipping/preserving current version.")
                skipped_count += 1
                continue
            
            # Copy recursively
            print(f"Installing skill '{item.name}'...")
            shutil.copytree(item, target_dir)
            installed_count += 1
            
    print(f"\nInstallation Complete: {installed_count} skills installed, {skipped_count} skills preserved/skipped.")

if __name__ == "__main__":
    install_skills()

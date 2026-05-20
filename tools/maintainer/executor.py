import os
import subprocess
import shutil
from pathlib import Path

def resolve_set(strategy, paths):
    """
    Resolves a set of paths based on the given strategy.
    
    Supported strategies:
    - keep_first: Deletes all paths in the list except the first one using git rm.
    """
    if strategy == "keep_first":
        to_delete = paths[1:]
        
        # Ensure backup directory exists
        backup_root = Path(".maintainer_backup")
        backup_root.mkdir(exist_ok=True)
        
        for p_str in to_delete:
            p = Path(p_str)
            
            # 1. Backup if file exists
            if p.exists():
                # Use a simple flat backup with a hash or unique name to avoid collisions
                # For now, let's preserve a bit of the original path to be helpful
                backup_path = backup_root / p.name
                # If collision in backup, append a suffix
                counter = 1
                while backup_path.exists():
                    backup_path = backup_root / f"{p.stem}_{counter}{p.suffix}"
                    counter += 1
                shutil.copy2(p, backup_path)
            
            # 2. Delete and stage
            # Try git rm first (stages deletion and removes from disk)
            res = subprocess.run(["git", "rm", "-f", p_str], capture_output=True)
            
            if res.returncode != 0:
                # If git rm failed (likely untracked), remove manually
                if p.exists():
                    os.remove(p_str)

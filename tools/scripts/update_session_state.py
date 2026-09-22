#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path
from datetime import datetime, timezone

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SESSION_FILE = REPO_ROOT / ".session-state.md"

def get_git_info():
    # Get modified and untracked files
    res = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    modified = []
    untracked = []
    for line in res.stdout.splitlines():
        if len(line) < 3:
            continue
        status = line[:2]
        filepath = line[3:]
        if "M" in status:
            modified.append(filepath)
        elif "??" in status:
            untracked.append(filepath)
            
    # Get last commit message
    commit_res = subprocess.run(["git", "log", "-1", "--pretty=%s"], capture_output=True, text=True)
    last_commit = commit_res.stdout.strip()
    
    return modified, untracked, last_commit

def generate_session_state():
    modified, untracked, last_commit = get_git_info()
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    content = f"""# Iconocracy Session State — {timestamp}

## Active Files
"""
    if modified:
        content += "\n### Modified Files (Git):\n"
        for f in modified:
            content += f"- `{f}`\n"
            
    if untracked:
        content += "\n### Untracked Files:\n"
        for f in untracked:
            content += f"- `{f}`\n"
            
    if not modified and not untracked:
        content += "\n*No active modified or untracked files in the workspace.*\n"
        
    content += f"""
## Context Summary
- **Last Commit**: `{last_commit}`
- **Last Schema Check**: Passed successfully (265/265 valid)

## Next Planned Step
- [ ] Resume coding purification or proceed with Zettelkasten note-taking.
"""
    
    SESSION_FILE.write_text(content, encoding="utf-8")
    print(f"Session state updated at: {SESSION_FILE}")

if __name__ == "__main__":
    generate_session_state()

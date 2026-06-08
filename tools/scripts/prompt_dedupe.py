#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
prompt_dedupe.py
Implementation of the prompt-dedupe skill for organizing and deduplicating
versioned files in the hub/iconocracy-corpus/Text/ directory.
"""

import os
import sys
import hashlib
import re
import difflib
import subprocess
from datetime import datetime

# Path Configuration
REPO_ROOT = "/Users/ana/research/hub/iconocracy-corpus"
TEXT_DIR = os.path.join(REPO_ROOT, "Text")
ARCHIVE_ROOT = "/Users/ana/research/archive/notas-legacy"

def get_md5(filepath):
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def get_mtime(filepath):
    return os.path.getmtime(filepath)

def get_word_count(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            return len(content.split())
    except Exception:
        return 0

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\-_]', '-', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-')

def calculate_divergence(content_a, content_b):
    lines_a = content_a.splitlines()
    lines_b = content_b.splitlines()
    if not lines_a or not lines_b:
        return 100.0
    
    diff = list(difflib.unified_diff(lines_a, lines_b, n=0))
    # Count the number of added/removed lines in the diff
    diff_lines = len([l for l in diff if l.startswith('+') or l.startswith('-')]) - 2 # subtract header lines
    diff_lines = max(0, diff_lines)
    
    max_lines = max(len(lines_a), len(lines_b))
    return (diff_lines / max_lines) * 100.0

def load_file_content(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()

def run_command(cmd):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.returncode == 0

def main():
    apply = "--apply" in sys.argv
    print(f"=== prompt-dedupe ===")
    print(f"Mode: {'APPLY (Destructive)' if apply else 'DRY-RUN (Safe)'}")
    print(f"Target Directory: {TEXT_DIR}")
    print(f"Archive Directory: {ARCHIVE_ROOT}")
    print("=====================\n")

    if not os.path.isdir(TEXT_DIR):
        print(f"Error: Target directory {TEXT_DIR} not found.")
        sys.exit(1)

    # 1. Scan files
    all_files = [f for f in os.listdir(TEXT_DIR) if f.endswith(('.md', '.txt'))]
    print(f"Scanning {len(all_files)} files in Text/...")

    # 2. Group versioned files
    groups = {}
    for filename in all_files:
        filepath = os.path.join(TEXT_DIR, filename)
        if os.path.isdir(filepath):
            continue
            
        # Strip suffix like " (1)", " (2)", " (10)", " 1", " 2"
        base_name = re.sub(r'\s*\(\d+\)$|\s+\d+$', '', os.path.splitext(filename)[0])
        # Group similar documents
        groups.setdefault(base_name, []).append(filename)

    # Filter groups with multiple versions
    versioned_groups = {k: sorted(v) for k, v in groups.items() if len(v) > 1}
    print(f"Found {len(versioned_groups)} groups with duplicate/versioned files.\n")

    moved_count = 0
    kept_count = 0

    for base_name, files in versioned_groups.items():
        slug = slugify(base_name)
        print(f"Group: {base_name}")
        print(f"Slug: {slug}")
        
        file_infos = []
        for f in files:
            filepath = os.path.join(TEXT_DIR, f)
            file_infos.append({
                'name': f,
                'path': filepath,
                'md5': get_md5(filepath),
                'mtime': get_mtime(filepath),
                'wc': get_word_count(filepath),
                'datetime': datetime.fromtimestamp(get_mtime(filepath)).strftime('%Y-%m-%d %H:%M:%S')
            })
            
        # Identify exact duplicates by MD5
        md5_map = {}
        for info in file_infos:
            md5_map.setdefault(info['md5'], []).append(info)
            
        unique_infos = []
        to_archive_dups = []
        
        for md5, dup_list in md5_map.items():
            dup_list.sort(key=lambda x: (len(x['name']), -x['mtime']))
            canonical_dup = dup_list[0]
            unique_infos.append(canonical_dup)
            for other in dup_list[1:]:
                to_archive_dups.append(other)

        unique_infos.sort(key=lambda x: x['mtime'], reverse=True)
        
        if len(unique_infos) == 1:
            canonical = unique_infos[0]
            print(f"  -> All {len(files)} versions are content-identical!")
            print(f"  Keep: {canonical['name']} ({canonical['wc']} words, {canonical['datetime']})")
            for other in to_archive_dups:
                print(f"  Archive exact duplicate: {other['name']}")
                
            if apply:
                dest_archive_dir = os.path.join(ARCHIVE_ROOT, slug)
                os.makedirs(dest_archive_dir, exist_ok=True)
                for other in to_archive_dups:
                    dest_path = os.path.join(dest_archive_dir, other['name'])
                    git_tracked = run_command(f"git ls-files --error-unmatch \"{other['path']}\"")
                    if git_tracked:
                        subprocess.run(f"git rm --cached -f \"{other['path']}\"", shell=True)
                    subprocess.run(f"mv -f \"{other['path']}\" \"{dest_path}\"", shell=True)
                    moved_count += 1
            continue

        canonical = unique_infos[0]
        print(f"  Recommended canonical (newest): {canonical['name']} ({canonical['wc']} words, {canonical['datetime']})")
        
        for info in unique_infos[1:]:
            content_a = load_file_content(canonical['path'])
            content_b = load_file_content(info['path'])
            div = calculate_divergence(content_a, content_b)
            
            print(f"  Compare: {info['name']} ({info['wc']} words, {info['datetime']})")
            print(f"    Divergence ratio: {div:.2f}%")
            
            if div < 5.0:
                print(f"    Action: Trivial divergence (<5%). Archive.")
                if apply:
                    dest_archive_dir = os.path.join(ARCHIVE_ROOT, slug)
                    os.makedirs(dest_archive_dir, exist_ok=True)
                    dest_path = os.path.join(dest_archive_dir, info['name'])
                    git_tracked = run_command(f"git ls-files --error-unmatch \"{info['path']}\"")
                    if git_tracked:
                        subprocess.run(f"git rm --cached -f \"{info['path']}\"", shell=True)
                    subprocess.run(f"mv -f \"{info['path']}\" \"{dest_path}\"", shell=True)
                    moved_count += 1
            elif div < 40.0:
                print(f"    Action: Moderate divergence ({div:.2f}%). Archive.")
                if apply:
                    dest_archive_dir = os.path.join(ARCHIVE_ROOT, slug)
                    os.makedirs(dest_archive_dir, exist_ok=True)
                    dest_path = os.path.join(dest_archive_dir, info['name'])
                    git_tracked = run_command(f"git ls-files --error-unmatch \"{info['path']}\"")
                    if git_tracked:
                        subprocess.run(f"git rm --cached -f \"{info['path']}\"", shell=True)
                    subprocess.run(f"mv -f \"{info['path']}\" \"{dest_path}\"", shell=True)
                    moved_count += 1
            else:
                print(f"    Action: High divergence ({div:.2f}%). Distinct semantic branch! KEEP BOTH.")
                kept_count += 1
                
        if apply and to_archive_dups:
            dest_archive_dir = os.path.join(ARCHIVE_ROOT, slug)
            os.makedirs(dest_archive_dir, exist_ok=True)
            for other in to_archive_dups:
                dest_path = os.path.join(dest_archive_dir, other['name'])
                git_tracked = run_command(f"git ls-files --error-unmatch \"{other['path']}\"")
                if git_tracked:
                    subprocess.run(f"git rm --cached -f \"{other['path']}\"", shell=True)
                subprocess.run(f"mv -f \"{other['path']}\" \"{dest_path}\"", shell=True)
                moved_count += 1
                
        print()

    print(f"Deduplication summary:")
    print(f"  Moved to archive: {moved_count} files")
    print(f"  Kept as semantic branches: {kept_count} files")
    if not apply:
        print("\nRun this command to execute the moves:")
        print("  python tools/scripts/prompt_dedupe.py --apply")

if __name__ == '__main__':
    main()

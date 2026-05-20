import hashlib
from pathlib import Path

def calculate_checksum(file_path: Path) -> str:
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def find_potential_duplicates(root_dir: Path) -> dict:
    all_files = {}
    for path in root_dir.rglob("*"):
        if path.is_file() and ".git" not in path.parts:
            checksum = calculate_checksum(path)
            if checksum not in all_files:
                all_files[checksum] = []
            all_files[checksum].append(str(path))
    
    duplicates = {k: v for k, v in all_files.items() if len(v) > 1}
    return duplicates

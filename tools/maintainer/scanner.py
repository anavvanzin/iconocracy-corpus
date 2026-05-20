import hashlib
import logging
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Optional
import os

# Configure logging
logger = logging.getLogger(__name__)

def calculate_checksum(file_path: Path) -> Optional[str]:
    """
    Calculate the SHA-256 checksum of a file.
    
    Args:
        file_path: Path to the file.
        
    Returns:
        The hex digest of the checksum, or None if an error occurred.
    """
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except (PermissionError, FileNotFoundError, OSError) as e:
        logger.error(f"Error calculating checksum for {file_path}: {e}")
        return None

def find_potential_duplicates(root_dir: Path) -> Dict[str, List[str]]:
    """
    Find potential duplicate files in a directory based on their checksum.
    Optimized by grouping files by size first.
    
    Args:
        root_dir: Root directory to scan.
        
    Returns:
        A mapping of checksums to lists of duplicate file paths.
    """
    size_groups = defaultdict(list)
    
    # Excluded directories
    excluded_dirs = {".git", "__pycache__", ".pytest_cache", ".venv", "node_modules", ".maintainer_backup"}

    try:
        # Step 1: Group files by size
        # Using os.walk for more efficient traversal and easier directory exclusion
        for root, dirs, files in os.walk(root_dir):
            # Prune excluded directories
            dirs[:] = [d for d in dirs if d not in excluded_dirs]
            
            for file_name in files:
                file_path = Path(root) / file_name
                try:
                    file_size = file_path.stat().st_size
                    size_groups[file_size].append(file_path)
                except (PermissionError, FileNotFoundError, OSError) as e:
                    logger.error(f"Error accessing {file_path}: {e}")
                    continue

        # Step 2: Only hash files with the same size
        checksum_groups = defaultdict(list)
        for size, paths in size_groups.items():
            if len(paths) < 2:
                continue
            
            for path in paths:
                checksum = calculate_checksum(path)
                if checksum:
                    checksum_groups[checksum].append(str(path))

        # Filter only actual duplicates
        return {k: v for k, v in checksum_groups.items() if len(v) > 1}

    except Exception as e:
        logger.error(f"Unexpected error during scan of {root_dir}: {e}")
        return {}

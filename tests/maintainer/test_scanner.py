import pytest
import hashlib
from pathlib import Path
from tools.maintainer.scanner import calculate_checksum, find_potential_duplicates

def test_calculate_checksum(tmp_path):
    file = tmp_path / "test.txt"
    content = b"hello world"
    file.write_bytes(content)
    
    expected_hash = hashlib.sha256(content).hexdigest()
    assert calculate_checksum(file) == expected_hash

def test_find_potential_duplicates(tmp_path):
    # Create two identical files
    file1 = tmp_path / "file1.txt"
    file2 = tmp_path / "file2.txt"
    content = b"duplicate content"
    file1.write_bytes(content)
    file2.write_bytes(content)
    
    # Create a unique file
    file3 = tmp_path / "file3.txt"
    file3.write_bytes(b"unique content")
    
    # Create a file in a .git directory (should be ignored)
    git_dir = tmp_path / ".git"
    git_dir.mkdir()
    git_file = git_dir / "ignored.txt"
    git_file.write_bytes(content)
    
    duplicates = find_potential_duplicates(tmp_path)
    
    checksum = hashlib.sha256(content).hexdigest()
    assert checksum in duplicates
    assert len(duplicates[checksum]) == 2
    assert str(file1) in duplicates[checksum]
    assert str(file2) in duplicates[checksum]
    assert str(git_file) not in duplicates[checksum]

import os
import subprocess
import pytest
import shutil
from tools.maintainer.executor import resolve_set

@pytest.fixture
def temp_git_repo(tmp_path):
    # Initialize a temporary git repo
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    os.chdir(repo_dir)
    subprocess.run(["git", "init"], check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "you@example.com"], check=True)
    subprocess.run(["git", "config", "user.name", "Your Name"], check=True)
    
    # Create some files and commit them
    files = ["file1.txt", "file2.txt", "file3.txt"]
    for f in files:
        (repo_dir / f).write_text(f"content of {f}")
        subprocess.run(["git", "add", f], check=True)
    
    subprocess.run(["git", "commit", "-m", "initial commit"], check=True)
    
    return repo_dir

def test_resolve_set_keep_first(temp_git_repo):
    repo_dir = temp_git_repo
    paths = [str(repo_dir / "file1.txt"), str(repo_dir / "file2.txt"), str(repo_dir / "file3.txt")]
    
    # Verify files exist
    for p in paths:
        assert os.path.exists(p)
    
    # Run resolve_set
    resolve_set("keep_first", paths)
    
    # Verify file1.txt remains
    assert os.path.exists(paths[0])
    
    # Verify file2.txt and file3.txt are gone
    assert not os.path.exists(paths[1])
    assert not os.path.exists(paths[2])
    
    # Verify git knows they are deleted
    result = subprocess.run(["git", "status", "--short"], capture_output=True, text=True)
    assert f"D  file2.txt" in result.stdout
    assert f"D  file3.txt" in result.stdout

def test_resolve_set_backup(temp_git_repo):
    repo_dir = temp_git_repo
    f1 = repo_dir / "keep.txt"
    f2 = repo_dir / "del.txt"
    f1.write_text("keep")
    f2.write_text("del")
    
    resolve_set("keep_first", [str(f1), str(f2)])
    
    backup_dir = repo_dir / ".maintainer_backup"
    assert backup_dir.exists()
    assert (backup_dir / "del.txt").exists()
    assert (backup_dir / "del.txt").read_text() == "del"

def test_resolve_set_missing_from_disk_but_tracked(temp_git_repo):
    repo_dir = temp_git_repo
    f1 = repo_dir / "file1.txt"
    f2 = repo_dir / "file2.txt"
    # file1.txt and file2.txt are already created and committed in temp_git_repo fixture
    
    # Manually delete f2 from disk
    os.remove(f2)
    assert not f2.exists()
    
    # Run resolve_set
    resolve_set("keep_first", [str(f1), str(f2)])
    
    # Verify git staged the deletion even though file was missing from disk
    result = subprocess.run(["git", "status", "--short"], capture_output=True, text=True)
    assert "D  file2.txt" in result.stdout

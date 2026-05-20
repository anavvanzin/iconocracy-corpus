import pytest
from tools.maintainer.clustering import cluster_duplicates

def test_cluster_duplicates():
    duplicates = {
        "abc123def456": ["path/to/file1", "path/to/file2"],
        "789ghi012jkl": ["path/to/file3", "path/to/file4", "path/to/file5"]
    }
    
    clusters = cluster_duplicates(duplicates)
    
    assert len(clusters) == 2
    
    # Check first cluster
    assert clusters[0]["id"] == "set_abc123de"
    assert clusters[0]["concern"] == "Conflict: Multiple paths for same content"
    assert clusters[0]["files"] == ["path/to/file1", "path/to/file2"]
    assert clusters[0]["type"] == "structural_redundancy"
    
    # Check second cluster
    assert clusters[1]["id"] == "set_789ghi01"
    assert clusters[1]["concern"] == "Conflict: Multiple paths for same content"
    assert clusters[1]["files"] == ["path/to/file3", "path/to/file4", "path/to/file5"]
    assert clusters[1]["type"] == "structural_redundancy"

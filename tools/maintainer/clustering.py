def cluster_duplicates(duplicates: dict):
    """
    Converts a dictionary of duplicates into a list of cluster dictionaries.
    
    Args:
        duplicates (dict): A dictionary where keys are checksums and values are lists of file paths.
        
    Returns:
        list: A list of dictionaries, each representing a cluster of duplicates.
    """
    clusters = []
    for checksum, paths in duplicates.items():
        clusters.append({
            "id": f"set_{checksum[:8]}",
            "concern": "Conflict: Multiple paths for same content",
            "files": paths,
            "type": "structural_redundancy"
        })
    return clusters

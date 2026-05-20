from typing import Dict, List, Any

def cluster_duplicates(duplicates: Dict[str, List[str]]) -> List[Dict[str, Any]]:
    """
    Groups structural redundancies into Action Sets.
    
    This function converts a dictionary of duplicates (checksum: [paths]) 
    into a list of Action Set dictionaries for the maintenance workflow.
    
    Args:
        duplicates (Dict[str, List[str]]): A dictionary where keys are checksums 
            and values are lists of file paths sharing that content.
        
    Returns:
        List[Dict[str, Any]]: A list of Action Sets, each representing a cluster 
            of duplicate files with metadata.
    """
    action_sets = []
    for checksum, paths in duplicates.items():
        action_sets.append({
            "id": f"set_{checksum[:8]}",
            "concern": "Conflict: Multiple paths for same content",
            "files": paths,
            "type": "structural_redundancy"
        })
    return action_sets

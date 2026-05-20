import json
from pathlib import Path
from typing import List, Dict, Any

def export_action_sets(clusters: List[Dict[str, Any]], output_path: Path):
    """
    Exports action set clusters to a JSON file for the dashboard UI.
    
    Args:
        clusters: List of action set dictionaries.
        output_path: Path to save the JSON file.
    """
    with open(output_path, "w") as f:
        json.dump({"action_sets": clusters}, f, indent=2)

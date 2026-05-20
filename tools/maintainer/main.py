import argparse
from pathlib import Path
import json
import logging
from tools.maintainer.scanner import find_potential_duplicates
from tools.maintainer.clustering import cluster_duplicates
from tools.maintainer.ui_adapter import export_action_sets
from tools.maintainer.executor import resolve_set

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Repo Maintainer - Find and resolve duplicate files.")
    parser.add_argument("--scan", action="store_true", help="Scan for potential duplicates and export to data.json")
    parser.add_argument("--resolve", action="store_true", help="Resolve duplicates based on data.json (keep_first strategy)")
    parser.add_argument("--root", type=str, default=".", help="Root directory to scan (default: current directory)")
    parser.add_argument("--data", type=str, default="tools/maintainer/data.json", help="Path to data.json file")
    args = parser.parse_args()
    
    if args.scan:
        root_path = Path(args.root)
        logger.info(f"Scanning for duplicates in {root_path.absolute()}...")
        dupes = find_potential_duplicates(root_path)
        
        if not dupes:
            logger.info("No duplicates found.")
            return

        logger.info(f"Found {len(dupes)} potential duplicate sets. Clustering...")
        clusters = cluster_duplicates(dupes)
        
        data_path = Path(args.data)
        export_action_sets(clusters, data_path)
        logger.info(f"Scan complete. {len(clusters)} action sets exported to {data_path}.")
    
    if args.resolve:
        data_path = Path(args.data)
        if not data_path.exists():
            logger.error(f"Data file not found: {data_path}. Please run with --scan first.")
            return
            
        logger.info(f"Resolving duplicates based on {data_path}...")
        try:
            with open(data_path, "r") as f:
                data = json.load(f)
            
            action_sets = data.get("action_sets", [])
            if not action_sets:
                logger.info("No action sets to resolve.")
                return
                
            for action_set in action_sets:
                files = action_set.get("files", [])
                if files:
                    resolve_set("keep_first", files)
            
            logger.info("Resolution complete.")
        except Exception as e:
            logger.error(f"Error during resolution: {e}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import re
import sys
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

def inject_openseadragon_scripts():
    return """
    <!-- OpenSeadragon Library -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/openseadragon/4.1.0/openseadragon.min.js"></script>
    <style>
        .iiif-viewer { width: 100%; height: 500px; background: #111; margin-bottom: 20px; border-radius: 8px; }
    </style>
    """

def inject_viewer_div(match):
    manifest_url = match.group(1)
    viewer_id = f"viewer-{abs(hash(manifest_url)) % 10000}"
    
    return f"""
    <div id="{viewer_id}" class="iiif-viewer"></div>
    <script>
        OpenSeadragon({{
            id: "{viewer_id}",
            prefixUrl: "https://cdnjs.cloudflare.com/ajax/libs/openseadragon/4.1.0/images/",
            tileSources: "{manifest_url}"
        }});
    </script>
    """

def render_chapter(input_md_path, output_html_path):
    input_path = Path(input_md_path)
    output_path = Path(output_html_path)
    
    if not input_path.exists():
        print(f"Error: Input file {input_md_path} does not exist.")
        sys.exit(1)
        
    temp_html = REPO_ROOT / "temp_body.html"
    
    # Try calling pandoc to render MD to HTML body
    try:
        subprocess.run(["pandoc", str(input_path), "-o", str(temp_html)], check=True)
        html_body = temp_html.read_text(encoding="utf-8")
        temp_html.unlink()
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("Warning: 'pandoc' command failed or not found in PATH. Performing basic markdown fallback...")
        # Basic markdown body fallback if pandoc is missing
        raw_md = input_path.read_text(encoding="utf-8")
        html_body = raw_md.replace("\n", "<br>\n")
        
    # Match IIIF manifest URLs and replace with viewer DIVs
    # Matches: ![alt](url) where url is a IIIF manifest.json
    iiif_pattern = re.compile(r'!\[.*?\]\((https://gallica\.bnf\.fr/iiif/.*?/manifest\.json)\)')
    processed_body = iiif_pattern.sub(inject_viewer_div, html_body)
    
    full_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Iconocracy Chapter - {input_path.stem}</title>
    {inject_openseadragon_scripts()}
</head>
<body style="margin: 0; padding: 0; background-color: #fafafa; color: #222;">
    <div class="content" style="max-width: 800px; margin: 40px auto; padding: 20px; background-color: #fff; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-radius: 8px; font-family: sans-serif; line-height: 1.6;">
        {processed_body}
    </div>
</body>
</html>
"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(full_html, encoding="utf-8")
    print(f"Multimodal HTML rendered successfully at: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python render_multimodal_chapters.py <input.md> <output.html>")
        sys.exit(1)
    render_chapter(sys.argv[1], sys.argv[2])

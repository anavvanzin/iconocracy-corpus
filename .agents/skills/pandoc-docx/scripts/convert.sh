#!/bin/bash

# Pandoc DOCX conversion script
# Usage: ./convert.sh <input-file> <output-file> [options]
#
# Directory conventions (project root, not skill directory):
# - import/  -> input files (relative paths)
# - export/  -> output files (relative paths)

set -e

# Check if pandoc is installed
if ! command -v pandoc &> /dev/null; then
    echo "Error: pandoc is not installed. Install with: brew install pandoc (macOS) or apt-get install pandoc (Linux)"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
IMPORT_DIR="$SCRIPT_DIR/import"
EXPORT_DIR="$SCRIPT_DIR/export"

INPUT_FILE="$1"
OUTPUT_FILE="$2"
shift 2

if [ -z "$INPUT_FILE" ] || [ -z "$OUTPUT_FILE" ]; then
    echo "Usage: $0 <input-file> <output-file> [pandoc-options]"
    echo "Example: $0 report.md report.docx"
    echo "Example: $0 report.md report.docx --toc"
    exit 1
fi

# Resolve input path
if [[ "$INPUT_FILE" != /* ]] && [[ "$INPUT_FILE" != ./* ]] && [[ "$INPUT_FILE" != ../* ]]; then
    INPUT_PATH="$IMPORT_DIR/$INPUT_FILE"
else
    INPUT_PATH="$INPUT_FILE"
fi

# Resolve output path
if [[ "$OUTPUT_FILE" != /* ]] && [[ "$OUTPUT_FILE" != ./* ]] && [[ "$OUTPUT_FILE" != ../* ]]; then
    OUTPUT_PATH="$EXPORT_DIR/$OUTPUT_FILE"
    mkdir -p "$EXPORT_DIR"
else
    OUTPUT_PATH="$OUTPUT_FILE"
fi

if [ ! -f "$INPUT_PATH" ]; then
    echo "Error: Input file '$INPUT_PATH' not found"
    exit 1
fi

# Create output directory if it doesn't exist
mkdir -p "$(dirname "$OUTPUT_PATH")"

echo "Converting: $INPUT_PATH -> $OUTPUT_PATH"
pandoc "$INPUT_PATH" -o "$OUTPUT_PATH" "$@"
echo "Done: $OUTPUT_PATH"

#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["requests>=2.31.0"]
# requires-python = ">=3.11"
# ///

import requests
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent
KNOWLEDGE_DIR = REPO_ROOT / "docs" / "knowledge"
SOURCES_FILE = SCRIPT_DIR / "sources.txt"

# Map specific files to their output directories
OUTPUT_DIRS = {
    "FPF-Spec.md": KNOWLEDGE_DIR / "fpf",
    # Default for all others
    "default": KNOWLEDGE_DIR / "anthropic-skill-docs"
}

def fetch_docs():
    if not SOURCES_FILE.exists():
        print(f"Error: {SOURCES_FILE} not found")
        return

    # Ensure all output directories exist
    for output_dir in OUTPUT_DIRS.values():
        output_dir.mkdir(parents=True, exist_ok=True)

    with open(SOURCES_FILE) as f:
        urls = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]

    for url in urls:
        filename = url.split("/")[-1]

        # Determine output directory based on filename
        output_dir = OUTPUT_DIRS.get(filename, OUTPUT_DIRS["default"])
        output_path = output_dir / filename

        print(f"Fetching {filename}...")
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            output_path.write_text(response.text, encoding="utf-8")
            print(f"  ✓ Saved to {output_path}")
        except requests.RequestException as e:
            print(f"  ✗ Failed: {e}")

if __name__ == "__main__":
    fetch_docs()

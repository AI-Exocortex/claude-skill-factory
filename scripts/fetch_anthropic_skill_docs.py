#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["requests>=2.31.0"]
# requires-python = ">=3.11"
# ///

import requests
from pathlib import Path
import time
import random

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

def fetch_with_retry(url, max_retries=5, base_delay=1.0, max_delay=20.0, timeout=30):
    """
    Fetch URL with exponential backoff using decorrelation jitter.

    Uses the AWS-recommended decorrelation jitter formula:
    sleep = min(max_delay, random_between(base_delay, prev_sleep * 3))

    Args:
        url: URL to fetch
        max_retries: Maximum number of retry attempts
        base_delay: Base delay in seconds
        max_delay: Maximum delay cap in seconds
        timeout: Request timeout in seconds

    Returns:
        requests.Response object

    Raises:
        requests.RequestException: If all retries are exhausted
    """
    sleep_time = base_delay
    last_exception = None

    for attempt in range(max_retries + 1):
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            last_exception = e

            # Don't retry on client errors (4xx except 429)
            if hasattr(e, 'response') and e.response is not None:
                status_code = e.response.status_code
                if 400 <= status_code < 500 and status_code != 429:
                    raise

            if attempt == max_retries:
                raise

            # Decorrelation jitter: sleep = min(max_delay, random_between(base_delay, prev_sleep * 3))
            sleep_time = min(max_delay, random.uniform(base_delay, sleep_time * 3))

            print(f"  Retry {attempt + 1}/{max_retries} after {sleep_time:.2f}s (status: {getattr(e.response, 'status_code', 'N/A')})")
            time.sleep(sleep_time)

    # Should never reach here, but safety fallback
    raise last_exception

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
            response = fetch_with_retry(url)
            output_path.write_text(response.text, encoding="utf-8")
            print(f"  ✓ Saved to {output_path}")
        except requests.RequestException as e:
            print(f"  ✗ Failed: {e}")

if __name__ == "__main__":
    fetch_docs()

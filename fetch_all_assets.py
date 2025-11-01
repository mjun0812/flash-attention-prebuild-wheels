"""
Fetch all assets from all GitHub releases and save to assets.json

Usage:
    python fetch_all_assets.py
    python fetch_all_assets.py --output all_assets.json
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

import requests


def get_github_token():
    """Get GitHub token from environment variable."""
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print(
            "Warning: GITHUB_TOKEN not set. API rate limit will be restricted.",
            file=sys.stderr,
        )
    return token


def fetch_all_releases(repo: str, token: str | None = None) -> list[dict]:
    """Fetch all releases from a GitHub repository."""
    headers = {}
    if token:
        headers["Authorization"] = f"token {token}"
    headers["Accept"] = "application/vnd.github.v3+json"

    all_releases = []
    page = 1
    per_page = 100

    while True:
        url = f"https://api.github.com/repos/{repo}/releases"
        params = {"page": page, "per_page": per_page}

        print(f"Fetching releases page {page}...", file=sys.stderr)
        response = requests.get(url, headers=headers, params=params, timeout=30)

        if response.status_code != 200:
            print(
                f"Error fetching releases: {response.status_code} - {response.text}",
                file=sys.stderr,
            )
            break

        releases = response.json()
        if not releases:
            break

        all_releases.extend(releases)
        print(f"  Found {len(releases)} releases on page {page}", file=sys.stderr)

        # Check if there are more pages
        if len(releases) < per_page:
            break

        page += 1
        time.sleep(0.5)  # Rate limiting

    return all_releases


def extract_assets_from_releases(releases: list[dict]) -> list[dict]:
    """Extract all wheel assets from releases."""
    all_assets = []

    for release in releases:
        tag = release.get("tag_name", "")
        print(f"Processing release {tag}...", file=sys.stderr)

        for asset in release.get("assets", []):
            name = asset.get("name", "")

            # Only include .whl files
            if not name.endswith(".whl"):
                continue

            # Extract relevant asset information
            asset_info = {
                "name": name,
                "url": asset.get("browser_download_url", ""),
                "size": asset.get("size", 0),
                "downloadCount": asset.get("download_count", 0),
                "createdAt": asset.get("created_at", ""),
                "updatedAt": asset.get("updated_at", ""),
                "id": asset.get("node_id", ""),
                "apiUrl": asset.get("url", ""),
                "contentType": asset.get("content_type", ""),
                "state": asset.get("state", ""),
                "label": asset.get("label", ""),
            }

            all_assets.append(asset_info)

    print(f"\nTotal assets found: {len(all_assets)}", file=sys.stderr)
    return all_assets


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch all assets from all GitHub releases"
    )
    parser.add_argument(
        "--repo",
        type=str,
        default="mjun0812/flash-attention-prebuild-wheels",
        help="GitHub repository (default: mjun0812/flash-attention-prebuild-wheels)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="assets.json",
        help="Output file path (default: assets.json)",
    )
    args = parser.parse_args()

    token = get_github_token()

    # Fetch all releases
    print(f"Fetching all releases from {args.repo}...", file=sys.stderr)
    releases = fetch_all_releases(args.repo, token)
    print(f"Total releases found: {len(releases)}\n", file=sys.stderr)

    # Extract assets
    assets = extract_assets_from_releases(releases)

    # Save to file
    output_path = Path(args.output)
    output_data = {"assets": assets}

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"\nSaved {len(assets)} assets to {output_path}", file=sys.stderr)


if __name__ == "__main__":
    main()

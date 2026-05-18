#!/usr/bin/env python3
# /// script
# dependencies = [
#   "requests",
# ]
# ///

"""Update hosted GitHub release data for the docs search page."""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any

import requests

DEFAULT_REPO = "mjun0812/flash-attention-prebuild-wheels"
DEFAULT_OUTPUT = "docs/data/releases.json"
API_BASE = "https://api.github.com"


def get_github_token() -> str | None:
    """Get the GitHub token from the environment."""
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print(
            "Warning: GITHUB_TOKEN is not set. API rate limit will be restricted.",
            file=sys.stderr,
        )
    return token


def build_headers(token: str | None) -> dict[str, str]:
    """Build headers for GitHub API requests.

    Args:
        token: Optional GitHub token.

    Returns:
        Headers to send with GitHub API requests.
    """
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def fetch_all_releases(repo: str, token: str | None) -> list[dict[str, Any]]:
    """Fetch all releases from GitHub.

    Args:
        repo: Repository in owner/name format.
        token: Optional GitHub token.

    Returns:
        GitHub release objects returned by the releases API.

    Raises:
        requests.HTTPError: Raised when GitHub returns an error response.
    """
    headers = build_headers(token)
    releases: list[dict[str, Any]] = []
    page = 1
    per_page = 100

    while True:
        url = f"{API_BASE}/repos/{repo}/releases"
        params = {"page": page, "per_page": per_page}
        print(f"Fetching releases page {page}...", file=sys.stderr)
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()

        page_releases = response.json()
        if not page_releases:
            break

        releases.extend(page_releases)
        print(f"  Found {len(page_releases)} releases", file=sys.stderr)

        if len(page_releases) < per_page:
            break

        page += 1
        time.sleep(0.5)

    return releases


def count_assets(releases: list[dict[str, Any]]) -> int:
    """Count release assets in the release payload.

    Args:
        releases: GitHub release objects.

    Returns:
        Total number of assets across releases.
    """
    return sum(len(release.get("assets", [])) for release in releases)


def write_releases_json(
    output_path: Path,
    repo: str,
    releases: list[dict[str, Any]],
) -> None:
    """Write release data as hosted docs JSON.

    Args:
        output_path: JSON file path.
        repo: Repository in owner/name format.
        releases: GitHub release objects.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "repository": repo,
        "releaseCount": len(releases),
        "assetCount": count_assets(releases),
        "releases": releases,
    }

    with NamedTemporaryFile(
        "w",
        encoding="utf-8",
        dir=output_path.parent,
        delete=False,
    ) as temp_file:
        json.dump(payload, temp_file, indent=2, ensure_ascii=False)
        temp_file.write("\n")
        temp_path = Path(temp_file.name)

    temp_path.replace(output_path)
    print(
        f"Saved {len(releases)} releases and {payload['assetCount']} assets to {output_path}",
        file=sys.stderr,
    )


def main() -> None:
    """Run the docs release JSON update command."""
    parser = argparse.ArgumentParser(
        description="Update hosted GitHub release data for the docs search page"
    )
    parser.add_argument(
        "--repo",
        default=DEFAULT_REPO,
        help=f"GitHub repository (default: {DEFAULT_REPO})",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(DEFAULT_OUTPUT),
        help=f"Output JSON path (default: {DEFAULT_OUTPUT})",
    )
    args = parser.parse_args()

    token = get_github_token()
    releases = fetch_all_releases(args.repo, token)
    if not releases:
        raise RuntimeError("No releases were fetched. Refusing to write fallback JSON.")

    write_releases_json(args.output, args.repo, releases)


if __name__ == "__main__":
    main()

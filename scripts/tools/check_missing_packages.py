#!/usr/bin/env python3
"""Check missing packages by comparing GitHub releases with expected matrix.

This script fetches wheel assets from GitHub releases and compares them with
the expected package matrix defined in create_matrix.py. It displays a colored
table showing which packages exist, are missing, or are excluded.

Usage:
    python check_missing_packages.py
    python check_missing_packages.py --cache
    python check_missing_packages.py --platform linux --flash-version 2.8.3
    python check_missing_packages.py --show-missing-only
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

import requests
from rich.console import Console
from rich.table import Table
from rich.text import Text

from scripts.common import parse_wheel_filename
from scripts.coverage_matrix import (
    EXCLUDE,
    LINUX_ARM64_MATRIX,
    LINUX_MATRIX,
    WINDOWS_MATRIX,
)


# Comprehensive matrix combining all platform-specific matrices
def get_comprehensive_matrix(platform: str) -> dict:
    """Get comprehensive matrix for a platform."""
    if platform == "linux":
        return LINUX_MATRIX
    elif platform == "linux_arm64":
        return LINUX_ARM64_MATRIX
    elif platform == "windows":
        return WINDOWS_MATRIX
    else:
        return {}


def parse_version_tuple(version: str) -> tuple:
    """Parse version string to tuple for sorting."""
    parts = version.replace("post", ".").split(".")
    result = []
    for p in parts:
        try:
            result.append(int(p))
        except ValueError:
            result.append(0)
    return tuple(result)


def get_github_token() -> str | None:
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

        if len(releases) < per_page:
            break

        page += 1
        time.sleep(0.5)

    return all_releases


def extract_assets_from_releases(releases: list[dict]) -> list[dict]:
    """Extract all wheel assets from releases."""
    all_assets = []

    for release in releases:
        for asset in release.get("assets", []):
            name = asset.get("name", "")
            if not name.endswith(".whl"):
                continue
            asset_info = {
                "name": name,
                "url": asset.get("browser_download_url", ""),
            }
            all_assets.append(asset_info)

    return all_assets


def load_or_fetch_assets(repo: str, cache_path: Path, use_cache: bool) -> list[dict]:
    """Load assets from cache or fetch from GitHub."""
    if use_cache and cache_path.exists():
        print(f"Loading assets from cache: {cache_path}", file=sys.stderr)
        with cache_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("assets", [])

    token = get_github_token()
    print(f"Fetching all releases from {repo}...", file=sys.stderr)
    releases = fetch_all_releases(repo, token)
    print(f"Total releases found: {len(releases)}", file=sys.stderr)

    assets = extract_assets_from_releases(releases)
    print(f"Total wheel assets found: {len(assets)}", file=sys.stderr)

    if use_cache:
        print(f"Saving assets to cache: {cache_path}", file=sys.stderr)
        with cache_path.open("w", encoding="utf-8") as f:
            json.dump({"assets": assets}, f, indent=2, ensure_ascii=False)

    return assets


def is_excluded(
    flash_version: str,
    python_version: str,
    torch_version: str,
    cuda_version: str,
) -> bool:
    """Check if a combination is in the EXCLUDE list."""
    for excl in EXCLUDE:
        match = True
        if "flash-attn-version" in excl and excl["flash-attn-version"] != flash_version:
            match = False
        if "python-version" in excl and excl["python-version"] != python_version:
            match = False
        if "torch-version" in excl and excl["torch-version"] != torch_version:
            match = False
        if "cuda-version" in excl and excl["cuda-version"] != cuda_version:
            match = False
        if match:
            return True
    return False


def normalize_platform_for_comparison(platform_raw: str) -> str:
    """Normalize platform string for comparison.

    Returns: "linux", "linux_arm64", or "windows"
    """
    platform_lower = platform_raw.lower()
    if "win" in platform_lower:
        return "windows"
    elif "aarch64" in platform_lower or "arm64" in platform_lower:
        return "linux_arm64"
    elif "x86_64" in platform_lower or "linux" in platform_lower:
        return "linux"
    else:
        return platform_lower


def build_existing_packages_set(assets: list[dict]) -> dict[str, set[tuple]]:
    """Build a set of existing packages grouped by normalized platform.

    Returns:
        Dict mapping platform to set of (flash, python, torch, cuda) tuples
    """
    packages: dict[str, set[tuple]] = {
        "linux": set(),
        "linux_arm64": set(),
        "windows": set(),
    }

    for asset in assets:
        name = asset.get("name", "")
        info = parse_wheel_filename(name)
        if not info:
            continue

        platform = normalize_platform_for_comparison(info["platform"])
        if platform not in packages:
            continue

        # Normalize torch version (2.9 -> 2.9.1 etc)
        # The wheel has minor version only, but matrix uses full version
        key = (
            info["flash_version"],
            info["python_version"],
            info["torch_version"],  # This is like "2.9", not "2.9.1"
            info["cuda_version"],
        )
        packages[platform].add(key)

    return packages


def normalize_torch_version(version: str) -> str:
    """Convert full torch version to minor version for comparison.

    Example: 2.9.1 -> 2.9, 2.10.0 -> 2.10
    """
    parts = version.split(".")
    if len(parts) >= 2:
        return f"{parts[0]}.{parts[1]}"
    return version


def generate_expected_matrix(matrix: dict) -> list[tuple]:
    """Generate all expected combinations from a matrix definition."""
    combinations = []
    for flash in matrix.get("flash-attn-version", []):
        for python in matrix.get("python-version", []):
            for torch in matrix.get("torch-version", []):
                for cuda in matrix.get("cuda-version", []):
                    combinations.append((flash, python, torch, cuda))
    return combinations


def create_status_table(
    platform_name: str,
    flash_version: str,
    matrix: dict,
    existing: set[tuple],
    console: Console,
) -> tuple[Table, int, int, int]:
    """Create a rich table for a specific platform and flash-attn version.

    Returns:
        Tuple of (table, existing_count, missing_count, excluded_count)
    """
    python_versions = sorted(matrix.get("python-version", []), key=parse_version_tuple)
    torch_versions = sorted(matrix.get("torch-version", []), key=parse_version_tuple)
    cuda_versions = sorted(matrix.get("cuda-version", []), key=parse_version_tuple)

    # Create table
    table = Table(
        title=f"{platform_name} - Flash-Attention {flash_version}",
        show_header=True,
        header_style="bold cyan",
        border_style="dim",
    )

    # Add Python column
    table.add_column("Python", style="bold", justify="center")

    # Add Torch/CUDA columns - group by torch version
    for torch in torch_versions:
        torch_minor = normalize_torch_version(torch)
        for cuda in cuda_versions:
            table.add_column(
                f"T{torch_minor}\nCU{cuda}",
                justify="center",
                min_width=6,
            )

    existing_count = 0
    missing_count = 0
    excluded_count = 0

    # Add rows for each Python version
    for python in python_versions:
        row = [f"cp{python.replace('.', '')}"]

        for torch in torch_versions:
            torch_minor = normalize_torch_version(torch)
            for cuda in cuda_versions:
                # Check status
                key = (flash_version, python, torch_minor, cuda)
                is_excl = is_excluded(flash_version, python, torch, cuda)

                if is_excl:
                    cell = Text("-", style="dim")
                    excluded_count += 1
                elif key in existing:
                    cell = Text("✓", style="bold green")
                    existing_count += 1
                else:
                    cell = Text("✗", style="bold red")
                    missing_count += 1

                row.append(cell)

        table.add_row(*row)

    return table, existing_count, missing_count, excluded_count


def display_platform_tables(
    platform: str,
    matrix: dict,
    existing_packages: set[tuple],
    console: Console,
    flash_version_filter: str | None = None,
    show_missing_only: bool = False,
) -> dict:
    """Display tables for a platform and return summary statistics."""
    platform_display_names = {
        "linux": "🐧 Linux x86_64",
        "linux_arm64": "🐧 Linux ARM64",
        "windows": "🪟 Windows",
    }
    platform_name = platform_display_names.get(platform, platform)

    flash_versions = matrix.get("flash-attn-version", [])
    if flash_version_filter:
        flash_versions = [v for v in flash_versions if v == flash_version_filter]

    total_existing = 0
    total_missing = 0
    total_excluded = 0
    missing_packages = []

    for flash_version in flash_versions:
        table, existing, missing, excluded = create_status_table(
            platform_name,
            flash_version,
            matrix,
            existing_packages,
            console,
        )

        total_existing += existing
        total_missing += missing
        total_excluded += excluded

        # Collect missing packages for summary
        if missing > 0:
            for python in matrix.get("python-version", []):
                for torch in matrix.get("torch-version", []):
                    torch_minor = normalize_torch_version(torch)
                    for cuda in matrix.get("cuda-version", []):
                        key = (flash_version, python, torch_minor, cuda)
                        is_excl = is_excluded(flash_version, python, torch, cuda)
                        if not is_excl and key not in existing_packages:
                            missing_packages.append(
                                {
                                    "platform": platform,
                                    "flash_version": flash_version,
                                    "python_version": python,
                                    "torch_version": torch,
                                    "cuda_version": cuda,
                                }
                            )

        # Show table only if there are missing packages (when --show-missing-only)
        if not show_missing_only or missing > 0:
            console.print(table)
            console.print()

    return {
        "existing": total_existing,
        "missing": total_missing,
        "excluded": total_excluded,
        "missing_packages": missing_packages,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Check missing packages by comparing GitHub releases with expected matrix"
    )
    parser.add_argument(
        "--repo",
        type=str,
        default="mjun0812/flash-attention-prebuild-wheels",
        help="GitHub repository (default: mjun0812/flash-attention-prebuild-wheels)",
    )
    parser.add_argument(
        "--cache",
        action="store_true",
        help="Use assets.json as cache (load if exists, save after fetch)",
    )
    parser.add_argument(
        "--cache-file",
        type=str,
        default="assets.json",
        help="Cache file path (default: assets.json)",
    )
    parser.add_argument(
        "--platform",
        type=str,
        choices=["linux", "linux_arm64", "windows", "all"],
        default="all",
        help="Platform to display (default: all)",
    )
    parser.add_argument(
        "--flash-version",
        type=str,
        help="Filter by specific flash-attn version",
    )
    parser.add_argument(
        "--show-missing-only",
        action="store_true",
        help="Only show tables with missing packages",
    )
    parser.add_argument(
        "--list-missing",
        action="store_true",
        help="List all missing packages at the end",
    )
    args = parser.parse_args()

    console = Console()
    cache_path = Path(args.cache_file)

    # Load or fetch assets
    assets = load_or_fetch_assets(args.repo, cache_path, args.cache)

    # Build existing packages set
    existing_packages = build_existing_packages_set(assets)

    # Determine which platforms to process
    platforms = ["linux", "linux_arm64", "windows"]
    if args.platform != "all":
        platforms = [args.platform]

    # Display tables and collect statistics
    all_stats = {}
    all_missing = []

    console.print()
    console.rule("[bold blue]Flash-Attention Package Status", style="blue")
    console.print()

    for platform in platforms:
        matrix = get_comprehensive_matrix(platform)
        if not matrix.get("flash-attn-version"):
            continue

        stats = display_platform_tables(
            platform,
            matrix,
            existing_packages.get(platform, set()),
            console,
            flash_version_filter=args.flash_version,
            show_missing_only=args.show_missing_only,
        )
        all_stats[platform] = stats
        all_missing.extend(stats["missing_packages"])

    # Display summary
    console.rule("[bold blue]Summary", style="blue")
    console.print()

    summary_table = Table(show_header=True, header_style="bold")
    summary_table.add_column("Platform", style="bold")
    summary_table.add_column("Existing", justify="right", style="green")
    summary_table.add_column("Missing", justify="right", style="red")
    summary_table.add_column("Excluded", justify="right", style="dim")
    summary_table.add_column("Coverage", justify="right")

    total_existing = 0
    total_missing = 0
    total_excluded = 0

    for platform, stats in all_stats.items():
        existing = stats["existing"]
        missing = stats["missing"]
        excluded = stats["excluded"]
        total = existing + missing

        total_existing += existing
        total_missing += missing
        total_excluded += excluded

        coverage = f"{existing / total * 100:.1f}%" if total > 0 else "N/A"
        coverage_style = (
            "green" if missing == 0 else "yellow" if existing > missing else "red"
        )

        summary_table.add_row(
            platform,
            str(existing),
            str(missing),
            str(excluded),
            Text(coverage, style=coverage_style),
        )

    # Add total row
    grand_total = total_existing + total_missing
    grand_coverage = (
        f"{total_existing / grand_total * 100:.1f}%" if grand_total > 0 else "N/A"
    )
    summary_table.add_row(
        Text("TOTAL", style="bold"),
        Text(str(total_existing), style="bold green"),
        Text(str(total_missing), style="bold red"),
        Text(str(total_excluded), style="dim"),
        Text(grand_coverage, style="bold"),
    )

    console.print(summary_table)
    console.print()

    # List missing packages if requested
    if args.list_missing and all_missing:
        console.rule("[bold red]Missing Packages", style="red")
        console.print()

        missing_table = Table(show_header=True, header_style="bold red")
        missing_table.add_column("Platform")
        missing_table.add_column("Flash-Attn")
        missing_table.add_column("Python")
        missing_table.add_column("Torch")
        missing_table.add_column("CUDA")

        for pkg in sorted(
            all_missing,
            key=lambda x: (
                x["platform"],
                parse_version_tuple(x["flash_version"]),
                parse_version_tuple(x["python_version"]),
                parse_version_tuple(x["torch_version"]),
                parse_version_tuple(x["cuda_version"]),
            ),
        ):
            missing_table.add_row(
                pkg["platform"],
                pkg["flash_version"],
                pkg["python_version"],
                pkg["torch_version"],
                pkg["cuda_version"],
            )

        console.print(missing_table)
        console.print()


if __name__ == "__main__":
    main()

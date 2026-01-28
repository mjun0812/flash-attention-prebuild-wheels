#!/usr/bin/env python3
"""Update README.md with package coverage badges and table.

This script fetches wheel assets from GitHub releases, calculates coverage
per platform, and updates the README.md between COVERAGE markers.

Usage:
    python update_readme_coverage.py
    python update_readme_coverage.py --cache
"""

import argparse
import urllib.parse
from pathlib import Path

from check_missing_packages import (
    build_existing_packages_set,
    generate_expected_matrix,
    get_comprehensive_matrix,
    is_excluded,
    load_or_fetch_assets,
    normalize_torch_version,
)

REPO = "mjun0812/flash-attention-prebuild-wheels"
PLATFORMS = {
    "linux": "Linux x86_64",
    "linux_arm64": "Linux ARM64",
    "windows": "Windows",
}

COVERAGE_START = "<!-- COVERAGE_START -->"
COVERAGE_END = "<!-- COVERAGE_END -->"


def calc_platform_stats(
    platform: str, existing_packages: dict[str, set[tuple]]
) -> dict:
    """Calculate existing, missing, excluded counts for a platform."""
    matrix = get_comprehensive_matrix(platform)
    if not matrix.get("flash-attn-version"):
        return {"existing": 0, "missing": 0, "excluded": 0}

    existing_set = existing_packages.get(platform, set())
    combinations = generate_expected_matrix(matrix)

    existing = 0
    missing = 0
    excluded = 0

    for flash, python, torch, cuda in combinations:
        torch_minor = normalize_torch_version(torch)
        if is_excluded(flash, python, torch, cuda):
            excluded += 1
        elif (flash, python, torch_minor, cuda) in existing_set:
            existing += 1
        else:
            missing += 1

    return {"existing": existing, "missing": missing, "excluded": excluded}


def badge_color(coverage_pct: float) -> str:
    """Return badge color based on coverage percentage."""
    if coverage_pct >= 90:
        return "green"
    elif coverage_pct >= 70:
        return "yellow"
    return "red"


def make_badge_url(label: str, coverage_pct: float) -> str:
    """Generate shields.io badge URL."""
    encoded_label = urllib.parse.quote(label.replace(" ", "_"))
    value = f"{coverage_pct:.1f}%"
    encoded_value = urllib.parse.quote(value)
    color = badge_color(coverage_pct)
    return f"https://img.shields.io/badge/{encoded_label}-{encoded_value}-{color}?style=for-the-badge"


def generate_coverage_markdown(stats_by_platform: dict[str, dict]) -> str:
    """Generate the coverage markdown block."""
    lines = [COVERAGE_START, "### Coverage", ""]

    # Badges
    for platform_key, display_name in PLATFORMS.items():
        s = stats_by_platform.get(platform_key)
        if not s:
            continue
        total = s["existing"] + s["missing"]
        pct = s["existing"] / total * 100 if total > 0 else 0
        url = make_badge_url(display_name, pct)
        lines.append(f"![{display_name}]({url})")
    lines.append("")

    # Table
    lines.append("| Platform | Existing | Missing | Coverage |")
    lines.append("|----------|----------|---------|----------|")

    total_existing = 0
    total_missing = 0

    for platform_key, display_name in PLATFORMS.items():
        s = stats_by_platform.get(platform_key)
        if not s:
            continue
        total = s["existing"] + s["missing"]
        pct = f"{s['existing'] / total * 100:.1f}%" if total > 0 else "N/A"
        lines.append(
            f"| {display_name} | {s['existing']} | {s['missing']} | {pct} |"
        )
        total_existing += s["existing"]
        total_missing += s["missing"]

    grand_total = total_existing + total_missing
    grand_pct = (
        f"{total_existing / grand_total * 100:.1f}%" if grand_total > 0 else "N/A"
    )
    lines.append(
        f"| **Total** | **{total_existing}** | **{total_missing}** | **{grand_pct}** |"
    )
    lines.append(COVERAGE_END)

    return "\n".join(lines)


def update_readme(readme_path: Path, coverage_block: str) -> None:
    """Replace content between COVERAGE markers in README."""
    content = readme_path.read_text(encoding="utf-8")

    start_idx = content.find(COVERAGE_START)
    end_idx = content.find(COVERAGE_END)

    if start_idx == -1 or end_idx == -1:
        print(f"Markers not found in {readme_path}. Skipping update.")
        return

    end_idx += len(COVERAGE_END)
    new_content = content[:start_idx] + coverage_block + content[end_idx:]
    readme_path.write_text(new_content, encoding="utf-8")
    print(f"Updated {readme_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Update README.md with coverage info")
    parser.add_argument(
        "--repo", type=str, default=REPO, help="GitHub repository"
    )
    parser.add_argument(
        "--cache", action="store_true", help="Use assets.json as cache"
    )
    parser.add_argument(
        "--cache-file", type=str, default="assets.json", help="Cache file path"
    )
    parser.add_argument(
        "--readme", type=str, default="README.md", help="README file path"
    )
    args = parser.parse_args()

    cache_path = Path(args.cache_file)
    assets = load_or_fetch_assets(args.repo, cache_path, args.cache)
    existing_packages = build_existing_packages_set(assets)

    stats_by_platform = {}
    for platform_key in PLATFORMS:
        stats_by_platform[platform_key] = calc_platform_stats(
            platform_key, existing_packages
        )

    coverage_block = generate_coverage_markdown(stats_by_platform)
    update_readme(Path(args.readme), coverage_block)


if __name__ == "__main__":
    main()

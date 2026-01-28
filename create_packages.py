"""Create and update doc/packages.md from assets.json.

This script generates a comprehensive package documentation page (doc/packages.md) from
GitHub release assets. It combines information from both assets.json and any existing
packages.md file, creating organized tables grouped by OS and Flash-Attention version.

The script:
- Parses wheel filenames to extract version information
- Merges data from assets.json and existing packages.md
- Generates collapsible tables organized by OS and Flash-Attention version
- Creates a table of contents for easy navigation
- Handles multiple download links per package

Usage:
    python create_packages.py [--assets <assets.json>] [--output <packages.md>]

Arguments:
    --assets: Path to assets.json file (default: assets.json)
              Can be obtained via `gh release view --json assets`
    --output: Output file path (default: doc/packages.md)

Example:
    # Basic usage
    python create_packages.py --assets assets.json --output doc/packages.md

    # Using defaults
    python create_packages.py

    # Generate from GitHub release
    gh release view v0.7.0 --json assets > assets.json
    python create_packages.py
"""

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote

import pandas as pd

from common import (
    get_os_emoji,
    get_tag_from_url,
    load_assets_json,
    normalize_platform_name,
    normalize_semantic_version,
    parse_numeric_version,
    parse_wheel_filename,
)

ADD_NOTE = """> [!NOTE]
> Since v0.7.0, wheels are built with manylinux2_28 platform.
> These wheels for Linux x86_64 and ManyLinux are compatible with old glibc versions (<=2.17).

> [!NOTE]
> Since v0.5.0, wheels are built with a local version label indicating the CUDA and PyTorch versions.
> Example: `pip list` -> `flash_attn==2.8.3 -> flash_attn==2.8.3+cu130torch2.9`
"""


def extract_packages_from_packages_md(packages_md_path: Path) -> list[dict]:
    """Extract package information from existing doc/packages.md."""
    if not packages_md_path.exists():
        return []

    with packages_md_path.open("r", encoding="utf-8") as f:
        content = f.read()

    lines = content.splitlines()

    packages = []
    current_os = None
    current_fa_version = None
    in_table = False

    for line in lines:
        line_stripped = line.strip()

        # Detect OS heading (## Linux x86_64)
        if line_stripped.startswith("## ") and not line_stripped.startswith("### "):
            # Remove emoji from OS name (e.g., "🐧 Linux x86_64" -> "Linux x86_64")
            os_name = line_stripped[3:].strip()
            while os_name and ord(os_name[0]) > 127:
                os_name = os_name[1:].strip()
            current_os = os_name
            current_fa_version = None
            in_table = False
            continue

        # Detect Flash-Attention version heading (### Flash-Attention 2.8.3)
        if line_stripped.startswith("### Flash-Attention "):
            current_fa_version = line_stripped.replace(
                "### Flash-Attention ", ""
            ).strip()
            in_table = False
            continue

        # Detect table start
        if "| Python | PyTorch | CUDA | package |" in line_stripped:
            in_table = True
            continue

        # Skip table separator line
        if in_table and "| ------ |" in line_stripped:
            continue

        # Process table rows
        if (
            in_table
            and line_stripped.startswith("|")
            and current_os
            and current_fa_version
        ):
            # Parse table row: | Python | PyTorch | CUDA | package |
            cells = [
                c.strip() for c in line_stripped.split("|")[1:-1]
            ]  # Remove empty first/last cells
            cells = [c for c in cells if c]  # Remove empty cells
            if len(cells) >= 4:
                python_version = cells[0]
                torch_version = cells[1]
                cuda_version = cells[2]
                package_cell = cells[3]

                # Extract all URLs from package cell
                # Pattern: [Release1](url1), [Download1](url1), [Release](url), [Download](url), ...
                # Support both Release and Download patterns for backward compatibility
                # Also support version suffix: [Download1(v1.0.0)](url)
                package_urls = re.findall(
                    r"\[(?:Release|Download)\d*(?:\([^)]*\))?\]\(([^)]+)\)",
                    package_cell,
                )

                if package_urls:
                    # Create a package entry for each URL
                    for package_url in package_urls:
                        # Decode URL to make it more readable
                        decoded_url = unquote(package_url)
                        packages.append(
                            {
                                "Flash-Attention": current_fa_version,
                                "Python": python_version,
                                "PyTorch": torch_version,
                                "CUDA": cuda_version,
                                "OS": current_os,
                                "package": decoded_url,
                            }
                        )
                elif package_cell != "-":
                    # Handle other formats
                    packages.append(
                        {
                            "Flash-Attention": current_fa_version,
                            "Python": python_version,
                            "PyTorch": torch_version,
                            "CUDA": cuda_version,
                            "OS": current_os,
                            "package": None,
                        }
                    )

        # Detect end of table (empty line or closing </details>)
        if in_table and (not line_stripped or line_stripped == "</details>"):
            in_table = False

    return packages


def extract_packages_from_assets_json(assets_path: Path) -> list[dict]:
    """Extract package information from assets.json file."""
    assets = load_assets_json(assets_path)
    packages = []

    for asset in assets:
        name = asset.get("name", "")
        url = asset.get("url", "")

        # Only process .whl files
        if not name.endswith(".whl"):
            continue

        # Parse wheel filename
        info = parse_wheel_filename(name)
        if not info:
            continue

        # Normalize platform name
        os_name = normalize_platform_name(info["platform"])

        # Decode URL to make it more readable
        decoded_url = unquote(url)

        packages.append(
            {
                "Flash-Attention": info["flash_version"],
                "Python": info["python_version"],
                "PyTorch": info["torch_version"],
                "CUDA": info["cuda_version"],
                "OS": os_name,
                "package": decoded_url,
            }
        )

    return packages


def sort_packages(
    df: pd.DataFrame,
    flash_ascending: bool = False,
    python_ascending: bool = False,
    pytorch_ascending: bool = False,
    cuda_ascending: bool = False,
    os_ascending: bool = True,
    package_ascending: bool = False,
) -> pd.DataFrame:
    """
    Sort packages by columns from left to right.

    Args:
        df: DataFrame to sort
        flash_ascending: Sort Flash-Attention in ascending order (default: False, newer first)
        python_ascending: Sort Python in ascending order (default: False, newer first)
        pytorch_ascending: Sort PyTorch in ascending order (default: False, newer first)
        cuda_ascending: Sort CUDA in ascending order (default: False, newer first)
        os_ascending: Sort OS in ascending order (default: True, alphabetical)
        package_ascending: Sort package in ascending order (default: False, newer first)

    Returns:
        Sorted DataFrame
    """
    df = df.copy()

    # Add sorting keys for version columns
    df["fa_sort"] = df["Flash-Attention"].apply(parse_numeric_version)
    df["py_sort"] = df["Python"].apply(parse_numeric_version)
    df["pt_sort"] = df["PyTorch"].apply(parse_numeric_version)
    df["cu_sort"] = df["CUDA"].apply(parse_numeric_version)
    df["os_sort"] = df["OS"].str.lower()

    # Package sort: extract version from download URL
    def package_sort_key(url):
        # Handle list of URLs (take the first one for sorting)
        if isinstance(url, list):
            if not url or all(pd.isna(u) or not u for u in url):
                return tuple()
            # Find first non-empty URL
            for u in url:
                if pd.notna(u) and u:
                    url = u
                    break
            else:
                return tuple()

        if pd.isna(url) or not url:
            return tuple()  # No URL

        # Extract tag from download URL: /releases/download/{tag}/
        tag_match = re.search(r"/releases/download/([^/]+)/", str(url))
        if not tag_match:
            return tuple()

        tag = tag_match.group(1)
        return parse_numeric_version(tag)

    df["pkg_sort"] = df["package"].apply(package_sort_key)

    # Sort by columns from left to right
    df_sorted = df.sort_values(
        by=["fa_sort", "os_sort", "py_sort", "pt_sort", "cu_sort", "pkg_sort"],
        ascending=[
            flash_ascending,
            os_ascending,
            python_ascending,
            pytorch_ascending,
            cuda_ascending,
            package_ascending,
        ],
    )

    # Drop sorting columns
    return df_sorted.drop(
        columns=["fa_sort", "os_sort", "py_sort", "pt_sort", "cu_sort", "pkg_sort"]
    )


def merge_duplicate_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Merge rows with duplicate Flash-Attention, Python, PyTorch, CUDA, OS values."""
    # Group by all columns except 'package'
    group_cols = ["Flash-Attention", "Python", "PyTorch", "CUDA", "OS"]

    def combine_packages(group):
        # Get unique non-null packages (handle both list and scalar values)
        all_packages = []
        for pkg in group["package"]:
            if pd.notna(pkg):
                if isinstance(pkg, list):
                    all_packages.extend(pkg)
                else:
                    all_packages.append(pkg)

        # Remove duplicates while preserving order
        seen = set()
        unique_packages = []
        for pkg in all_packages:
            if pkg and pkg not in seen:
                seen.add(pkg)
                unique_packages.append(pkg)

        # Return as a Series with object dtype to avoid pandas 3.0 StringDtype issues
        packages = unique_packages if unique_packages else [None]
        return pd.Series({"package": packages}, dtype=object)

    # Group and combine
    merged_df = df.groupby(group_cols, as_index=False).apply(
        combine_packages, include_groups=False
    )

    # Reset index to clean up
    merged_df = merged_df.reset_index(drop=True)

    return merged_df


def generate_markdown_table_by_os(df: pd.DataFrame) -> str:
    """Generate markdown tables grouped by OS and Flash-Attention version."""
    if df.empty:
        return ""

    all_sections = []

    # Generate Table of Contents
    # Custom order: Linux x86_64, Linux arm64, Windows
    os_order = ["Linux x86_64", "Linux arm64", "Windows"]
    all_os_names = df["OS"].unique()
    os_names = [os for os in os_order if os in all_os_names]
    # Add any OS not in the predefined order (for flexibility)
    for os in sorted(all_os_names):
        if os not in os_names:
            os_names.append(os)
    toc_lines = ["## Table of Contents", ""]
    for os_name in os_names:
        # Create anchor link (lowercase, replace spaces with hyphens)
        os_anchor = os_name.lower().replace(" ", "-")
        toc_lines.append(f"- [{os_name}](#{os_anchor})")

        # Add Flash-Attention versions for this OS (sorted)
        os_df = df[df["OS"] == os_name].copy()
        os_df = sort_packages(os_df, flash_ascending=False)
        for fa_version in os_df["Flash-Attention"].unique():
            # Create anchor for Flash-Attention version
            fa_anchor = f"flash-attention-{fa_version.replace('.', '')}".lower()
            toc_lines.append(f"  - [Flash-Attention {fa_version}](#{fa_anchor})")
    toc_lines.append("")
    all_sections.extend(toc_lines)

    # Group by OS and sort each group
    for os_name in os_names:
        os_df = df[df["OS"] == os_name].copy()

        # Sort within OS group: Flash-Attention > Python > PyTorch > CUDA
        os_df = sort_packages(
            os_df,
            flash_ascending=False,
            python_ascending=True,
            pytorch_ascending=True,
            cuda_ascending=True,
        )

        # Create OS section header with emoji
        os_emoji = get_os_emoji(os_name)
        os_lines = [f"## {os_emoji}{os_name}", ""]

        # Group by Flash-Attention version within each OS
        fa_versions = []
        for fa_version in os_df["Flash-Attention"].unique():
            fa_df = os_df[os_df["Flash-Attention"] == fa_version].copy()

            # Sort by Python > PyTorch > CUDA within each Flash-Attention version
            fa_df = sort_packages(
                fa_df,
                python_ascending=True,
                pytorch_ascending=True,
                cuda_ascending=True,
            )

            # Create collapsible table for this Flash-Attention version
            table_lines = [
                "| Python | PyTorch | CUDA | package |",
                "| ------ | ------- | ---- | ------- |",
            ]

            for _, row in fa_df.iterrows():
                packages = row["package"]

                # Handle case where packages is a list
                if isinstance(packages, list):
                    if packages and any(pd.notna(pkg) and pkg for pkg in packages):
                        # Create numbered download links
                        package_links = []
                        for i, pkg in enumerate(packages, 1):
                            if pd.notna(pkg) and pkg:
                                tag = get_tag_from_url(pkg)
                                tag_str = f"({tag})" if tag else ""
                                package_links.append(f"[Download{i}{tag_str}]({pkg})")
                        package_cell = ", ".join(package_links)
                    else:
                        package_cell = "-"
                else:
                    # Handle single package (backward compatibility)
                    tag = get_tag_from_url(packages)
                    tag_str = f"({tag})" if tag else ""
                    package_cell = (
                        f"[Download{tag_str}]({packages})"
                        if pd.notna(packages) and packages
                        else "-"
                    )

                line = f"| {row['Python']} | {row['PyTorch']} | {row['CUDA']} | {package_cell} |"
                table_lines.append(line)

            # Create collapsible section for this Flash-Attention version
            fa_section = [
                f"### Flash-Attention {fa_version}",
                "",
                "<details>",
                f"<summary>Packages for Flash-Attention {fa_version}</summary>",
                "",
                "\n".join(table_lines),
                "",
                "</details>",
                "",
            ]

            fa_versions.extend(fa_section)

        os_lines.extend(fa_versions)
        all_sections.extend(os_lines)

    return "\n".join(all_sections)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create and update doc/packages.md from assets.json"
    )
    parser.add_argument(
        "--assets",
        type=str,
        default="assets.json",
        help="Path to assets.json file (default: assets.json)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="doc/packages.md",
        help="Output file path (default: doc/packages.md)",
    )
    args = parser.parse_args()

    assets_path = Path(args.assets)
    output_path = Path(args.output)

    # Extract packages from assets.json if it exists
    assets_packages = []
    if assets_path.exists():
        assets_packages = extract_packages_from_assets_json(assets_path)

    # Extract packages from existing doc/packages.md
    packages_md_packages = extract_packages_from_packages_md(output_path)

    # Combine both lists
    all_packages = assets_packages + packages_md_packages

    if not all_packages:
        print(f"No packages found in {assets_path} or {output_path}", file=sys.stderr)
        return

    # Convert to DataFrame and process
    df = pd.DataFrame(all_packages)
    # Normalize CUDA versions (remove patch version)
    df["CUDA"] = df["CUDA"].apply(normalize_semantic_version)
    # Normalize PyTorch versions (remove patch version)
    df["PyTorch"] = df["PyTorch"].apply(normalize_semantic_version)
    # Normalize Python versions (remove patch version)
    df["Python"] = df["Python"].apply(normalize_semantic_version)
    df_sorted = sort_packages(df)
    df_merged = merge_duplicate_rows(df_sorted)
    markdown = generate_markdown_table_by_os(df_merged)

    # Create parent directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Generate markdown with "# Packages" header for standalone file
    standalone_markdown = f"# Packages\n\n{ADD_NOTE}\n{markdown}"

    with output_path.open("w", encoding="utf-8") as f:
        f.write(standalone_markdown)
    print(f"Written packages to {output_path}")


if __name__ == "__main__":
    main()

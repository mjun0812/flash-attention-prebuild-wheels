"""
python insert_packages_to_readme.py --assets assets.json --update
"""

import argparse
import json
import re
import sys
from pathlib import Path

import pandas as pd

from common import normalize_platform_name, parse_wheel_filename


def parse_numeric_version(text: str) -> tuple:
    """Extract numeric version tuple for sorting."""
    nums = re.findall(r"\d+", text)
    return tuple(int(n) for n in nums)


def normalize_semantic_version(version: str) -> str:
    """Normalize semantic version by removing patch version.

    Examples:
        2.9.1 -> 2.9
        2.8.1 -> 2.8
        2.6.3 -> 2.6
        2.9 -> 2.9 (no change if no patch version)
    """
    if pd.isna(version) or not version:
        return version

    # Split by '.' and take only major.minor
    parts = str(version).split(".")
    if len(parts) >= 2:
        return ".".join(parts[:2])
    return version


def extract_packages_from_readme(readme_path: Path) -> list[dict]:
    """Extract package information from existing Packages section in README.md."""
    with readme_path.open("r", encoding="utf-8") as f:
        content = f.read()

    # Find Packages section
    packages_start = content.find("## Packages")
    if packages_start == -1:
        return []

    # Find the end of Packages section
    packages_end = content.find("## History", packages_start)
    if packages_end == -1:
        remaining_content = content[packages_start + len("## Packages") :]
        next_section = remaining_content.find("\n## ")
        if next_section != -1:
            packages_end = packages_start + len("## Packages") + next_section
        else:
            packages_end = len(content)

    packages_section = content[packages_start:packages_end]
    lines = packages_section.splitlines()

    packages = []
    current_os = None
    current_fa_version = None
    in_table = False

    for i, line in enumerate(lines):
        line_stripped = line.strip()

        # Detect OS heading (### Linux x86_64)
        if line_stripped.startswith("### ") and not line_stripped.startswith("#### "):
            current_os = line_stripped[4:].strip()
            current_fa_version = None
            in_table = False
            continue

        # Detect Flash-Attention version heading (#### Flash-Attention 2.8.3)
        if line_stripped.startswith("#### Flash-Attention "):
            # Extract version after "#### Flash-Attention "
            current_fa_version = line_stripped.replace(
                "#### Flash-Attention ", ""
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
                package_urls = re.findall(
                    r"\[(?:Release|Download)\d*\]\(([^)]+)\)", package_cell
                )

                if package_urls:
                    # Create a package entry for each URL
                    for package_url in package_urls:
                        packages.append(
                            {
                                "Flash-Attention": current_fa_version,
                                "Python": python_version,
                                "PyTorch": torch_version,
                                "CUDA": cuda_version,
                                "OS": current_os,
                                "package": package_url,
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
    with assets_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if "assets" not in data:
        return []

    packages = []

    for asset in data["assets"]:
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

        # Format versions for display
        flash_version = info["flash_version"]
        python_version = info["python_version"]
        torch_version = info["torch_version"]  # Already in format like "2.9"
        cuda_version = info["cuda_version"]

        packages.append(
            {
                "Flash-Attention": flash_version,
                "Python": python_version,
                "PyTorch": torch_version,
                "CUDA": cuda_version,
                "OS": os_name,
                "package": url,  # Use download URL directly
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

        # Take the first row as base
        result = group.iloc[0].copy()

        # Combine packages into a list
        result["package"] = unique_packages if unique_packages else [None]

        return result

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

    # Group by OS and sort each group
    for os_name in sorted(df["OS"].unique()):
        os_df = df[df["OS"] == os_name].copy()

        # Sort within OS group: Flash-Attention > Python > PyTorch > CUDA
        os_df = sort_packages(
            os_df,
            flash_ascending=False,
            python_ascending=True,
            pytorch_ascending=True,
            cuda_ascending=True,
        )

        # Create OS section header
        os_lines = [f"### {os_name}", ""]

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
                                package_links.append(f"[Download{i}]({pkg})")
                        package_cell = ", ".join(package_links)
                    else:
                        package_cell = "-"
                else:
                    # Handle single package (backward compatibility)
                    package_cell = (
                        f"[Download]({packages})"
                        if pd.notna(packages) and packages
                        else "-"
                    )

                line = f"| {row['Python']} | {row['PyTorch']} | {row['CUDA']} | {package_cell} |"
                table_lines.append(line)

            # Create collapsible section for this Flash-Attention version
            fa_section = [
                f"#### Flash-Attention {fa_version}",
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


def update_readme_packages_section(readme_path: Path, packages_markdown: str) -> None:
    """Update the Packages section in README.md with new content."""
    with readme_path.open("r", encoding="utf-8") as f:
        content = f.read()

    # Find the Packages section
    packages_start = content.find("## Packages")
    if packages_start == -1:
        raise ValueError("Packages section not found in README.md")

    # Find the end of Packages section (next ## section or History section)
    packages_end = content.find("## History", packages_start)
    if packages_end == -1:
        # If no History section found, look for any other ## section
        remaining_content = content[packages_start + len("## Packages") :]
        next_section = remaining_content.find("\n## ")
        if next_section != -1:
            packages_end = packages_start + len("## Packages") + next_section
        else:
            packages_end = len(content)

    # Replace the Packages section
    new_content = (
        content[:packages_start]
        + "## Packages\n\n"
        + packages_markdown
        + "\n\n"
        + content[packages_end:]
    )

    # Write back to file
    with readme_path.open("w", encoding="utf-8") as f:
        f.write(new_content)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a one-row-per-package Markdown table from assets.json file"
    )
    parser.add_argument(
        "--assets",
        type=str,
        default="assets.json",
        help="Path to assets.json file (default: assets.json)",
    )
    parser.add_argument(
        "--update",
        action="store_true",
        help="Update the Packages section in README.md instead of printing to stdout",
    )
    args = parser.parse_args()

    assets_path = Path(args.assets)
    if not assets_path.exists():
        print(f"Error: {assets_path} not found", file=sys.stderr)
        sys.exit(1)

    readme_path = Path("README.md")

    # Extract packages from assets.json
    assets_packages = extract_packages_from_assets_json(assets_path)

    # Extract packages from existing README.md
    readme_packages = extract_packages_from_readme(readme_path)

    # Combine both lists
    all_packages = assets_packages + readme_packages

    if not all_packages:
        print(f"No packages found in {assets_path} or README.md", file=sys.stderr)
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

    if args.update:
        # Update the README.md file
        update_readme_packages_section(readme_path, markdown)
        print(f"Updated Packages section in {readme_path}")
    else:
        # Print to stdout (original behavior)
        print(markdown)


if __name__ == "__main__":
    main()

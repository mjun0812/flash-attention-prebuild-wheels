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


def extract_release_url_from_download_url(download_url: str) -> str | None:
    """Extract release tag from download URL and construct release page URL."""
    # Pattern: /releases/download/{tag}/
    match = re.search(r"/releases/download/([^/]+)/", download_url)
    if not match:
        return None

    tag = match.group(1)
    # Construct release page URL
    # Extract repo path from download URL
    repo_match = re.search(r"(https://github\.com/[^/]+/[^/]+)", download_url)
    if not repo_match:
        return None

    repo_path = repo_match.group(1)
    return f"{repo_path}/releases/tag/{tag}"


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

                # Extract all release URLs from package cell
                # Pattern: [Release1](url1), [Release2](url2), ...
                release_urls = re.findall(r"\[Release\d+\]\(([^)]+)\)", package_cell)

                if release_urls:
                    # Create a package entry for each release URL
                    for release_url in release_urls:
                        packages.append(
                            {
                                "Flash-Attention": current_fa_version,
                                "Python": python_version,
                                "PyTorch": torch_version,
                                "CUDA": cuda_version,
                                "OS": current_os,
                                "package": release_url,
                            }
                        )
                elif package_cell != "-":
                    # Handle single release or other formats
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

        # Extract release URL from download URL
        release_url = extract_release_url_from_download_url(url)

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
                "package": release_url,
            }
        )

    return packages


def sort_packages(df: pd.DataFrame) -> pd.DataFrame:
    """Sort packages with custom priority."""

    # Add sorting keys
    # Flash-Attention: descending order (newer versions first)
    df["fa_sort"] = df["Flash-Attention"].apply(
        lambda x: tuple(-v for v in parse_numeric_version(x))
    )
    df["os_sort"] = df["OS"].str.lower()
    # Python, PyTorch, CUDA: descending order (newer versions first)
    df["py_sort"] = df["Python"].apply(
        lambda x: tuple(-v for v in parse_numeric_version(x))
    )
    df["pt_sort"] = df["PyTorch"].apply(
        lambda x: tuple(-v for v in parse_numeric_version(x))
    )
    df["cu_sort"] = df["CUDA"].apply(
        lambda x: tuple(-v for v in parse_numeric_version(x))
    )

    # Package sort: extract version from URL, newer first
    def package_sort_key(url):
        if pd.isna(url) or not url:
            return (1, tuple())  # No URL comes last

        tag_match = re.search(r"/tag/([^/]+)$", str(url))
        if not tag_match:
            return (1, tuple())

        tag = tag_match.group(1)
        version_tuple = parse_numeric_version(tag)
        return (0, tuple(-v for v in version_tuple))  # Negate for descending

    df["pkg_sort"] = df["package"].apply(package_sort_key)

    # Sort by priority: Flash-Attention > OS > Python > PyTorch > CUDA > package
    df_sorted = df.sort_values(
        ["fa_sort", "os_sort", "py_sort", "pt_sort", "cu_sort", "pkg_sort"]
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

        # Re-sort within each OS group to ensure Flash-Attention is in descending order
        os_df["fa_sort"] = os_df["Flash-Attention"].apply(
            lambda x: tuple(-v for v in parse_numeric_version(x))
        )
        os_df["py_sort"] = os_df["Python"].apply(
            lambda x: tuple(-v for v in parse_numeric_version(x))
        )
        os_df["pt_sort"] = os_df["PyTorch"].apply(
            lambda x: tuple(-v for v in parse_numeric_version(x))
        )
        os_df["cu_sort"] = os_df["CUDA"].apply(
            lambda x: tuple(-v for v in parse_numeric_version(x))
        )

        # Sort by Flash-Attention > Python > PyTorch > CUDA
        os_df = os_df.sort_values(["fa_sort", "py_sort", "pt_sort", "cu_sort"])
        os_df = os_df.drop(columns=["fa_sort", "py_sort", "pt_sort", "cu_sort"])

        # Create OS section header
        os_lines = [f"### {os_name}", ""]

        # Group by Flash-Attention version within each OS
        fa_versions = []
        for fa_version in os_df["Flash-Attention"].unique():
            fa_df = os_df[os_df["Flash-Attention"] == fa_version].copy()

            # Re-sort by Python > PyTorch > CUDA within each Flash-Attention version
            fa_df["py_sort"] = fa_df["Python"].apply(
                lambda x: tuple(-v for v in parse_numeric_version(x))
            )
            fa_df["pt_sort"] = fa_df["PyTorch"].apply(
                lambda x: tuple(-v for v in parse_numeric_version(x))
            )
            fa_df["cu_sort"] = fa_df["CUDA"].apply(
                lambda x: tuple(-v for v in parse_numeric_version(x))
            )
            fa_df = fa_df.sort_values(["py_sort", "pt_sort", "cu_sort"])
            fa_df = fa_df.drop(columns=["py_sort", "pt_sort", "cu_sort"])

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
                        # Create numbered release links
                        package_links = []
                        for i, pkg in enumerate(packages, 1):
                            if pd.notna(pkg) and pkg:
                                package_links.append(f"[Release{i}]({pkg})")
                        package_cell = ", ".join(package_links)
                    else:
                        package_cell = "-"
                else:
                    # Handle single package (backward compatibility)
                    package_cell = (
                        f"[Release]({packages})"
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


def generate_markdown_table(df: pd.DataFrame) -> str:
    """Generate markdown table from DataFrame (legacy function for backward compatibility)."""
    lines = [
        "| Flash-Attention | Python | PyTorch | CUDA | OS | package |",
        "| --------------- | ------ | ------- | ------ | ---- | ------- |",
    ]

    for _, row in df.iterrows():
        packages = row["package"]

        # Handle case where packages is a list
        if isinstance(packages, list):
            if packages and any(pd.notna(pkg) and pkg for pkg in packages):
                # Create numbered release links
                package_links = []
                for i, pkg in enumerate(packages, 1):
                    if pd.notna(pkg) and pkg:
                        package_links.append(f"[Release{i}]({pkg})")
                package_cell = ", ".join(package_links)
            else:
                package_cell = "-"
        else:
            # Handle single package (backward compatibility)
            package_cell = (
                f"[Release]({packages})" if pd.notna(packages) and packages else "-"
            )

        line = f"| {row['Flash-Attention']} | {row['Python']} | {row['PyTorch']} | {row['CUDA']} | {row['OS']} | {package_cell} |"
        lines.append(line)

    return "\n".join(lines)


def update_readme_packages_section(readme_path: Path, packages_markdown: str) -> None:
    """Update the Packages section in README.md with new content."""
    try:
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

    except Exception as e:
        raise RuntimeError(f"Failed to update README.md: {e}")


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

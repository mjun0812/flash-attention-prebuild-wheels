"""Generate release notes from assets.json.

This script generates markdown release notes from a GitHub release assets JSON file.
It extracts version information from wheel filenames and creates a formatted table
showing supported Flash-Attention, Python, PyTorch, and CUDA versions for each platform.

Usage:
    python create_release_note.py <assets.json>

Arguments:
    assets.json: Path to JSON file containing GitHub release assets
                 (obtained via `gh release view --json assets`)

Output:
    Markdown-formatted release notes to stdout

Example:
    gh release view v0.7.0 --json assets > assets.json
    python create_release_note.py assets.json > release_notes.md
"""

import sys
from pathlib import Path

from scripts.common import collect_versions_from_assets, format_versions, load_assets_json


def generate_release_notes(assets: list[dict]) -> str:
    """Generate release notes from assets.

    Args:
        assets: List of asset dictionaries

    Returns:
        Formatted release notes as markdown string
    """
    versions_by_platform = collect_versions_from_assets(assets)

    if not versions_by_platform:
        return ""

    notes = []
    for platform_name in sorted(versions_by_platform.keys()):
        data = versions_by_platform[platform_name]

        notes.append(f"## {platform_name}")
        notes.append("")
        notes.append("| Flash-Attention | Python | PyTorch | CUDA |")
        notes.append("| --- | --- | --- | --- |")

        flash_versions = format_versions(data["flash_versions"])
        python_versions = format_versions(data["python_versions"])
        torch_versions = format_versions(data["torch_versions"])
        cuda_versions = format_versions(data["cuda_versions"])

        notes.append(
            f"| {flash_versions} | {python_versions} | {torch_versions} | {cuda_versions} |"
        )
        notes.append("")

    return "\n".join(notes)


def main():
    try:
        if len(sys.argv) != 2:
            print("Usage: python create_release_note.py <assets.json>", file=sys.stderr)
            sys.exit(1)

        assets_json_path = Path(sys.argv[1])
        if not assets_json_path.exists():
            print(f"File not found: {assets_json_path}", file=sys.stderr)
            sys.exit(1)

        assets = load_assets_json(assets_json_path)
        if not assets:
            print("No assets found in JSON file", file=sys.stderr)
            sys.exit(1)

        text = generate_release_notes(assets)
        if text:
            print(text)
        else:
            print("No wheel assets found", file=sys.stderr)
            sys.exit(1)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

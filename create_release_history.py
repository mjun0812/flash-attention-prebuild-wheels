"""Update the History section in README.md from assets.

This script updates the History section in README.md by inserting or updating a release entry.
It extracts version information from a GitHub release assets JSON file and formats it as a
markdown table, then inserts it into the README.md History section.

Usage:
    python create_release_history.py --assets <assets.json> --tag <tag> --repo <owner/name> --output <README.md>

Arguments:
    --assets: Path to JSON file containing GitHub release assets
              (obtained via `gh release view --json assets`)
    --tag:    Release tag name (e.g., v0.7.0)
    --repo:   Repository in owner/name format (e.g., mjun0812/flash-attention-prebuild-wheels)
    --output: Path to README.md file to update

Example:
    gh release view v0.7.0 --json assets > /tmp/assets.json
    python create_release_history.py \\
        --assets /tmp/assets.json \\
        --tag v0.7.0 \\
        --repo mjun0812/flash-attention-prebuild-wheels \\
        --output README.md
"""

import argparse
import re
from pathlib import Path

from common import (
    collect_versions_from_assets,
    format_versions,
    load_assets_json,
)


def render_body_from_versions(
    versions_by_platform: dict[str, dict[str, set[str]]]
) -> str:
    """Render markdown body from aggregated version data.

    Args:
        versions_by_platform: Dictionary mapping platform to version sets

    Returns:
        Formatted markdown string
    """
    if not versions_by_platform:
        raise ValueError("No wheel assets found")

    body_lines: list[str] = []

    for platform in sorted(versions_by_platform.keys()):
        data = versions_by_platform[platform]
        body_lines.extend(
            [
                f"#### {platform}",
                "",
                "| Flash-Attention | Python | PyTorch | CUDA |",
                "| --- | --- | --- | --- |",
                "| "
                + " | ".join(
                    [
                        format_versions(data["flash_versions"]),
                        format_versions(data["python_versions"]),
                        format_versions(data["torch_versions"]),
                        format_versions(data["cuda_versions"]),
                    ]
                )
                + " |",
                "",
            ]
        )

    return "\n".join(body_lines).strip()


def build_history_section(tag: str, repo: str, body: str) -> str:
    """Build history section for README.md.

    Args:
        tag: Release tag name
        repo: Repository in owner/name format
        body: Markdown body content

    Returns:
        Formatted history section
    """
    release_url = f"https://github.com/{repo}/releases/tag/{tag}"
    lines = [f"### {tag}", "", f"[Release]({release_url})", "", body.strip()]
    return "\n".join(lines).rstrip() + "\n\n"


def remove_existing_section(content: str, tag: str) -> str:
    """Remove existing section for the given tag from README content.

    Args:
        content: README.md content
        tag: Release tag name

    Returns:
        Content with the section removed
    """
    pattern = re.compile(
        rf"^### {re.escape(tag)}\n.*?(?=^### |\Z)", re.MULTILINE | re.DOTALL
    )
    return re.sub(pattern, "", content)


def insert_history_section(content: str, section: str) -> str:
    """Insert history section into README content.

    Args:
        content: README.md content
        section: History section to insert

    Returns:
        Updated README.md content
    """
    marker = "## History\n"
    idx = content.find(marker)
    if idx == -1:
        raise ValueError("History section is missing in README.md")

    insert_pos = idx + len(marker)
    return content[:insert_pos] + "\n" + section + content[insert_pos:]


def main() -> None:
    parser = argparse.ArgumentParser(description="Update README.md History section")
    parser.add_argument(
        "--assets", type=Path, required=True, help="JSON file from gh release view"
    )
    parser.add_argument("--tag", required=True, help="Release tag name")
    parser.add_argument("--repo", required=True, help="Repository in owner/name format")
    parser.add_argument("--output", type=Path, required=True, help="Output file path")
    args = parser.parse_args()

    # Load and process assets
    assets = load_assets_json(args.assets)
    versions_by_platform = collect_versions_from_assets(assets)
    history_body = render_body_from_versions(versions_by_platform)

    # Build and insert history section
    section = build_history_section(args.tag, args.repo, history_body)

    content = args.output.read_text(encoding="utf-8")
    stripped = remove_existing_section(content, args.tag)
    updated = insert_history_section(stripped, section)

    if updated == content:
        print("No changes in README.md")
        return

    args.output.write_text(updated, encoding="utf-8")
    print(f"Inserted history for {args.tag} into README.md")


if __name__ == "__main__":
    main()

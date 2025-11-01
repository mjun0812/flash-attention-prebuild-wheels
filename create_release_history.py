"""Update the History section in README.md from assets."""

import argparse
import json
import re
from pathlib import Path
from typing import Dict, Iterable

from common import normalize_platform_name, parse_wheel_filename


def collect_versions(
    assets: Iterable[Dict[str, str]],
) -> Dict[str, Dict[str, set[str]]]:
    aggregated: Dict[str, Dict[str, set[str]]] = {}
    for asset in assets:
        info = parse_wheel_filename(asset.get("name", ""))
        if not info:
            continue

        platform = normalize_platform_name(info["platform"])
        platform_data = aggregated.setdefault(
            platform,
            {
                "flash_versions": set(),
                "python_versions": set(),
                "torch_versions": set(),
                "cuda_versions": set(),
            },
        )

        platform_data["flash_versions"].add(info["flash_version"])
        platform_data["python_versions"].add(info["python_version"])
        platform_data["torch_versions"].add(info["torch_version"])
        platform_data["cuda_versions"].add(info["cuda_version"])

    return aggregated


def format_versions(values: set[str]) -> str:
    if not values:
        return "-"
    return ", ".join(sorted(values))


def render_body_from_aggregated(aggregated: Dict[str, Dict[str, set[str]]]) -> str:
    if not aggregated:
        raise ValueError("No wheel assets found")

    body_lines: list[str] = []

    for platform in sorted(aggregated.keys()):
        data = aggregated[platform]
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
    release_url = f"https://github.com/{repo}/releases/tag/{tag}"
    lines = [f"### {tag}", "", f"[Release]({release_url})", "", body.strip()]
    return "\n".join(lines).rstrip() + "\n\n"


def remove_existing_section(content: str, tag: str) -> str:
    pattern = re.compile(
        rf"^### {re.escape(tag)}\n.*?(?=^### |\Z)", re.MULTILINE | re.DOTALL
    )
    return re.sub(pattern, "", content)


def insert_history_section(content: str, section: str) -> str:
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

    data = json.loads(args.assets.read_text(encoding="utf-8"))
    assets = data.get("assets", [])
    aggregated = collect_versions(assets)
    history_body = render_body_from_aggregated(aggregated)

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

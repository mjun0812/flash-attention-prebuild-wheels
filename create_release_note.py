import json
import sys
from pathlib import Path

from common import normalize_platform_name, parse_wheel_filename


def generate_release_notes_from_assets(assets_info: dict):
    assets_names = [
        asset["name"] for asset in assets_info if asset["name"].endswith(".whl")
    ]
    if len(assets_names) == 0:
        sys.exit(1)

    assets_dict = {}

    for asset_name in assets_names:
        asset_info = parse_wheel_filename(asset_name)
        if asset_info is None:
            continue

        if asset_info["platform"] not in assets_dict:
            assets_dict[asset_info["platform"]] = {
                "flash_versions": set(),
                "python_versions": set(),
                "torch_versions": set(),
                "cuda_versions": set(),
            }
        assets_dict[asset_info["platform"]]["flash_versions"].add(
            asset_info["flash_version"]
        )
        assets_dict[asset_info["platform"]]["python_versions"].add(
            asset_info["python_version"]
        )
        assets_dict[asset_info["platform"]]["torch_versions"].add(
            asset_info["torch_version"]
        )
        assets_dict[asset_info["platform"]]["cuda_versions"].add(
            asset_info["cuda_version"]
        )

    notes = []

    for platform_name, data in sorted(assets_dict.items()):
        if any(len(data[key]) == 0 for key in data):
            continue

        platform_name = normalize_platform_name(platform_name)

        notes.append(f"## {platform_name}")
        notes.append("")
        notes.append("| Flash-Attention | Python | PyTorch | CUDA |")
        notes.append("| --- | --- | --- | --- |")

        flash_versions = ", ".join(sorted(data["flash_versions"]))
        python_versions = ", ".join(sorted(data["python_versions"]))
        torch_versions = ", ".join(sorted(data["torch_versions"]))
        cuda_versions = ", ".join(sorted(data["cuda_versions"]))

        notes.append(
            f"| {flash_versions} | {python_versions} | {torch_versions} | {cuda_versions} |"
        )
        notes.append("")

    return "\n".join(notes)


def main():
    try:
        if len(sys.argv) != 2:
            sys.exit(1)

        assets_json_path = Path(sys.argv[1])
        if not assets_json_path.exists():
            sys.exit(1)

        with open(assets_json_path, "r") as f:
            assets_info = json.load(f)["assets"]

        if len(assets_info) == 0:
            sys.exit(1)

        text = generate_release_notes_from_assets(assets_info)
        if text:
            print(text)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

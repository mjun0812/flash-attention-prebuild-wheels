"""Common utility functions for processing Flash-Attention wheel packages.

This module provides shared functionality for parsing wheel filenames, extracting version
information, and processing GitHub release assets. It is used by scripts that generate
documentation and release notes for Flash-Attention prebuilt wheels.

Functions:
    - load_assets_json: Load assets from GitHub release JSON file
    - parse_wheel_filename: Extract version info from wheel filename
    - normalize_platform_name: Standardize platform names for display
    - parse_numeric_version: Convert version strings to tuples for sorting
    - normalize_semantic_version: Remove patch version from semantic versions
    - get_tag_from_url: Extract release tag from GitHub download URL
    - get_os_emoji: Get emoji representation for OS names
    - collect_versions_from_assets: Aggregate version info by platform
    - format_versions: Format version sets as comma-separated strings
"""

import json
import re
from pathlib import Path
from typing import Iterable

import pandas as pd


def load_assets_json(path: Path) -> list[dict]:
    """Load assets from assets.json file.

    Args:
        path: Path to assets.json file

    Returns:
        List of asset dictionaries
    """
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("assets", [])


def parse_numeric_version(text: str) -> tuple:
    """Extract numeric version tuple for sorting.

    Examples:
        "2.9.1" -> (2, 9, 1)
        "3.10" -> (3, 10)
    """
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


def get_tag_from_url(url: str) -> str:
    """Extract tag from GitHub release URL.

    Examples:
        "https://github.com/user/repo/releases/download/v1.0.0/file.whl" -> "v1.0.0"
    """
    if pd.isna(url) or not url:
        return ""
    match = re.search(r"/releases/download/([^/]+)/", str(url))
    return match.group(1) if match else ""


def get_os_emoji(os_name: str) -> str:
    """Get emoji for OS name.

    Args:
        os_name: OS name (e.g., "Linux x86_64", "Windows")

    Returns:
        Emoji string with trailing space, or empty string
    """
    os_lower = os_name.lower()
    if "linux" in os_lower:
        return "🐧 "
    elif "windows" in os_lower:
        return "🪟 "
    else:
        return ""


def collect_versions_from_assets(
    assets: Iterable[dict],
) -> dict[str, dict[str, set[str]]]:
    """Collect version information from assets, grouped by platform.

    Args:
        assets: Iterable of asset dictionaries with "name" key

    Returns:
        Dictionary mapping platform name to version sets:
        {
            "Linux x86_64": {
                "flash_versions": {"2.6.3", "2.7.4"},
                "python_versions": {"3.10", "3.11"},
                "torch_versions": {"2.5", "2.6"},
                "cuda_versions": {"12.4", "13.0"}
            },
            ...
        }
    """
    aggregated: dict[str, dict[str, set[str]]] = {}

    for asset in assets:
        name = asset.get("name", "")
        if not name.endswith(".whl"):
            continue

        info = parse_wheel_filename(name)
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
    """Format a set of version strings as comma-separated sorted string.

    Args:
        values: Set of version strings

    Returns:
        Comma-separated sorted string, or "-" if empty
    """
    if not values:
        return "-"
    return ", ".join(sorted(values))


def parse_wheel_filename(filename: str) -> dict | None:
    """
    Extract information from a wheel filename.
    Examples:
        flash_attn-2.6.3+cu124torch2.5-cp311-cp311-linux_x86_64.whl
        flash_attn-2.7.4+cu124torch2.6-cp311-cp311-linux_x86_64.whl
        flash_attn-2.7.4.post1+cu130torch2.9-cp310-cp310-linux_x86_64.whl
        flash_attn-2.8.3+cu128torch2.9-cp313-cp313-manylinux_2_34_x86_64.whl
        flash_attn-2.6.3+cu128torch2.9-cp310-cp310-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl

    ---
    Wheel filename から情報を抽出
    例: flash_attn-2.6.3+cu124torch2.5-cp311-cp311-linux_x86_64.whl
        flash_attn-2.7.4+cu124torch2.6-cp311-cp311-linux_x86_64.whl
        flash_attn-2.7.4.post1+cu130torch2.9-cp310-cp310-linux_x86_64.whl
        flash_attn-2.6.3+cu128torch2.9-cp310-cp310-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl
    """
    # Flash Attention wheelのパターンに合わせて正規表現を調整
    # PyTorchバージョンはマイナーバージョン1桁の形式も対応 (例: torch2.9)
    # post1 のようなバージョンサフィックスにも対応 (例: 2.7.4.post1)
    # manylinux の複数タグにも対応 (例: manylinux_2_24_x86_64.manylinux_2_28_x86_64)
    pattern = r"flash_attn-(\d+\.\d+\.\d+(?:\.[a-z0-9]+)?)\+cu(\d+)torch(\d+\.\d+)-cp(\d+)-cp\d+-(.+?)\.whl"
    match = re.match(pattern, filename)

    if match:
        flash_version = match.group(1)
        cuda_version = f"{match.group(2)[:2]}.{match.group(2)[2:]}"  # 130 -> 13.0
        torch_version = match.group(3)
        python_version = f"{match.group(4)[:1]}.{match.group(4)[1:]}"  # 310 -> 3.10
        platform = match.group(5)  # linux_x86_64, win32など

        return {
            "flash_version": flash_version,
            "cuda_version": cuda_version,
            "torch_version": torch_version,
            "python_version": python_version,
            "platform": platform,
        }
    return None


def normalize_platform_name(raw: str) -> str:
    """Platform name normalization
    Examples:
        linux -> Linux
        linux_x86_64 -> Linux x86_64
        manylinux_2_34_x86_64 -> Manylinux 2_34 x86_64
        manylinux_2_17_aarch64 -> Manylinux 2_17 arm64
        manylinux_2_24_x86_64.manylinux_2_28_x86_64 -> Manylinux 2_24 x86_64
        win32 -> Windows
        amd64 -> x86_64
    """
    # Handle manylinux format with multiple tags: use only the first tag
    # Example: manylinux_2_24_x86_64.manylinux_2_28_x86_64 -> manylinux_2_24_x86_64
    if "." in raw and raw.startswith("manylinux"):
        raw = raw.split(".")[0]

    # Handle manylinux format: manylinux_X_Y_ARCH -> Manylinux X_Y ARCH
    if raw.startswith("manylinux"):
        # Extract parts from manylinux_X_Y_ARCH format
        # Examples: manylinux_2_34_x86_64, manylinux_2_17_aarch64
        parts = raw.split("_")
        if len(parts) >= 4:
            # parts[0] = 'manylinux', parts[1] = X, parts[2] = Y, parts[3:] = ARCH parts
            # ARCH can contain underscores (e.g., x86_64)
            version = f"{parts[1]}_{parts[2]}"
            arch = "_".join(parts[3:])  # Join remaining parts for arch (e.g., x86_64)
            # Apply architecture normalization
            if arch == "aarch64":
                arch = "arm64"
            return f"Manylinux {version} {arch}"

    name = raw[:1].upper() + raw[1:]  # linux -> Linux
    name = name.replace("_", " ", 1)  # linux_x86_64 -> Linux x86_64
    if "Win" in name:
        name = name.replace("Win", "Windows")
    if "amd64" in name:
        name = name.replace("amd64", "x86_64")
    if "aarch64" in name:
        name = name.replace("aarch64", "arm64")
    return name

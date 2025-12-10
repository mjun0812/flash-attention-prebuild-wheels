import re


def parse_wheel_filename(filename: str) -> dict | None:
    """
    Extract information from a wheel filename.
    Examples:
        flash_attn-2.6.3+cu124torch2.5-cp311-cp311-linux_x86_64.whl
        flash_attn-2.7.4+cu124torch2.6-cp311-cp311-linux_x86_64.whl
        flash_attn-2.7.4.post1+cu130torch2.9-cp310-cp310-linux_x86_64.whl
        flash_attn-2.8.3+cu128torch2.9-cp313-cp313-manylinux_2_34_x86_64.whl

    ---
    Wheel filename から情報を抽出
    例: flash_attn-2.6.3+cu124torch2.5-cp311-cp311-linux_x86_64.whl
        flash_attn-2.7.4+cu124torch2.6-cp311-cp311-linux_x86_64.whl
        flash_attn-2.7.4.post1+cu130torch2.9-cp310-cp310-linux_x86_64.whl
    """
    # Flash Attention wheelのパターンに合わせて正規表現を調整
    # PyTorchバージョンはマイナーバージョン1桁の形式も対応 (例: torch2.9)
    # post1 のようなバージョンサフィックスにも対応 (例: 2.7.4.post1)
    pattern = r"flash_attn-(\d+\.\d+\.\d+(?:\.[a-z0-9]+)?)\+cu(\d+)torch(\d+\.\d+)-cp(\d+)-cp\d+-(\w+)\.whl"
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
        win32 -> Windows
        amd64 -> x86_64
    """
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

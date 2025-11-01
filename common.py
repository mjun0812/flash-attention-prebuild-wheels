import re


def parse_wheel_filename(filename: str) -> dict | None:
    """
    Wheel filename から情報を抽出
    例: flash_attn-2.6.3+cu124torch2.5-cp311-cp311-linux_x86_64.whl
        flash_attn-2.7.4+cu124torch2.6-cp311-cp311-linux_x86_64.whl
        flash_attn-2.7.4.post1+cu130torch2.9-cp310-cp310-linux_x86_64.whl
    """
    # Flash Attention wheelのパターンに合わせて正規表現を調整
    # PyTorchバージョンはマイナーバージョン1桁の形式も対応 (例: torch2.9)
    # post1 のようなバージョンサフィックスにも対応 (例: 2.7.4.post1)
    pattern = (
        r"flash_attn-(\d+\.\d+\.\d+(?:\.[a-z0-9]+)?)\+cu(\d+)torch(\d+\.\d+)-cp(\d+)-cp\d+-(\w+)\.whl"
    )
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
        win32 -> Windows
        amd64 -> x86_64
    """
    name = raw[:1].upper() + raw[1:]  # linux -> Linux
    name = name.replace("_", " ", 1)  # linux_x86_64 -> Linux x86_64
    if "Win" in name:
        name = name.replace("Win", "Windows")
    if "amd64" in name:
        name = name.replace("amd64", "x86_64")
    return name

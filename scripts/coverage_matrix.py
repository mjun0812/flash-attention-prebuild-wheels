"""Coverage matrix definitions for wheel availability checks."""

FA3_STABLE_COMMIT = "fa3:e2743ab5b3803bb672b16437ba98a3b1d4576c50"

OS = ["linux_x86_64", "linux_arm64", "windows"]
PYTHON_VERSIONS = ["3.10", "3.11", "3.12", "3.13", "3.14"]
TORCH_FULL_VERSIONS = [
    "2.0.1",
    "2.1.2",
    "2.2.2",
    "2.3.1",
    "2.4.1",
    "2.5.1",
    "2.6.0",
    "2.7.1",
    "2.8.0",
    "2.9.1",
    "2.10.0",
    "2.11.0",
]
TORCH_SUPPORT_CUDA_VERSIONS = {
    "2.0": ("11.7", "11.8"),
    "2.1": ("11.8", "12.1"),
    "2.2": ("11.8", "12.1"),
    "2.3": ("11.8", "12.1"),
    "2.4": ("11.8", "12.1", "12.4"),
    "2.5": ("11.8", "12.1", "12.4"),
    "2.6": ("11.8", "12.4", "12.6"),
    "2.7": ("11.8", "12.6", "12.8"),
    "2.8": ("12.6", "12.8", "12.9"),
    "2.9": ("12.6", "12.8", "13.0"),
    "2.10": ("12.6", "12.8", "13.0"),
    "2.11": ("12.6", "12.8", "12.9", "13.0"),
}
# torch_version: minimum and maximum supported Python versions
TORCH_SUPPORT_PYTHON_VERSIONS = {
    "2.0": ("3.8", "3.11"),
    "2.1": ("3.8", "3.11"),
    "2.2": ("3.8", "3.12"),
    "2.3": ("3.8", "3.12"),
    "2.4": ("3.8", "3.12"),
    "2.5": ("3.8", "3.13"),
    "2.6": ("3.9", "3.13"),
    "2.7": ("3.9", "3.13"),
    "2.8": ("3.9", "3.13"),
    "2.9": ("3.10", "3.14"),
    "2.10": ("3.10", "3.14"),
    "2.11": ("3.10", "3.14"),
}

# CUDA_VERSIONS: CUDA version using PyTorch. e.g., ["11.7", "11.8", ...]
# This will be generated from TORCH_SUPPORT_CUDA_VERSIONS
CUDA_VERSIONS = [
    v for versions in TORCH_SUPPORT_CUDA_VERSIONS.values() for v in versions
]  # Flatten the list of CUDA versions from the support mapping
CUDA_VERSIONS = sorted(set(CUDA_VERSIONS))

EXCLUDE = []
# Exclude incompatible CUDA versions for each PyTorch version
for torch_version, torch_cuda_versions in TORCH_SUPPORT_CUDA_VERSIONS.items():
    torch_full_version = next(
        v for v in TORCH_FULL_VERSIONS if v.startswith(f"{torch_version}.")
    )
    for cuda_version in CUDA_VERSIONS:
        if cuda_version not in torch_cuda_versions:
            EXCLUDE.append(
                {"torch-version": torch_full_version, "cuda-version": cuda_version}
            )
# Exclude incompatible Python versions for each PyTorch version
for torch_version, (min_py, max_py) in TORCH_SUPPORT_PYTHON_VERSIONS.items():
    torch_full_version = next(
        v for v in TORCH_FULL_VERSIONS if v.startswith(f"{torch_version}.")
    )
    for python_version in PYTHON_VERSIONS:
        if not (min_py <= python_version <= max_py):
            EXCLUDE.append(
                {"torch-version": torch_full_version, "python-version": python_version}
            )

LINUX_MATRIX = {
    "flash-attn-version": ["2.6.3", "2.7.4", "2.8.3", FA3_STABLE_COMMIT],
    "python-version": PYTHON_VERSIONS + ["3.14t"],
    "torch-version": ["2.5.1", "2.6.0", "2.7.1", "2.8.0", "2.9.1", "2.10.0", "2.11.0"],
    "cuda-version": ["12.4", "12.6", "12.8", "12.9", "13.0"],
}

LINUX_ARM64_MATRIX = {
    "flash-attn-version": ["2.8.3", FA3_STABLE_COMMIT],
    "python-version": PYTHON_VERSIONS,
    "torch-version": ["2.9.1", "2.10.0", "2.11.0"],
    "cuda-version": ["12.6", "12.8", "12.9", "13.0"],
}

WINDOWS_MATRIX = {
    "flash-attn-version": ["2.8.3", FA3_STABLE_COMMIT],
    "python-version": PYTHON_VERSIONS,
    "torch-version": ["2.9.1", "2.10.0", "2.11.0"],
    "cuda-version": ["12.6", "12.8", "13.0"],
}

_PLATFORM_MATRICES = {
    "linux": LINUX_MATRIX,
    "linux_arm64": LINUX_ARM64_MATRIX,
    "windows": WINDOWS_MATRIX,
}


def get_python_versions_for_platform(platform: str) -> list[str]:
    """Get the list of Python versions defined in the matrix for a platform.

    Args:
        platform: Normalized platform key ("linux", "linux_arm64", "windows").

    Returns:
        List of Python version strings (e.g., ["3.10", "3.11", "3.12"]).
    """
    matrix = _PLATFORM_MATRICES.get(platform, {})
    return matrix.get("python-version", [])

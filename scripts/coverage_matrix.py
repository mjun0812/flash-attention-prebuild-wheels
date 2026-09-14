"""Coverage matrix definitions and helpers for wheel availability checks."""

CoverageMatrix = dict[str, list[str]]

FA3_STABLE_COMMIT = "fa3:e2743ab5b3803bb672b16437ba98a3b1d4576c50"

OS = ["linux_x86_64", "linux_arm64", "windows"]
PYTHON_VERSIONS = ["3.10", "3.11", "3.12", "3.13", "3.14"]
FREE_THREADED_PYTHON_VERSIONS = ["3.13t", "3.14t"]
ALL_PYTHON_VERSIONS = PYTHON_VERSIONS + FREE_THREADED_PYTHON_VERSIONS
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
    "2.12.1",
    "2.13.0",
    "2.14.0",
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
    "2.11": ("12.6", "12.8", "13.0"),
    "2.12": ("12.6", "13.0", "13.2"),
    "2.13": ("12.6", "13.0", "13.2"),
    "2.14": ("12.6", "13.0", "13.2"),
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
    "2.12": ("3.10", "3.14"),
    "2.13": ("3.10", "3.14"),
    "2.14": ("3.10", "3.14"),
}
# torch_version: ROCm versions whose PyTorch index (download.pytorch.org/whl/rocmX.Y)
# ships that torch release. ROCm keeps the dot (7.2, 7.14) because both rocm7.1
# and rocm7.14 exist; see ADR 0002.
TORCH_SUPPORT_ROCM_VERSIONS = {
    "2.13": ("7.1", "7.2"),
    "2.14": ("7.2", "7.14"),
}
TORCH_EXPERIMENTAL_FREE_THREADED_PYTHON_VERSIONS = {
    "2.6": ("3.13t",),
    "2.7": ("3.13t",),
    "2.8": ("3.13t",),
    "2.9": ("3.13t", "3.14t"),
    "2.10": ("3.13t", "3.14t"),
    "2.11": ("3.13t", "3.14t"),
    "2.12": ("3.14t",),
    "2.13": ("3.14t",),
    "2.14": ("3.14t",),
}

# FA3 is distributed as a single ABI3 wheel per (torch, cuda) combination, so
# it covers only non-free-threaded CPython interpreters. The entry in each
# platform matrix therefore represents one wheel across all regular Python
# versions; free-threaded builds (e.g., "3.14t") are not covered.
FA3_VERSION_PREFIX = "fa3:"


def is_fa3_version(flash_version: str) -> bool:
    """Return whether the flash-attn version string refers to an FA3 build."""
    return flash_version.startswith(FA3_VERSION_PREFIX)


# CUDA_VERSIONS: CUDA version using PyTorch. e.g., ["11.7", "11.8", ...]
# This will be generated from TORCH_SUPPORT_CUDA_VERSIONS
CUDA_VERSIONS = [
    v for versions in TORCH_SUPPORT_CUDA_VERSIONS.values() for v in versions
]  # Flatten the list of CUDA versions from the support mapping
CUDA_VERSIONS = sorted(set(CUDA_VERSIONS))
ROCM_VERSIONS = sorted(
    {v for versions in TORCH_SUPPORT_ROCM_VERSIONS.values() for v in versions}
)


def parse_python_version(version: str) -> tuple[int, int]:
    """Parse a Python version string to a comparable tuple.

    Args:
        version: Python version string such as "3.14" or "3.14t".

    Returns:
        Comparable (major, minor) tuple.
    """
    normalized = version.removesuffix("t")
    major, minor = normalized.split(".")
    return int(major), int(minor)


def is_free_threaded_python(version: str) -> bool:
    """Return whether the Python version is a free-threaded build."""
    return version.endswith("t")


def is_supported_python_version(torch_version: str, python_version: str) -> bool:
    """Return whether a Python version is supported by a torch version.

    Free-threaded Python support is tracked separately because it is still
    experimental and should not be inferred from the normal CPython range.

    Args:
        torch_version: Torch minor version string such as "2.10".
        python_version: Python version string such as "3.14" or "3.14t".

    Returns:
        True if the Python version is supported for the torch version.
    """
    min_py, max_py = TORCH_SUPPORT_PYTHON_VERSIONS[torch_version]
    parsed_python_version = parse_python_version(python_version)
    if not (
        parse_python_version(min_py)
        <= parsed_python_version
        <= parse_python_version(max_py)
    ):
        return False

    if not is_free_threaded_python(python_version):
        return True

    return python_version in TORCH_EXPERIMENTAL_FREE_THREADED_PYTHON_VERSIONS.get(
        torch_version, ()
    )


# The CI matrix `exclude` lists are keyed by accelerator: a CUDA job's matrix
# has no rocm-version key and vice versa, so each accelerator gets its own list
# (EXCLUDE for CUDA jobs, EXCLUDE_ROCM for the ROCm job) sharing the
# accelerator-independent entries.
_EXCLUDE_CUDA = []
# Exclude incompatible CUDA versions for each PyTorch version
for torch_version, torch_cuda_versions in TORCH_SUPPORT_CUDA_VERSIONS.items():
    torch_full_version = next(
        v for v in TORCH_FULL_VERSIONS if v.startswith(f"{torch_version}.")
    )
    for cuda_version in CUDA_VERSIONS:
        if cuda_version not in torch_cuda_versions:
            _EXCLUDE_CUDA.append(
                {"torch-version": torch_full_version, "cuda-version": cuda_version}
            )
# Exclude ROCm versions whose PyTorch index does not ship that torch release
_EXCLUDE_ROCM = []
for torch_version in TORCH_SUPPORT_CUDA_VERSIONS:
    torch_full_version = next(
        v for v in TORCH_FULL_VERSIONS if v.startswith(f"{torch_version}.")
    )
    torch_rocm_versions = TORCH_SUPPORT_ROCM_VERSIONS.get(torch_version, ())
    for rocm_version in ROCM_VERSIONS:
        if rocm_version not in torch_rocm_versions:
            _EXCLUDE_ROCM.append(
                {"torch-version": torch_full_version, "rocm-version": rocm_version}
            )
_EXCLUDE_COMMON = []
# Exclude incompatible Python versions for each PyTorch version
for torch_version, (min_py, max_py) in TORCH_SUPPORT_PYTHON_VERSIONS.items():
    torch_full_version = next(
        v for v in TORCH_FULL_VERSIONS if v.startswith(f"{torch_version}.")
    )
    for python_version in ALL_PYTHON_VERSIONS:
        if not is_supported_python_version(torch_version, python_version):
            _EXCLUDE_COMMON.append(
                {"torch-version": torch_full_version, "python-version": python_version}
            )
# FA3 is an ABI3 wheel that does not support free-threaded CPython builds.
# Exclude those combinations so the expected matrix does not count them as
# missing wheels.
for python_version in FREE_THREADED_PYTHON_VERSIONS:
    _EXCLUDE_COMMON.append(
        {
            "flash-attn-version": FA3_STABLE_COMMIT,
            "python-version": python_version,
        }
    )
EXCLUDE = _EXCLUDE_CUDA + _EXCLUDE_COMMON
EXCLUDE_ROCM = _EXCLUDE_ROCM + _EXCLUDE_COMMON


LINUX_MATRIX = {
    "flash-attn-version": ["2.6.3", "2.7.4", "2.8.3", FA3_STABLE_COMMIT],
    "python-version": ALL_PYTHON_VERSIONS,
    "torch-version": [
        "2.5.1",
        "2.6.0",
        "2.7.1",
        "2.8.0",
        "2.9.1",
        "2.10.0",
        "2.11.0",
        "2.12.1",
        "2.13.0",
        "2.14.0",
    ],
    "cuda-version": ["12.4", "12.6", "12.8", "12.9", "13.0", "13.2"],
}

LINUX_ARM64_MATRIX = {
    "flash-attn-version": ["2.8.3", FA3_STABLE_COMMIT],
    "python-version": ALL_PYTHON_VERSIONS,
    "torch-version": [
        "2.9.1",
        "2.10.0",
        "2.11.0",
        "2.12.1",
        "2.13.0",
        "2.14.0",
    ],
    "cuda-version": ["12.6", "12.8", "12.9", "13.0", "13.2"],
}

# Windows excludes "3.14t" because torch 2.12.x's setuptools/cpp_extension cannot
# resolve the free-threaded import library on Windows
# (LNK1104: python314.lib vs python314t.lib). 3.13t is pruned for torch
# 2.12.1/2.13.0/2.14.0 by TORCH_EXPERIMENTAL_FREE_THREADED_PYTHON_VERSIONS because
# those versions do not publish cp313t wheels.
WINDOWS_PYTHON_VERSIONS = [*PYTHON_VERSIONS, "3.13t"]

WINDOWS_MATRIX = {
    "flash-attn-version": ["2.8.3", FA3_STABLE_COMMIT],
    "python-version": WINDOWS_PYTHON_VERSIONS,
    "torch-version": [
        "2.9.1",
        "2.10.0",
        "2.11.0",
        "2.12.1",
        "2.13.0",
        "2.14.0",
    ],
    "cuda-version": ["12.6", "12.8", "13.0", "13.2"],
}

# ROCm wheels: FA2 only (FA3 has no Composable Kernel path), Linux x86_64 only
# (PyTorch ships no aarch64 / Windows ROCm wheels). Free-threaded CPython is
# not built yet even though the ROCm torch index does ship cp314t wheels.
# Uses "rocm-version" in place of "cuda-version" as the accelerator axis.
LINUX_ROCM_MATRIX = {
    "flash-attn-version": ["2.8.3"],
    "python-version": PYTHON_VERSIONS,
    "torch-version": ["2.14.0"],
    "rocm-version": ["7.2"],
}

_PLATFORM_MATRICES = {
    "linux": LINUX_MATRIX,
    "linux_rocm": LINUX_ROCM_MATRIX,
    "linux_arm64": LINUX_ARM64_MATRIX,
    "windows": WINDOWS_MATRIX,
}


def get_platform_matrix(platform: str) -> CoverageMatrix:
    """Get the coverage matrix for a platform.

    Args:
        platform: Normalized platform key ("linux", "linux_rocm", "linux_arm64", "windows").

    Returns:
        Coverage matrix for the platform. Returns an empty dict if unsupported.
    """
    return _PLATFORM_MATRICES.get(platform, {})


def get_matrix_accelerator(matrix: CoverageMatrix) -> str:
    """Return which accelerator axis a matrix uses ("cuda" or "rocm")."""
    return "rocm" if "rocm-version" in matrix else "cuda"


def get_matrix_accelerator_versions(matrix: CoverageMatrix) -> list[str]:
    """Return the accelerator version axis of a matrix (cuda-version or rocm-version)."""
    return matrix.get(f"{get_matrix_accelerator(matrix)}-version", [])


def get_python_versions_for_platform(platform: str) -> list[str]:
    """Get the list of Python versions defined in the matrix for a platform.

    Args:
        platform: Normalized platform key ("linux", "linux_arm64", "windows").

    Returns:
        List of Python version strings (e.g., ["3.10", "3.11", "3.12"]).
    """
    matrix = get_platform_matrix(platform)
    return matrix.get("python-version", [])


def get_non_free_threaded_python_versions_for_platform(platform: str) -> list[str]:
    """Get non-free-threaded Python versions defined in the matrix for a platform.

    Args:
        platform: Normalized platform key ("linux", "linux_arm64", "windows").

    Returns:
        List of non-free-threaded Python version strings.
    """
    return [
        version
        for version in get_python_versions_for_platform(platform)
        if not is_free_threaded_python(version)
    ]


def normalize_torch_version(version: str) -> str:
    """Convert full torch version to a major.minor string for comparison.

    Args:
        version: Full or partial torch version string.

    Returns:
        Normalized torch version string.
    """
    parts = version.split(".")
    if len(parts) >= 2:
        return f"{parts[0]}.{parts[1]}"
    return version


def is_excluded_combination(
    flash_version: str,
    python_version: str,
    torch_version: str,
    accelerator_version: str,
    accelerator: str = "cuda",
) -> bool:
    """Check whether a matrix combination is excluded.

    Args:
        flash_version: Flash-Attention version in the matrix.
        python_version: Python version in the matrix.
        torch_version: Full torch version in the matrix.
        accelerator_version: CUDA or ROCm version in the matrix.
        accelerator: "cuda" or "rocm"; selects which exclusion entries apply.

    Returns:
        True when the combination is excluded by the coverage matrix rules.
    """
    for excluded in EXCLUDE + _EXCLUDE_ROCM:
        match = True
        if (
            "flash-attn-version" in excluded
            and excluded["flash-attn-version"] != flash_version
        ):
            match = False
        if (
            "python-version" in excluded
            and excluded["python-version"] != python_version
        ):
            match = False
        if "torch-version" in excluded and excluded["torch-version"] != torch_version:
            match = False
        # An entry keyed by the other accelerator never applies to this one.
        for key_accelerator in ("cuda", "rocm"):
            key = f"{key_accelerator}-version"
            if key in excluded and (
                key_accelerator != accelerator or excluded[key] != accelerator_version
            ):
                match = False
        if match:
            return True
    return False


def generate_expected_matrix(
    matrix: CoverageMatrix,
) -> list[tuple[str, str, str, str]]:
    """Generate all expected flash/python/torch/accelerator combinations.

    Args:
        matrix: Coverage matrix definition (cuda-version or rocm-version axis).

    Returns:
        List of matrix combinations; the last element is the CUDA or ROCm version.
    """
    combinations: list[tuple[str, str, str, str]] = []
    accelerator_versions = get_matrix_accelerator_versions(matrix)
    for flash_version in matrix.get("flash-attn-version", []):
        for python_version in matrix.get("python-version", []):
            for torch_version in matrix.get("torch-version", []):
                for accelerator_version in accelerator_versions:
                    combinations.append(
                        (
                            flash_version,
                            python_version,
                            torch_version,
                            accelerator_version,
                        )
                    )
    return combinations

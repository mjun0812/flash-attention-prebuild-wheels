"""Coverage matrix definitions for wheel availability checks."""

LINUX_MATRIX = {
    "flash-attn-version": [
        "2.6.3",
        "2.7.4",
        "2.8.3",
    ],
    "python-version": [
        "3.10",
        "3.11",
        "3.12",
        "3.13",
        "3.14",
    ],
    "torch-version": [
        "2.5.1",
        "2.6.0",
        "2.7.1",
        "2.8.0",
        "2.9.1",
        "2.10.0",
    ],
    "cuda-version": [
        "12.4",
        "12.6",
        "12.8",
        "13.0",
    ],
}

LINUX_ARM64_MATRIX = {
    "flash-attn-version": [
        "2.8.3",
    ],
    "python-version": [
        "3.10",
        "3.11",
        "3.12",
        "3.13",
        "3.14",
    ],
    "torch-version": [
        "2.9.1",
        "2.10.0",
    ],
    "cuda-version": [
        "12.6",
        "12.8",
        "13.0",
    ],
}

WINDOWS_MATRIX = {
    "flash-attn-version": [
        "2.8.3",
    ],
    "python-version": [
        "3.10",
        "3.11",
        "3.12",
        "3.13",
        "3.14",
    ],
    "torch-version": [
        "2.9.1",
        "2.10.0",
    ],
    "cuda-version": [
        "12.6",
        "12.8",
        "13.0",
    ],
}

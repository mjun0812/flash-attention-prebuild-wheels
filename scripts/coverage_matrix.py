"""Coverage matrix definitions for wheel availability checks."""

EXCLUDE = [
    # torch < 2.2 does not support Python 3.12
    {"python-version": "3.12", "torch-version": "2.0.1"},
    {"python-version": "3.12", "torch-version": "2.1.2"},
    # torch 2.0.1 does not support CUDA 12.x
    {"torch-version": "2.0.1", "cuda-version": "12.1"},
    {"torch-version": "2.0.1", "cuda-version": "12.4"},
    {"torch-version": "2.0.1", "cuda-version": "12.6"},
    {"torch-version": "2.0.1", "cuda-version": "12.8"},
    # torch 2.5.1 only supports CUDA 11.8, 12.1, 12.4
    {"torch-version": "2.5.1", "cuda-version": "12.6"},
    {"torch-version": "2.5.1", "cuda-version": "12.8"},
    {"torch-version": "2.5.1", "cuda-version": "12.9"},
    {"torch-version": "2.5.1", "cuda-version": "13.0"},
    # torch 2.6.0 only supports CUDA 11.8, 12.4, 12.6
    {"torch-version": "2.6.0", "cuda-version": "12.1"},
    {"torch-version": "2.6.0", "cuda-version": "12.8"},
    {"torch-version": "2.6.0", "cuda-version": "12.9"},
    {"torch-version": "2.6.0", "cuda-version": "13.0"},
    # torch 2.7.1 only supports CUDA 11.8, 12.6, 12.8
    {"torch-version": "2.7.1", "cuda-version": "12.4"},
    {"torch-version": "2.7.1", "cuda-version": "12.9"},
    {"torch-version": "2.7.1", "cuda-version": "13.0"},
    # torch 2.8.0 only supports CUDA 12.6, 12.8, 12.9
    {"torch-version": "2.8.0", "cuda-version": "12.4"},
    {"torch-version": "2.8.0", "cuda-version": "13.0"},
    # torch 2.9.1 only supports CUDA 12.6, 12.8, 13.0
    {"torch-version": "2.9.1", "cuda-version": "12.4"},
    {"torch-version": "2.9.1", "cuda-version": "12.9"},
    # torch 2.10.0 only supports CUDA 12.6, 12.8, 13.0
    {"torch-version": "2.10.0", "cuda-version": "12.4"},
    {"torch-version": "2.10.0", "cuda-version": "12.9"},
    # torch < 2.6 does not support Python 3.13
    {"torch-version": "2.5.1", "python-version": "3.13"},
    # torch >= 2.9 does not support Python 3.9
    {"torch-version": "2.9.1", "python-version": "3.9"},
    {"torch-version": "2.10.0", "python-version": "3.9"},
    # torch < 2.9 does not support Python 3.14
    {"torch-version": "2.5.1", "python-version": "3.14"},
    {"torch-version": "2.6.0", "python-version": "3.14"},
    {"torch-version": "2.7.1", "python-version": "3.14"},
    {"torch-version": "2.8.0", "python-version": "3.14"},
]

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

import json

from scripts.coverage_matrix import EXCLUDE

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
    ],
    "torch-version": [
        "2.5.1",
        "2.6.0",
        "2.7.1",
        "2.8.0",
        "2.9.1",
        # "2.10.0",
    ],
    "cuda-version": [
        "12.4",
        # "12.6",
        "12.8",
        # "12.9",
        "13.0",
    ],
}

LINUX_ARM64_MATRIX = {
    "flash-attn-version": [
        # "2.6.3",
        # "2.7.4",
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
        # "2.5.1",
        # "2.6.0",
        # "2.7.1",
        # "2.8.0",
        "2.9.1",
        "2.10.0",
    ],
    "cuda-version": [
        # "12.4",
        "12.6",
        "12.8",
        # "12.9",
        "13.0",
    ],
}

LINUX_SELF_HOSTED_MATRIX = {
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
        # "2.5.1",
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
        # "12.9",
        "13.0",
    ],
}

LINUX_ARM64_SELF_HOSTED_MATRIX = {
    "flash-attn-version": [
        # "2.6.3",
        # "2.7.4",
        "2.8.3",
    ],
    "python-version": [
        # "3.10",
        # "3.11",
        # "3.12",
        # "3.13",
        "3.14",
    ],
    "torch-version": [
        # "2.5.1",
        # "2.6.0",
        # "2.7.1",
        # "2.8.0",
        "2.9.1",
        # "2.10.0",
    ],
    "cuda-version": [
        # "12.4",
        # "12.6",
        # "12.8",
        # "12.9",
        "13.0",
    ],
}

WINDOWS_MATRIX = {
    "flash-attn-version": [
        # "2.6.3",
        # "2.7.4",
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
        # "2.5.1",
        # "2.6.0",
        # "2.7.1",
        # "2.8.0",
        # "2.9.1",
        "2.10.0",
    ],
    "cuda-version": [
        # "12.4",
        "12.6",
        "12.8",
        # "12.9",
        "13.0",
    ],
}

WINDOWS_CODEBUILD_MATRIX = {
    "flash-attn-version": [
        # "2.6.3",
        # "2.7.4.post1",
        "2.8.3",
    ],
    "python-version": [
        # "3.10",
        # "3.11",
        "3.12",
        # "3.13",
    ],
    "torch-version": [
        "2.9.1",
        # "2.10.0",
    ],
    "cuda-version": [
        "12.8",
        # "13.0",
    ],
}

WINDOWS_SELF_HOSTED_MATRIX = {
    "flash-attn-version": [
        # "2.6.3",
        # "2.7.4",
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
        # "2.5.1",
        # "2.6.0",
        # "2.7.1",
        # "2.8.0",
        "2.9.1",
        "2.10.0",
    ],
    "cuda-version": [
        # "12.4",
        # "12.6",
        "12.8",
        # "12.9",
        "13.0",
    ],
}


def main():
    print(
        json.dumps(
            {
                "linux": False,
                # "linux": LINUX_MATRIX,
                #
                # "linux_arm64": False,
                "linux_arm64": LINUX_ARM64_MATRIX,
                #
                # "linux_self_hosted": False,
                "linux_self_hosted": LINUX_SELF_HOSTED_MATRIX,
                #
                "linux_arm64_self_hosted": False,
                # "linux_arm64_self_hosted": LINUX_ARM64_SELF_HOSTED_MATRIX,
                #
                "windows": False,
                # "windows": WINDOWS_MATRIX,
                #
                "windows_self_hosted": False,
                # "windows_self_hosted": WINDOWS_SELF_HOSTED_MATRIX,
                #
                "windows_code_build": False,
                # "windows_code_build": WINDOWS_CODEBUILD_MATRIX,
                #
                "exclude": EXCLUDE,
            }
        )
    )


if __name__ == "__main__":
    main()

import json

from scripts.coverage_matrix import EXCLUDE

FA3_COMMIT = "fa3:e2743ab5b3803bb672b16437ba98a3b1d4576c50"


LINUX_MATRIX = {
    "flash-attn-version": [
        # "2.6.3",
        # "2.7.4",
        # "2.8.3",
    ],
    "python-version": [
        # "3.10",
        # "3.11",
        "3.12",
        # "3.13",
        # "3.13t",
        # "3.14",
        # "3.14t",
    ],
    "torch-version": [
        # "2.5.1",
        # "2.6.0",
        # "2.7.1",
        # "2.8.0",
        # "2.9.1",
        "2.10.0",
        # "2.11.0",
        # "2.12.0",
    ],
    "cuda-version": [
        # "12.4",
        # "12.6",
        "12.8",
        # "12.9",
        # "13.0",
        # "13.2",
    ],
}

# Fill the remaining FA3 ARM64 missing wheels (torch 2.9.1+cu13.0 and
# torch 2.10.0+cu12.6). FA3 is abi3, so one build python (3.12) covers all
# non-FT pythons. The base matrix expands to 2x2 = 4 (torch x cuda); the
# two already-released pairs are dropped via ARM64_FA3_ALREADY_RELEASED in
# main() below, leaving exactly the two missing builds.
LINUX_ARM64_MATRIX = {
    "flash-attn-version": [
        FA3_COMMIT,
    ],
    "python-version": [
        "3.12",  # FA3 is abi3 (cp39-abi3); one build covers all non-FT pythons
    ],
    "torch-version": [
        "2.9.1",
        "2.10.0",
    ],
    "cuda-version": [
        "12.6",
        "13.0",
    ],
}

# torch x cuda pairs already shipped in earlier releases. Added to the
# build matrix's exclude list so v0.9.40 only rebuilds the missing pair
# (2.9.1+13.0, 2.10.0+12.6). Reset alongside LINUX_ARM64_MATRIX after the
# missing wheels land.
ARM64_FA3_ALREADY_RELEASED = [
    {"torch-version": "2.9.1", "cuda-version": "12.6"},
    {"torch-version": "2.10.0", "cuda-version": "13.0"},
]

LINUX_SELF_HOSTED_MATRIX = {
    "flash-attn-version": [
        "2.6.3",
        "2.7.4",
        "2.8.3",
        FA3_COMMIT,
    ],
    "python-version": [
        # "3.10",
        # "3.11",
        # "3.12",
        # "3.13",
        # "3.14",
        "3.13t",
        # "3.14t",
    ],
    "torch-version": [
        # "2.5.1",
        "2.6.0",
        "2.7.1",
        "2.8.0",
        "2.9.1",
        "2.10.0",
        # "2.11.0",
        # "2.12.0",
    ],
    "cuda-version": [
        "12.4",
        "12.6",
        "12.8",
        "12.9",
        "13.0",
        "13.2",
    ],
}

LINUX_ARM64_SELF_HOSTED_MATRIX = {
    "flash-attn-version": [
        # "2.6.3",
        # "2.7.4",
        # "2.8.3",
        FA3_COMMIT,
    ],
    "python-version": [
        "3.10",
        # "3.11",
        # "3.12",
        # "3.13",
        # "3.13t",
        # "3.14",
        # "3.14t",
    ],
    "torch-version": [
        # "2.5.1",
        # "2.6.0",
        # "2.7.1",
        # "2.8.0",
        # "2.9.1",
        # "2.10.0",
        "2.11.0",
        "2.12.0",
    ],
    "cuda-version": [
        # "12.4",
        "12.6",
        # "12.8",
        # "12.9",
        # "13.0",
        # "13.2",
    ],
}

LINUX_NO_CONTAINER_MATRIX = {
    "flash-attn-version": [
        "2.6.3",
        "2.7.4",
        "2.8.3",
        FA3_COMMIT,
    ],
    "python-version": [
        "3.10",
        "3.11",
        "3.12",
        "3.13",
        "3.14",
        "3.13t",
        "3.14t",
    ],
    "torch-version": [
        # "2.5.1",
        # "2.6.0",
        # "2.7.1",
        # "2.8.0",
        # "2.9.1",
        # "2.10.0",
        "2.11.0",
        "2.12.0",
    ],
    "cuda-version": [
        # "12.4",
        "12.6",
        "12.8",
        # "12.9",
        "13.0",
        "13.2",
    ],
}

LINUX_ARM64_NO_CONTAINER_MATRIX = {
    "flash-attn-version": [
        # "2.6.3",
        # "2.7.4",
        # "2.8.3",
        FA3_COMMIT,
    ],
    "python-version": [
        "3.10",
        "3.11",
        "3.12",
        "3.13",
        "3.14",
        "3.13t",
        "3.14t",
    ],
    "torch-version": [
        # "2.5.1",
        # "2.6.0",
        # "2.7.1",
        # "2.8.0",
        "2.9.1",
        "2.10.0",
        "2.11.0",
        "2.12.0",
    ],
    "cuda-version": [
        # "12.4",
        "12.6",
        "12.8",
        # "12.9",
        "13.0",
        "13.2",
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
        "2.5.1",
        "2.6.0",
        "2.7.1",
        "2.8.0",
        "2.9.1",
        "2.10.0",
        "2.11.0",
        "2.12.0",
    ],
    "cuda-version": [
        "12.4",
        "12.6",
        "12.8",
        "12.9",
        "13.0",
        "13.2",
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
        # "2.11.0",
        # "2.12.0",
    ],
    "cuda-version": [
        "12.8",
        # "13.0",
        # "13.2",
    ],
}

WINDOWS_SELF_HOSTED_MATRIX = {
    "flash-attn-version": [
        "2.8.3",
        FA3_COMMIT,
    ],
    "python-version": [
        "3.10",
        "3.11",
        "3.12",
        "3.13",
        "3.14",
        "3.13t",
        # "3.14t",  # Excluded: torch 2.12.0's setuptools/cpp_extension cannot
        # resolve the free-threaded import library on Windows
        # (LNK1104: python314.lib vs python314t.lib). Re-enable once PyTorch
        # / setuptools handle this for free-threaded CPython on Windows.
    ],
    "torch-version": [
        # "2.5.1",
        # "2.6.0",
        # "2.7.1",
        # "2.8.0",
        # "2.9.1",
        # "2.10.0",
        # "2.11.0",
        "2.12.0",
    ],
    "cuda-version": [
        # "12.4",
        "12.6",
        # "12.8",
        # "12.9",
        "13.0",
        "13.2",
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
                "linux_self_hosted": False,
                # "linux_self_hosted": LINUX_SELF_HOSTED_MATRIX,
                #
                "linux_arm64_self_hosted": False,
                # "linux_arm64_self_hosted": LINUX_ARM64_SELF_HOSTED_MATRIX,
                #
                "linux_no_container": False,
                # "linux_no_container": LINUX_NO_CONTAINER_MATRIX,
                #
                "linux_arm64_no_container": False,
                # "linux_arm64_no_container": LINUX_ARM64_NO_CONTAINER_MATRIX,
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
                "exclude": EXCLUDE + ARM64_FA3_ALREADY_RELEASED,
            }
        )
    )


if __name__ == "__main__":
    main()

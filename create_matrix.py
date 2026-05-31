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

LINUX_ARM64_MATRIX = {
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

# Temporary matrix to fill missing Windows wheels.
# Step 3 of 3 (Group 3): covers 12 combinations, of which 4 are missing
# (3.12 × 2.9.1 × 13.0; 3.14 × 2.9.1 × 12.6/12.8; 3.14 × 2.10.0 × 12.8).
# Groups 1 and 2 already backfilled the torch 2.12.0 and 3.13t holes.
# The other 8 jobs are existing wheels that will be rebuilt and re-uploaded
# via --clobber.
# Restore the original (full) matrix after this final round completes.
WINDOWS_SELF_HOSTED_MATRIX = {
    "flash-attn-version": [
        "2.8.3",
        # FA3_COMMIT,  # FA3 has no missing wheels; skipped during fill-in rounds.
    ],
    "python-version": [
        # "3.10",   # No missing
        # "3.11",   # No missing
        "3.12",
        # "3.13",   # No missing
        "3.14",
        # "3.13t",  # Covered by Group 2 (v0.9.27)
        # "3.14t",  # Excluded entirely; see PR #102.
    ],
    "torch-version": [
        # "2.5.1",
        # "2.6.0",
        # "2.7.1",
        # "2.8.0",
        "2.9.1",
        "2.10.0",
        # "2.11.0",  # No missing in Group 3
        # "2.12.0",  # Covered by Group 1 (v0.9.26)
    ],
    "cuda-version": [
        # "12.4",
        "12.6",
        "12.8",
        # "12.9",
        "13.0",
        # "13.2",  # No missing in Group 3 (torch 2.9-2.10 don't support 13.2)
    ],
}


def main():
    print(
        json.dumps(
            {
                "linux": False,
                # "linux": LINUX_MATRIX,
                #
                "linux_arm64": False,
                # "linux_arm64": LINUX_ARM64_MATRIX,
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
                # "windows_self_hosted": False,
                "windows_self_hosted": WINDOWS_SELF_HOSTED_MATRIX,
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

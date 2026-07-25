"""Restore a resumable ninja build cache into a fresh flash-attention clone.

Python counterpart of the restore block in build_linux.sh, used by
build_windows.ps1 (updating tens of thousands of file mtimes is too slow in
PowerShell). Steps:

1. Validate the cached build tree (see validate_build_cache).
2. Move it into the variant's build root (flash-attention/build for FA2,
   flash-attention/hopper/build for FA3).
3. Re-initialize the cutlass submodule (a cached copy would carry a .git
   pointer into the previous runner's gitdir).
4. Push every non-cached input (repo sources, torch headers, CUDA headers)
   to 1970-01-02 so the restored .o files stay strictly newer.
5. Discover every build.ninja under the build root, verify its metadata with
   `ninja -t deps`, and re-stat the cached objects with `ninja -t restat`.

On any failure the restored build root is deleted and the script exits
non-zero so the caller falls back to a clean build.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from validate_build_cache import validate_build_cache

PAST_EPOCH = 86400  # 1970-01-02


def touch_tree_to_past(root: Path, skip: list[Path]) -> int:
    """Set the mtime of every file under ``root`` to 1970-01-02.

    Args:
        root: Directory tree to walk.
        skip: Directories to leave untouched (the restored build root).

    Returns:
        The number of files updated.
    """
    skip_resolved = {p.resolve() for p in skip}
    count = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [
            d for d in dirnames if (Path(dirpath) / d).resolve() not in skip_resolved
        ]
        for name in filenames:
            try:
                os.utime(Path(dirpath) / name, times=(PAST_EPOCH, PAST_EPOCH))
                count += 1
            except OSError:
                continue
    return count


def restat_ninja_dirs(build_root: Path) -> bool:
    """Verify and re-stat every ninja build directory under ``build_root``.

    Args:
        build_root: The restored build root.

    Returns:
        True if every discovered ninja dir passed `ninja -t deps` and
        `ninja -t restat`; False otherwise.
    """
    ninja_files = sorted(build_root.rglob("build.ninja"))
    if not ninja_files:
        print("restore-build-cache: no build.ninja found", file=sys.stderr)
        return False
    for ninja_file in ninja_files:
        ninja_dir = ninja_file.parent
        print(f"restore-build-cache: verifying {ninja_dir}")
        deps = subprocess.run(
            ["ninja", "-t", "deps"], cwd=ninja_dir, capture_output=True, check=False
        )
        if deps.returncode != 0:
            print(
                f"restore-build-cache: ninja -t deps failed in {ninja_dir}",
                file=sys.stderr,
            )
            return False
        objects = [
            str(p.relative_to(ninja_dir))
            for p in ninja_dir.rglob("*")
            if p.suffix in (".o", ".obj") and p.is_file()
        ]
        for start in range(0, len(objects), 500):
            restat = subprocess.run(
                ["ninja", "-t", "restat", *objects[start : start + 500]],
                cwd=ninja_dir,
                check=False,
            )
            if restat.returncode != 0:
                print(
                    f"restore-build-cache: ninja -t restat failed in {ninja_dir}",
                    file=sys.stderr,
                )
                return False
    return True


def main() -> int:
    """Restore the cached build tree; entry point for CLI use."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cache-root",
        type=Path,
        required=True,
        help="Cache root holding the saved build dir, e.g. ~/.fa-build-cache",
    )
    parser.add_argument(
        "--repo",
        type=Path,
        required=True,
        help="Path to the flash-attention clone",
    )
    parser.add_argument(
        "--build-root",
        type=Path,
        required=True,
        help="Destination build root, e.g. flash-attention/hopper/build",
    )
    parser.add_argument(
        "--extra-include",
        type=Path,
        action="append",
        default=[],
        help="Additional header tree to push into the past (torch include, CUDA include); repeatable",
    )
    args = parser.parse_args()
    cache_root: Path = args.cache_root.expanduser()
    cached_build = cache_root / "build"
    build_root: Path = args.build_root

    if not cached_build.is_dir():
        print(f"restore-build-cache: no cached build at {cached_build}; nothing to do")
        return 0

    print(f"restore-build-cache: restoring {cached_build} into {build_root}")
    problems = validate_build_cache(cached_build)
    if problems:
        for problem in problems:
            print(f"restore-build-cache: {problem}", file=sys.stderr)
        print("restore-build-cache: cached build failed validation; using clean build")
        shutil.rmtree(cache_root, ignore_errors=True)
        return 1

    build_root.parent.mkdir(parents=True, exist_ok=True)
    if build_root.exists():
        shutil.rmtree(build_root)
    shutil.move(str(cached_build), str(build_root))

    # Normally done inside setup.py; doing it before the past-touch keeps the
    # cutlass headers older than the cached objects.
    print("restore-build-cache: initializing cutlass submodule")
    submodule = subprocess.run(
        ["git", "-C", str(args.repo), "submodule", "update", "--init", "csrc/cutlass"],
        check=False,
    )
    if submodule.returncode != 0:
        print("restore-build-cache: cutlass submodule init failed", file=sys.stderr)
        shutil.rmtree(build_root, ignore_errors=True)
        return 1

    touched = touch_tree_to_past(args.repo, skip=[build_root])
    for include_root in args.extra_include:
        if include_root.is_dir():
            touched += touch_tree_to_past(include_root, skip=[])
    print(f"restore-build-cache: pushed {touched} input files to 1970-01-02")

    if not restat_ninja_dirs(build_root):
        print("restore-build-cache: verification failed; using clean build")
        shutil.rmtree(build_root, ignore_errors=True)
        return 1

    print("restore-build-cache: restore done")
    return 0


if __name__ == "__main__":
    sys.exit(main())

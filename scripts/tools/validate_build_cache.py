"""Validate a cached ninja build directory before save / after restore.

A resumable build cache is only worth saving (and only safe to reuse) when
the interrupted build left behind a structurally sound ninja tree. This
script checks the minimum conditions:

1. The build root exists and is a directory.
2. At least one ``build.ninja`` exists under it.
3. At least one compiled object (``.o`` / ``.obj``) exists under it.
4. Every ``.ninja_deps`` under it parses with the strict parser from
   :mod:`truncate_build_cache_mtimes` (a SIGTERM mid-write can truncate it).

Exit code 0 means the cache is usable; 1 means the caller must skip the
cache save or fall back to a clean build.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from truncate_build_cache_mtimes import NinjaDepsError, parse_ninja_deps  # noqa: E402


def validate_build_cache(build_root: Path) -> list[str]:
    """Check that ``build_root`` holds a resumable ninja build tree.

    Args:
        build_root: The cached build directory (e.g. ``~/.fa-build-cache/build``
            or ``flash-attention/hopper/build``).

    Returns:
        A list of human-readable problems; an empty list means the cache is
        valid.
    """
    if not build_root.is_dir():
        return [f"{build_root} is not a directory"]
    problems: list[str] = []
    if not any(build_root.rglob("build.ninja")):
        problems.append("no build.ninja found")
    has_objects = any(build_root.rglob("*.o")) or any(build_root.rglob("*.obj"))
    if not has_objects:
        problems.append("no .o/.obj object files found")
    for deps_path in build_root.rglob(".ninja_deps"):
        try:
            parse_ninja_deps(deps_path.read_bytes())
        except (NinjaDepsError, OSError) as exc:
            problems.append(f"{deps_path}: {exc}")
    return problems


def main() -> int:
    """Validate a build cache directory; entry point for CLI use."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "build_root",
        type=Path,
        help="Build directory to validate, e.g. ~/.fa-build-cache/build",
    )
    args = parser.parse_args()
    problems = validate_build_cache(args.build_root.expanduser())
    if problems:
        for problem in problems:
            print(f"invalid build cache: {problem}", file=sys.stderr)
        return 1
    print(f"build cache OK: {args.build_root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

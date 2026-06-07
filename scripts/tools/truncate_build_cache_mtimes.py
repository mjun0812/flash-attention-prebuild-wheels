"""Truncate mtimes in the FA build cache to second precision.

actions/cache@v4 stores its payload via GNU tar with ustar formatting, which
keeps only second-precision mtimes. ninja's .ninja_deps records mtimes at
nanosecond precision; on restore, ninja sees the .o / header mtimes as
``X.000000000`` while the recorded value is ``X.NNNNNNNNN`` and decides the
output is "dirty", forcing a full rebuild.

Run this script over ``~/.fa-build-cache`` right before actions/cache/save so
that both sides of the comparison line up at ``X.000000000`` after restore:

1. Walk every file under the cache root and truncate its stat mtime to whole
   seconds via ``os.utime(..., ns=(sec*1e9, sec*1e9))``.
2. For every ``.ninja_deps`` file under the cache root, parse the binary
   record format (header version 3 or 4) and rewrite the per-target mtime
   fields to the same whole-second value.

The script is idempotent and safe to re-run.
"""

from __future__ import annotations

import argparse
import os
import struct
import sys
from pathlib import Path

NS_PER_SEC = 1_000_000_000


def truncate_file_mtimes(root: Path) -> int:
    """Truncate stat mtimes of every file under ``root`` to whole seconds.

    Returns:
        The number of files updated.
    """
    count = 0
    for dirpath, _dirnames, filenames in os.walk(root):
        for name in filenames:
            path = Path(dirpath) / name
            try:
                st = path.stat()
            except FileNotFoundError:
                # Symlinks pointing nowhere, races, etc.
                continue
            sec = int(st.st_mtime)
            target_ns = sec * NS_PER_SEC
            if st.st_mtime_ns == target_ns:
                continue
            try:
                os.utime(path, ns=(target_ns, target_ns))
            except (PermissionError, OSError) as exc:
                print(f"warn: cannot touch {path}: {exc}", file=sys.stderr)
                continue
            count += 1
    return count


def truncate_ninja_deps(deps_path: Path) -> int:
    """Rewrite per-target mtimes in a ``.ninja_deps`` file to whole seconds.

    The on-disk format (see ``ninja/src/deps_log.cc``):

    - Header: ``"# ninjadeps\n"`` (12 bytes) followed by a little-endian
      uint32 version. Supported here: versions 3 and 4.
    - Records: each starts with a little-endian uint32 ``size_field``.
      The high bit indicates the record type, the low 31 bits hold the
      record body size in bytes.
      - Node record (high bit = 0): variable-length name + uint32 checksum.
      - Deps record (high bit = 1): uint32 out_id + int64 mtime (ns) +
        N x uint32 in_ids.

    Returns:
        The number of deps records rewritten.
    """
    if not deps_path.exists():
        return 0
    data = bytearray(deps_path.read_bytes())
    if data[:12] != b"# ninjadeps\n":
        print(f"warn: {deps_path} is not a ninja deps log; skipping", file=sys.stderr)
        return 0
    (version,) = struct.unpack_from("<I", data, 12)
    if version not in (3, 4):
        print(
            f"warn: unsupported .ninja_deps version {version} in {deps_path}; skipping",
            file=sys.stderr,
        )
        return 0
    pos = 16
    rewritten = 0
    while pos + 4 <= len(data):
        (size_field,) = struct.unpack_from("<I", data, pos)
        is_deps = (size_field >> 31) & 1
        record_size = size_field & 0x7FFFFFFF
        body_start = pos + 4
        body_end = body_start + record_size
        if body_end > len(data):
            break
        if is_deps:
            mtime_offset = body_start + 4
            if mtime_offset + 8 <= body_end:
                (mtime_ns,) = struct.unpack_from("<q", data, mtime_offset)
                sec = mtime_ns // NS_PER_SEC if mtime_ns >= 0 else -(
                    (-mtime_ns) // NS_PER_SEC
                )
                target_ns = sec * NS_PER_SEC
                if target_ns != mtime_ns:
                    struct.pack_into("<q", data, mtime_offset, target_ns)
                    rewritten += 1
        pos = body_end
    if rewritten:
        deps_path.write_bytes(bytes(data))
    return rewritten


def main() -> int:
    """Truncate cache mtimes; entry point for ``python -m scripts.tools.truncate_build_cache_mtimes``."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "root",
        type=Path,
        help="Cache root, e.g. ~/.fa-build-cache",
    )
    args = parser.parse_args()
    root: Path = args.root.expanduser()
    if not root.is_dir():
        print(f"error: {root} is not a directory", file=sys.stderr)
        return 1
    touched = truncate_file_mtimes(root)
    deps_rewritten_total = 0
    deps_files = list(root.rglob(".ninja_deps"))
    for deps in deps_files:
        deps_rewritten_total += truncate_ninja_deps(deps)
        # The file's own mtime was just bumped by the rewrite; re-truncate it
        # too so the cache stays consistent after save+restore.
        try:
            st = deps.stat()
            sec = int(st.st_mtime)
            os.utime(deps, ns=(sec * NS_PER_SEC, sec * NS_PER_SEC))
        except OSError:
            pass
    print(
        f"truncate-mtimes: touched {touched} files, rewrote {deps_rewritten_total} "
        f"deps records across {len(deps_files)} .ninja_deps files"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

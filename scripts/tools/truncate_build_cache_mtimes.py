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

A build interrupted by SIGTERM can leave a partially written ``.ninja_deps``
behind. The parser is strict: any structural corruption (bad header,
unsupported version, truncated or misaligned record) raises
:class:`NinjaDepsError` and the script exits non-zero so the caller skips the
cache save instead of persisting a broken deps log.

The script is idempotent and safe to re-run on a valid cache.
"""

from __future__ import annotations

import argparse
import os
import struct
import sys
from pathlib import Path

NS_PER_SEC = 1_000_000_000

DEPS_MAGIC = b"# ninjadeps\n"
SUPPORTED_DEPS_VERSIONS = (3, 4)
# Node record: name padded to 4 bytes (>= 4) + uint32 checksum.
MIN_NODE_RECORD_SIZE = 8
# Deps record: uint32 out_id + mtime (in_ids may be empty). The mtime is a
# uint32 in whole seconds for version 3 and an int64 in nanoseconds for
# version 4.
MIN_DEPS_RECORD_SIZE = {3: 8, 4: 12}


class NinjaDepsError(ValueError):
    """Raised when a .ninja_deps file is structurally invalid."""


def parse_ninja_deps(data: bytes) -> tuple[int, list[int]]:
    """Strictly parse a ``.ninja_deps`` payload.

    The on-disk format (see ``ninja/src/deps_log.cc``):

    - Header: ``"# ninjadeps\\n"`` (12 bytes) followed by a little-endian
      uint32 version. Supported here: versions 3 and 4.
    - Records: each starts with a little-endian uint32 ``size_field``.
      The high bit indicates the record type, the low 31 bits hold the
      record body size in bytes (always a multiple of 4).
      - Node record (high bit = 0): variable-length name + uint32 checksum.
      - Deps record (high bit = 1): uint32 out_id + mtime (4 bytes seconds
        for version 3, 8 bytes nanoseconds for version 4) + N x uint32 in_ids.

    Args:
        data: Raw bytes of the deps log.

    Returns:
        A ``(version, deps_offsets)`` tuple where ``deps_offsets`` holds the
        body-start offset of every deps record (node records are validated
        but not returned).

    Raises:
        NinjaDepsError: If the header, version, or any record is invalid,
            truncated, or misaligned.
    """
    if len(data) < 16:
        raise NinjaDepsError("file too small for ninja deps header")
    if data[:12] != DEPS_MAGIC:
        raise NinjaDepsError("bad ninja deps magic")
    (version,) = struct.unpack_from("<I", data, 12)
    if version not in SUPPORTED_DEPS_VERSIONS:
        raise NinjaDepsError(f"unsupported ninja deps version {version}")
    pos = 16
    deps_offsets: list[int] = []
    while pos < len(data):
        if pos + 4 > len(data):
            raise NinjaDepsError(f"truncated record header at offset {pos}")
        (size_field,) = struct.unpack_from("<I", data, pos)
        is_deps = bool((size_field >> 31) & 1)
        record_size = size_field & 0x7FFFFFFF
        if record_size % 4 != 0:
            raise NinjaDepsError(
                f"record size {record_size} at offset {pos} is not 4-byte aligned"
            )
        body_start = pos + 4
        body_end = body_start + record_size
        if body_end > len(data):
            raise NinjaDepsError(f"truncated record body at offset {pos}")
        min_size = MIN_DEPS_RECORD_SIZE[version] if is_deps else MIN_NODE_RECORD_SIZE
        if record_size < min_size:
            kind = "deps" if is_deps else "node"
            raise NinjaDepsError(
                f"{kind} record at offset {pos} too small ({record_size} bytes)"
            )
        if is_deps:
            deps_offsets.append(body_start)
        pos = body_end
    return version, deps_offsets


def truncate_file_mtimes(root: Path) -> int:
    """Truncate stat mtimes of every file under ``root`` to whole seconds.

    Args:
        root: Directory tree to walk.

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

    Args:
        deps_path: Path to the deps log.

    Returns:
        The number of deps records rewritten.

    Raises:
        NinjaDepsError: If the deps log is structurally invalid.
    """
    data = bytearray(deps_path.read_bytes())
    version, deps_offsets = parse_ninja_deps(bytes(data))
    if version != 4:
        # Version 3 stores mtimes as uint32 whole seconds already.
        return 0
    rewritten = 0
    for body_start in deps_offsets:
        mtime_offset = body_start + 4
        (mtime_ns,) = struct.unpack_from("<q", data, mtime_offset)
        sec = mtime_ns // NS_PER_SEC if mtime_ns >= 0 else -((-mtime_ns) // NS_PER_SEC)
        target_ns = sec * NS_PER_SEC
        if target_ns != mtime_ns:
            struct.pack_into("<q", data, mtime_offset, target_ns)
            rewritten += 1
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
        try:
            deps_rewritten_total += truncate_ninja_deps(deps)
        except NinjaDepsError as exc:
            print(f"error: {deps}: {exc}", file=sys.stderr)
            return 1
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

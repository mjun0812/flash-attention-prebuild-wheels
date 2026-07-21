"""Tests for the resumable build cache tools.

Covers the strict ``.ninja_deps`` parser, the mtime truncation used before
``actions/cache/save``, and the build cache validator, plus an integration
test against a deps log written by a real ninja binary (skipped when ninja
or a C compiler is unavailable).
"""

from __future__ import annotations

import os
import shutil
import struct
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.tools.truncate_build_cache_mtimes import (
    NS_PER_SEC,
    NinjaDepsError,
    parse_ninja_deps,
    truncate_file_mtimes,
    truncate_ninja_deps,
)
from scripts.tools.validate_build_cache import validate_build_cache

DEPS_HEADER_V4 = b"# ninjadeps\n" + struct.pack("<I", 4)


def node_record(name: bytes, node_id: int) -> bytes:
    """Build a binary node record for a synthetic deps log.

    Args:
        name: Node path name.
        node_id: Sequential node id (its bitwise complement is the checksum).

    Returns:
        The serialized record including its size header.
    """
    padding = (4 - len(name) % 4) % 4
    body = name + b"\x00" * padding + struct.pack("<I", ~node_id & 0xFFFFFFFF)
    return struct.pack("<I", len(body)) + body


def deps_record_v4(out_id: int, mtime_ns: int, in_ids: list[int]) -> bytes:
    """Build a version-4 binary deps record for a synthetic deps log.

    Args:
        out_id: Node id of the output.
        mtime_ns: Output mtime in nanoseconds.
        in_ids: Node ids of the inputs.

    Returns:
        The serialized record including its size header.
    """
    body = struct.pack("<Iq", out_id, mtime_ns)
    body += b"".join(struct.pack("<I", i) for i in in_ids)
    return struct.pack("<I", (1 << 31) | len(body)) + body


def deps_record_v3(out_id: int, mtime_sec: int, in_ids: list[int]) -> bytes:
    """Build a version-3 binary deps record (uint32 mtime in whole seconds).

    Args:
        out_id: Node id of the output.
        mtime_sec: Output mtime in seconds.
        in_ids: Node ids of the inputs.

    Returns:
        The serialized record including its size header.
    """
    body = struct.pack("<II", out_id, mtime_sec)
    body += b"".join(struct.pack("<I", i) for i in in_ids)
    return struct.pack("<I", (1 << 31) | len(body)) + body


def sample_deps_log_v4(mtime_ns: int) -> bytes:
    """Build a minimal valid version-4 deps log with one deps record.

    Args:
        mtime_ns: The output mtime recorded in the deps record.

    Returns:
        The full deps log bytes.
    """
    return (
        DEPS_HEADER_V4
        + node_record(b"a.o", 0)
        + node_record(b"a.h", 1)
        + deps_record_v4(0, mtime_ns, [1])
    )


class ParseNinjaDepsTests(unittest.TestCase):
    """Strict parser behavior on valid and corrupt deps logs."""

    def test_parses_version_4(self) -> None:
        version, offsets = parse_ninja_deps(sample_deps_log_v4(12345 * NS_PER_SEC))
        self.assertEqual(version, 4)
        self.assertEqual(len(offsets), 1)

    def test_parses_version_3(self) -> None:
        data = (
            b"# ninjadeps\n"
            + struct.pack("<I", 3)
            + node_record(b"a.o", 0)
            + deps_record_v3(0, 12345, [])
        )
        version, offsets = parse_ninja_deps(data)
        self.assertEqual(version, 3)
        self.assertEqual(len(offsets), 1)

    def test_rejects_unsupported_version(self) -> None:
        data = b"# ninjadeps\n" + struct.pack("<I", 5)
        with self.assertRaisesRegex(NinjaDepsError, "unsupported"):
            parse_ninja_deps(data)

    def test_rejects_bad_magic(self) -> None:
        with self.assertRaisesRegex(NinjaDepsError, "magic"):
            parse_ninja_deps(b"# notadeps!!\x04\x00\x00\x00")

    def test_rejects_short_header(self) -> None:
        with self.assertRaisesRegex(NinjaDepsError, "too small"):
            parse_ninja_deps(b"# ninjadeps\n")

    def test_rejects_truncated_record_header(self) -> None:
        data = sample_deps_log_v4(0) + b"\x01\x02"
        with self.assertRaisesRegex(NinjaDepsError, "truncated record header"):
            parse_ninja_deps(data)

    def test_rejects_truncated_record_body(self) -> None:
        # A SIGTERM mid-write typically cuts the last record body short.
        data = sample_deps_log_v4(0)
        with self.assertRaisesRegex(NinjaDepsError, "truncated record body"):
            parse_ninja_deps(data[:-4])

    def test_rejects_misaligned_record_size(self) -> None:
        body = b"\x00" * 10
        data = DEPS_HEADER_V4 + struct.pack("<I", len(body)) + body
        with self.assertRaisesRegex(NinjaDepsError, "not 4-byte aligned"):
            parse_ninja_deps(data)

    def test_rejects_too_small_node_record(self) -> None:
        data = DEPS_HEADER_V4 + struct.pack("<I", 4) + b"\x00" * 4
        with self.assertRaisesRegex(NinjaDepsError, "node record .* too small"):
            parse_ninja_deps(data)

    def test_rejects_too_small_deps_record(self) -> None:
        data = DEPS_HEADER_V4 + struct.pack("<I", (1 << 31) | 8) + b"\x00" * 8
        with self.assertRaisesRegex(NinjaDepsError, "deps record .* too small"):
            parse_ninja_deps(data)


class TruncateMtimesTests(unittest.TestCase):
    """mtime truncation of cache files and deps records."""

    def setUp(self) -> None:
        self.tmpdir = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmpdir)

    def test_truncate_file_mtimes_to_whole_seconds(self) -> None:
        path = self.tmpdir / "a.o"
        path.write_bytes(b"obj")
        ns = 1_700_000_000 * NS_PER_SEC + 123_456_789
        os.utime(path, ns=(ns, ns))
        touched = truncate_file_mtimes(self.tmpdir)
        self.assertEqual(touched, 1)
        self.assertEqual(path.stat().st_mtime_ns % NS_PER_SEC, 0)

    def test_truncate_ninja_deps_mtime_to_whole_seconds(self) -> None:
        deps_path = self.tmpdir / ".ninja_deps"
        deps_path.write_bytes(sample_deps_log_v4(1_700_000_000 * NS_PER_SEC + 42))
        rewritten = truncate_ninja_deps(deps_path)
        self.assertEqual(rewritten, 1)
        version, offsets = parse_ninja_deps(deps_path.read_bytes())
        self.assertEqual(version, 4)
        (mtime_ns,) = struct.unpack_from("<q", deps_path.read_bytes(), offsets[0] + 4)
        self.assertEqual(mtime_ns, 1_700_000_000 * NS_PER_SEC)

    def test_truncate_ninja_deps_version_3_is_noop(self) -> None:
        deps_path = self.tmpdir / ".ninja_deps"
        deps_path.write_bytes(
            b"# ninjadeps\n"
            + struct.pack("<I", 3)
            + node_record(b"a.o", 0)
            + deps_record_v3(0, 12345, [])
        )
        self.assertEqual(truncate_ninja_deps(deps_path), 0)

    def test_truncate_ninja_deps_rejects_corrupt_log(self) -> None:
        deps_path = self.tmpdir / ".ninja_deps"
        deps_path.write_bytes(sample_deps_log_v4(0)[:-4])
        with self.assertRaises(NinjaDepsError):
            truncate_ninja_deps(deps_path)


class ValidateBuildCacheTests(unittest.TestCase):
    """Build cache validator accept/reject conditions."""

    def setUp(self) -> None:
        self.tmpdir = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmpdir)
        self.build_root = self.tmpdir / "build"
        # x86_64 / CPython 3.13 layout must be accepted (no hardcoded arch).
        self.ninja_dir = self.build_root / "temp.linux-x86_64-cpython-313"
        self.ninja_dir.mkdir(parents=True)

    def populate_valid_cache(self) -> None:
        """Create a minimal valid ninja build tree in ``self.ninja_dir``."""
        (self.ninja_dir / "build.ninja").write_text("rule cc\n")
        (self.ninja_dir / "kernel.o").write_bytes(b"obj")
        (self.ninja_dir / ".ninja_deps").write_bytes(sample_deps_log_v4(0))

    def test_accepts_valid_cache(self) -> None:
        self.populate_valid_cache()
        self.assertEqual(validate_build_cache(self.build_root), [])

    def test_rejects_missing_build_root(self) -> None:
        problems = validate_build_cache(self.tmpdir / "nope")
        self.assertEqual(len(problems), 1)

    def test_rejects_cache_without_objects(self) -> None:
        (self.ninja_dir / "build.ninja").write_text("rule cc\n")
        problems = validate_build_cache(self.build_root)
        self.assertTrue(any(".o/.obj" in p for p in problems))

    def test_rejects_cache_without_build_ninja(self) -> None:
        (self.ninja_dir / "kernel.o").write_bytes(b"obj")
        problems = validate_build_cache(self.build_root)
        self.assertTrue(any("build.ninja" in p for p in problems))

    def test_rejects_cache_with_corrupt_ninja_deps(self) -> None:
        self.populate_valid_cache()
        (self.ninja_dir / ".ninja_deps").write_bytes(sample_deps_log_v4(0)[:-4])
        problems = validate_build_cache(self.build_root)
        self.assertTrue(any(".ninja_deps" in p for p in problems))

    def test_accepts_windows_style_obj_objects(self) -> None:
        (self.ninja_dir / "build.ninja").write_text("rule cc\n")
        (self.ninja_dir / "kernel.obj").write_bytes(b"obj")
        self.assertEqual(validate_build_cache(self.build_root), [])


@unittest.skipUnless(
    shutil.which("ninja") and shutil.which("cc"),
    "requires ninja and a C compiler",
)
class RealNinjaLogTests(unittest.TestCase):
    """The strict parser must accept deps logs produced by a real ninja."""

    def test_parses_and_truncates_real_ninja_deps(self) -> None:
        tmpdir = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmpdir)
        (tmpdir / "foo.h").write_text("#define FOO 1\n")
        (tmpdir / "main.c").write_text(
            '#include "foo.h"\nint main(void){return FOO-1;}\n'
        )
        (tmpdir / "build.ninja").write_text(
            "rule cc\n"
            "  command = cc -MD -MF $out.d -c $in -o $out\n"
            "  depfile = $out.d\n"
            "  deps = gcc\n"
            "build main.o: cc main.c\n"
        )
        subprocess.run(
            ["ninja"], cwd=tmpdir, check=True, capture_output=True, text=True
        )
        deps_path = tmpdir / ".ninja_deps"
        self.assertTrue(deps_path.exists())
        version, offsets = parse_ninja_deps(deps_path.read_bytes())
        self.assertIn(version, (3, 4))
        self.assertGreaterEqual(len(offsets), 1)
        truncate_ninja_deps(deps_path)
        self.assertEqual(validate_build_cache(tmpdir), [])


if __name__ == "__main__":
    unittest.main()

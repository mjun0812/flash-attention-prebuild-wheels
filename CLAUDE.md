# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Pre-built Python wheel distribution for Flash Attention (v2/v3) across multiple platforms (Linux x86_64, Linux ARM64, Windows). Uses GitHub Actions matrix builds to cover many combinations of PyTorch, CUDA, and Python versions.

## Architecture

### Build Flow

1. **`create_matrix.py`** — Generates JSON matrices of all build combinations (flash-attn, python, torch, cuda versions). Each platform matrix can be individually toggled `False` in `main()` to skip; the combined `exclude` list is `EXCLUDE` from `scripts/coverage_matrix.py` plus optional inline excludes for already-released cells.
2. **`build_linux.sh` / `build_windows.ps1`** — Builds a wheel for one combination (args: `<flash-attn-version> <python-version> <torch-version> <cuda-version>`). FA3 paths overlay `patches/fa3/setup_linux.py` (Linux) or `patches/fa3/setup_windows.py` (Windows) onto the upstream clone before invoking `python setup.py bdist_wheel`.
3. **`.github/actions/build-and-upload/action.yml`** — Composite action: restore build cache → build → test (`import flash_attn`) → upload → `auditwheel repair` → manylinux test & upload. Cap + cache save logic gated by the `use-build-cache` input.

### CI/CD Workflow Structure

- **`build.yml`** — Main workflow. Triggered by `v*` tag push. Creates release → generates matrix → parallel builds (7 job types) → updates release notes & docs.
- **`test-build.yml`** — Manual `workflow_dispatch` for individual platform test builds. Forces `is-upload: false`.
- **`_build_*.yml`** — Reusable workflows per runner type (Linux hosted/self-hosted/no-container, Windows hosted/self-hosted/CodeBuild, Linux ARM hosted/self-hosted/no-container).

### GitHub-hosted Linux Resumable Build Cache (retry mechanism)

`use-build-cache: true` (set in `build.yml` for `build_wheels_linux` and `build_wheels_linux_arm64`) enables, for FA2 and FA3 on both x86_64 and ARM64:

- A build cap measured from job start (`BUILD_JOB_STARTED_AT`, default `build-timeout-minutes: 330` of the job's `timeout-minutes: 360`) so setup time counts toward GitHub's hard 6h job cancel and ~30m remain to validate/compress/upload the cache.
- `actions/cache@v4` save+restore of `~/.fa-build-cache/` (ninja build dir only; cutlass is re-initialized as a real submodule on restore because a cached copy carries a `.git` pointer into the previous runner's gitdir, breaking FA2's `check=True` submodule update in setup.py) under the `fabuild-v4-` prefix. The key includes a toolchain/script fingerprint plus `github.run_id`, so caches are only shared between rerun attempts of the same workflow run; each attempt saves its own immutable key.
- Save only happens when the build exits with code 124 (capped by `timeout`); completed builds and compile errors never save. Before saving, `scripts/tools/validate_build_cache.py` checks the build tree (build.ninja present, objects present, every `.ninja_deps` structurally valid) and `scripts/tools/truncate_build_cache_mtimes.py` rewrites every mtime (and the int64 mtime in version-4 `.ninja_deps`) to whole seconds so they survive GNU tar's ustar precision loss. Either failing skips the save.
- On restore, `build_linux.sh` validates the cache, moves it to the variant's build root (`flash-attention/build` for FA2, `flash-attention/hopper/build` for FA3), runs `git submodule update --init csrc/cutlass`, pushes every non-cached input (FA sources incl. cutlass, `.venv`'s torch include, `${CUDA_HOME}/include`) to `1970-01-02`, then discovers every `build.ninja` dynamically (no hardcoded `temp.linux-*` dir) and runs `ninja -t deps` + `ninja -t restat` so the restored `.o` tree stays "newer than its inputs" from ninja's perspective. Any verification failure falls back to a clean build.

Typical run-to-completion: attempt 1 caps and saves cache → `gh run rerun <run_id> --failed` triggers attempt 2 which restores the cache, ninja skips most completed compilations, and the build finishes within the cap. See `memory/project_build_cache_ninja_mtime.md` for the full debug trail. Tools are unit-tested in `tests/test_build_cache_tools.py` (run via `.github/workflows/test-build-cache-tools.yml`).

### Scripts (`scripts/`)

- **`common.py`** — Shared utilities (wheel filename parsing, version extraction).
- **`coverage_matrix.py`** — Single source of truth for `TORCH_SUPPORT_CUDA_VERSIONS`, `TORCH_SUPPORT_PYTHON_VERSIONS`, `EXCLUDE` (incompatible torch×cuda / torch×python combinations and FA3 free-threaded exclusions).
- **`release/`** — Generates Markdown for release notes, release history, and package lists.
- **`maintenance/update_readme_coverage.py`** — Updates coverage badges and tables in README.
- **`tools/check_missing_packages.py`** — Prints per-platform coverage tables (✓/✗/-) by hitting the GitHub Releases API.
- **`tools/truncate_build_cache_mtimes.py`** — Stand-alone mtime truncator + strict `.ninja_deps` parser used by the cache save step.
- **`tools/validate_build_cache.py`** — Validates a cached ninja build tree before cache save / after restore.
- **`tools/fetch_all_assets.py`** — Bulk asset retrieval.

### FA3 patches (`patches/fa3/`)

- `setup_linux.py` — plain copy of the pinned upstream `hopper/setup.py` with only `--resource-usage` commented out; fully replaces (not patches) the upstream file in `build_linux.sh`.
- `setup_windows.py` — same, but based on the unmerged upstream PR Dao-AILab/flash-attention#2047 (Windows linker 32KB command-line limit workaround via Ninja response files); used by `build_windows.ps1`.
- `cuda_h_alignment_fix.patch` / `cutlass_alignment_fix.patch` are kept for reference; current build flow does not apply them — overlay the patched setup instead.

### Version Detection

- FA2: Plain version strings like `"2.6.3"`, `"2.7.4"`, `"2.8.3"`.
- FA3: Distinguished by `"fa3:<commit-hash>"` prefix. FA3 wheels are abi3 (`cp39-abi3`) — one build covers all non-FT pythons.

### Wheel Naming Convention

```text
flash_attn-{version}+cu{cuda}torch{pytorch}-cp{python}-cp{python}-{platform}.whl
```

## Common Commands

```bash
# Generate / inspect the build matrix locally
uv run --python 3.14 --script create_matrix.py | python3 -m json.tool

# Linux build (requires CUDA environment)
./build_linux.sh <flash-attn-version> <python-version> <torch-version> <cuda-version>

# Release & doc generation (project root)
python -m scripts.release.create_release_note
python -m scripts.release.create_packages
python -m scripts.maintenance.update_readme_coverage

# Coverage check (needs requests + rich + pandas)
uv run --with requests --with rich --with pandas -m scripts.tools.check_missing_packages

# Format and lint
uvx ruff format
uvx ruff check --fix

# Retry a GitHub-hosted Linux build after the timeout cap saved its cache
gh run rerun <run_id> --failed

# Build cache tool tests
python3 -m unittest discover -v
```

## Key Conventions

- Adding a new version requires updating both `create_matrix.py` (matrix definitions) **and** `scripts/coverage_matrix.py` (`TORCH_SUPPORT_*` tables + `EXCLUDE` rules).
- Build resources (`MAX_JOBS`, `NVCC_THREADS`) are auto-calculated from CPU/RAM in `build_linux.sh`.
- FA3 builds replace the upstream `hopper/setup.py` with `patches/fa3/setup_linux.py` / `setup_windows.py` (full file copy, not a patch).
- Cache key prefix is `fabuild-v4-`; bumping the layout (added/removed paths under `~/.fa-build-cache/`) requires a new prefix to avoid restoring incompatible caches.
- `LINUX_ARM64_MATRIX` is frequently scoped down to a single combination for tag releases — restore the broader matrix (or leave a `_ALREADY_RELEASED` exclude list) when finished to make `check_missing_packages` work correctly.

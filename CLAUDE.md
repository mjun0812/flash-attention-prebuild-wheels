# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Pre-built Python wheel distribution for Flash Attention (v2/v3) across multiple platforms (Linux x86_64, Linux ARM64, Windows). Uses GitHub Actions matrix builds to cover many combinations of PyTorch, CUDA, and Python versions.

## Architecture

### Build Flow

1. **`create_matrix.py`** — Generates JSON matrices of all build combinations (flash-attn, python, torch, cuda versions). Each platform matrix can be individually toggled `False` in `main()` to skip; the combined `exclude` list is `EXCLUDE` from `scripts/coverage_matrix.py` plus optional inline excludes for already-released cells.
2. **`build_linux.sh` / `build_windows.ps1`** — Builds a wheel for one combination (args: `<flash-attn-version> <python-version> <torch-version> <cuda-version>`). FA3 paths overlay `patches/fa3/setup.py` onto the upstream clone before invoking `python setup.py bdist_wheel`.
3. **`.github/actions/build-and-upload/action.yml`** — Composite action: restore build cache → build → test (`import flash_attn`) → upload → `auditwheel repair` → manylinux test & upload. Cap + cache save logic gated by the `use-build-cache` input.

### CI/CD Workflow Structure

- **`build.yml`** — Main workflow. Triggered by `v*` tag push. Creates release → generates matrix → parallel builds (7 job types) → updates release notes & docs.
- **`test-build.yml`** — Manual `workflow_dispatch` for individual platform test builds. Forces `is-upload: false`.
- **`_build_*.yml`** — Reusable workflows per runner type (Linux hosted/self-hosted/no-container, Windows hosted/self-hosted/CodeBuild, Linux ARM hosted/self-hosted/no-container).

### ARM64 GitHub-hosted Build Cache (FA3 retry mechanism)

`use-build-cache: true` (set in `build.yml` line 81 for `build_wheels_linux_arm64`) enables:

- A 5h45m `timeout --signal=TERM 345m` cap so the build stops before GitHub's hard 6h cancel.
- `actions/cache@v4` save+restore of `~/.fa-build-cache/` (build dir + `flash-attention/csrc/cutlass`) under the `fabuild3-` prefix.
- On save, `scripts/tools/truncate_build_cache_mtimes.py` rewrites every mtime (and the int64 mtime in `.ninja_deps`) to whole seconds so they survive GNU tar's ustar precision loss.
- On restore, `build_linux.sh` pushes every non-cached input (FA3 sources, `.venv`'s torch include, `/usr/local/cuda/include`) to `1970-01-02` then runs `ninja -t restat` so the restored `.o` tree stays "newer than its inputs" from ninja's perspective.

Typical run-to-completion: attempt 1 caps at 5h45m and saves cache → `gh run rerun <run_id> --failed` triggers attempt 2 which restores the cache, ninja skips ~80% of compilations, and the build completes in ~1.5h. See `memory/project_build_cache_ninja_mtime.md` for the full debug trail.

### Scripts (`scripts/`)

- **`common.py`** — Shared utilities (wheel filename parsing, version extraction).
- **`coverage_matrix.py`** — Single source of truth for `TORCH_SUPPORT_CUDA_VERSIONS`, `TORCH_SUPPORT_PYTHON_VERSIONS`, `EXCLUDE` (incompatible torch×cuda / torch×python combinations and FA3 free-threaded exclusions).
- **`release/`** — Generates Markdown for release notes, release history, and package lists.
- **`maintenance/update_readme_coverage.py`** — Updates coverage badges and tables in README.
- **`tools/check_missing_packages.py`** — Prints per-platform coverage tables (✓/✗/-) by hitting the GitHub Releases API.
- **`tools/truncate_build_cache_mtimes.py`** — Stand-alone mtime truncator used by the cache save step.
- **`tools/fetch_all_assets.py`** — Bulk asset retrieval.

### FA3 patches (`patches/fa3/`)

- `setup.py` is fully replaced (not patched) by `build_linux.sh` to suppress verbose `--resource-usage` ptxas logs.
- `cuda_h_alignment_fix.patch` / `cutlass_alignment_fix.patch` are kept for reference; current build flow does not apply them — overlay the patched `setup.py` instead.

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

# Retry an ARM64 FA3 build after the 5h45m cap saved its cache
gh run rerun <run_id> --failed
```

## Key Conventions

- Adding a new version requires updating both `create_matrix.py` (matrix definitions) **and** `scripts/coverage_matrix.py` (`TORCH_SUPPORT_*` tables + `EXCLUDE` rules).
- Build resources (`MAX_JOBS`, `NVCC_THREADS`) are auto-calculated from CPU/RAM in `build_linux.sh`.
- FA3 builds replace the upstream `hopper/setup.py` with `patches/fa3/setup.py` (full file copy, not a patch).
- Cache key prefix is `fabuild3-`; bumping the layout (added/removed paths under `~/.fa-build-cache/`) requires a new prefix to avoid restoring incompatible caches.
- `LINUX_ARM64_MATRIX` is frequently scoped down to a single combination for tag releases — restore the broader matrix (or leave a `_ALREADY_RELEASED` exclude list) when finished to make `check_missing_packages` work correctly.

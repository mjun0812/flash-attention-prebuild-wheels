# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Pre-built Python wheel distribution for Flash Attention (v2/v3) across multiple platforms (Linux x86_64, Linux ARM64, Windows), plus ROCm (AMD GPU) wheels for Linux x86_64. Uses GitHub Actions matrix builds to cover many combinations of PyTorch, CUDA / ROCm, and Python versions.

## Architecture

### Build Flow

1. **`create_matrix.py`** — Generates JSON matrices of all build combinations (flash-attn, python, torch, cuda versions). Each platform matrix can be individually toggled `False` in `main()` to skip; the combined `exclude` list is `EXCLUDE` from `scripts/coverage_matrix.py` plus optional inline excludes for already-released cells.
2. **`build_linux.sh` / `build_windows.ps1`** — Builds a wheel for one combination (args: `<flash-attn-version> <python-version> <torch-version> <cuda-version>`). FA3 paths overlay `patches/fa3/setup_linux.py` (Linux) or `patches/fa3/setup_windows.py` (Windows) onto the upstream clone before invoking `python setup.py bdist_wheel`.
   - **`build_linux_rocm.sh`** — ROCm counterpart (args: `... <rocm-version>`), FA2 only. Installs torch from `download.pytorch.org/whl/rocm<ver>`, sets `BUILD_TARGET=rocm` and `GPU_ARCHS` (default `gfx90a;gfx942;gfx950`, all in one wheel; `create_matrix.py`'s `LINUX_ROCM_MATRIX["gpu-archs"]` overrides it for release builds and must match the pinned version's `allowed_archs`), and labels the wheel `rocm<ver>torch<major.minor>`. Shares no code with `build_linux.sh`; `MAX_JOBS` is the only parallelism knob (upstream's ROCm branch ignores `NVCC_THREADS`). When `ccache` is installed it sets `PYTORCH_NVCC="ccache <hipcc>"` (the hook PyTorch documents for this) so every hipcc call is content-addressed, with `CCACHE_DIR=~/.cache/ccache-rocm`, `CCACHE_MAXSIZE=20G` and `CCACHE_COMPILERCHECK=content` (the CI runner reinstalls ROCm each job, changing hipcc's mtime); any of those set by the caller wins, and a missing `ccache` only costs the caching. A ninja build-directory cache like the CUDA path's cannot work here because upstream regenerates all ~7.6k kernel sources on every run and the ROCm compile lines carry no depfiles.
3. **`.github/actions/build-and-upload/action.yml`** — Composite action: restore build cache → build → test (`import flash_attn`) → upload → `auditwheel repair` → manylinux test & upload. Cap + cache save logic gated by the `use-build-cache` input.

### CI/CD Workflow Structure

- **`build.yml`** — Main workflow. Triggered by `v*` tag push. Creates release → generates matrix → parallel builds (7 job types) → updates release notes & docs.
- **`test-build.yml`** — Manual `workflow_dispatch` for individual platform test builds. Forces `is-upload: false`.
- **`_build_*.yml`** — Reusable workflows per runner type (Linux hosted/self-hosted/no-container, Windows hosted/self-hosted/CodeBuild, Linux ARM hosted/self-hosted/no-container, Linux ROCm self-hosted/no-container via `mjun0812/setup-rocm`). `_build_linux_rocm.yml` also logs build-time and disk measurements and uploads the wheel as a job artifact. With three GPU targets one cell takes ~2h50m on the 32-thread self-hosted runner and ~7h20m on the 16-thread one; with ten targets, ~9h05m and ~25h10m. Because a job's `GITHUB_TOKEN` expires 24h after the job starts, `_build_linux_rocm.yml` caps the build at `build-timeout-minutes` (default 1200) measured from job start and exits 124; re-running the job then resumes from ccache. The cache is carried by `actions/cache` under a `fa-rocm-ccache-` key that pins the cell plus `github.run_id` (saved only on a capped build, restored by prefix without the attempt suffix), because the two self-hosted runners share one label and a re-run lands on either of them; `CCACHE_DIR` therefore points into `RUNNER_TEMP` and cleanup deletes it with the pip and uv caches. Measured on a three-target cell: cached objects replay at ~176 TU/min against ~19 TU/min for real compiles, and the whole cache is ~140 MB per 1816 objects.

### GitHub-hosted Resumable Build Cache (retry mechanism)

`use-build-cache: true` (set in `build.yml` for `build_wheels_linux`, `build_wheels_linux_arm64`, and `build_wheels_windows`) enables, for FA2 and FA3:

- A build cap measured from job start (`BUILD_JOB_STARTED_AT`, default `build-timeout-minutes: 330` of the job's `timeout-minutes: 360`) so setup time counts toward GitHub's hard 6h job cancel and ~30m remain to validate/compress/upload the cache.
- `actions/cache@v4` save+restore of `~/.fa-build-cache/` (ninja build dir only; cutlass is re-initialized as a real submodule on restore because a cached copy carries a `.git` pointer into the previous runner's gitdir, breaking FA2's `check=True` submodule update in setup.py) under the `fa-build-cache-` prefix. The key includes a toolchain/script fingerprint plus `github.run_id`, so caches are only shared between rerun attempts of the same workflow run; each attempt saves its own immutable key.
- Save only happens when the build exits with code 124 (capped by `timeout`); completed builds and compile errors never save. Before saving, `scripts/tools/validate_build_cache.py` checks the build tree (build.ninja present, objects present, every `.ninja_deps` structurally valid) and `scripts/tools/truncate_build_cache_mtimes.py` rewrites every mtime (and the int64 mtime in version-4 `.ninja_deps`) to whole seconds so they survive GNU tar's ustar precision loss. Either failing skips the save.
- On restore, the cache is validated, moved to the variant's build root (`flash-attention/build` for FA2, `flash-attention/hopper/build` for FA3), cutlass is re-initialized via `git submodule update --init csrc/cutlass`, every non-cached input (FA sources incl. cutlass, `.venv`'s torch include, `${CUDA_HOME}/include`) is pushed to `1970-01-02`, then every `build.ninja` is discovered dynamically (no hardcoded `temp.*` dir) and `ninja -t deps` + `ninja -t restat` run so the restored object tree stays "newer than its inputs" from ninja's perspective. Any verification failure falls back to a clean build. Linux implements this inline in `build_linux.sh`; Windows calls `scripts/tools/restore_build_cache.py` from `build_windows.ps1` (mtime rewinds over ~70k files are too slow in PowerShell).
- Windows has no `timeout(1)`, so `_build_windows.yml` wraps `build_windows.ps1` in `scripts/tools/run_with_timeout.py`, which stops the whole process tree on expiry (CTRL_BREAK_EVENT → grace period → `taskkill /T /F`) and exits 124 like coreutils timeout.

Typical run-to-completion: attempt 1 caps and saves cache → `gh run rerun <run_id> --failed` triggers attempt 2 which restores the cache, ninja skips most completed compilations, and the build finishes within the cap. See `memory/project_build_cache_ninja_mtime.md` for the full debug trail.

### Scripts (`scripts/`)

- **`common.py`** — Shared utilities (wheel filename parsing, version extraction).
- **`coverage_matrix.py`** — Single source of truth for `TORCH_SUPPORT_CUDA_VERSIONS`, `TORCH_SUPPORT_ROCM_VERSIONS`, `TORCH_SUPPORT_PYTHON_VERSIONS`, `EXCLUDE` (CUDA jobs: incompatible torch×cuda / torch×python combinations and FA3 free-threaded exclusions) and `EXCLUDE_ROCM` (the ROCm job: torch×rocm plus the shared entries). ROCm matrices use a `rocm-version` axis instead of `cuda-version`; the coverage key is `linux_rocm`. `TORCH_SUPPORT_ROCM_VERSIONS` mirrors what `download.pytorch.org/whl/rocm*/torch/` actually ships, oldest first (torch 2.10 → 7.0/7.1, 2.11–2.13 → 7.1/7.2, 2.14 → 7.2/7.14); verify against those indexes before changing it. Only the first entry of each tuple is built: one wheel serves every ROCm minor of that torch release (measured — see ADR 0005), and the oldest is chosen because only forward compatibility was tested. ROCm publishes no free-threaded torch, so `LINUX_ROCM_MATRIX` takes `PYTHON_VERSIONS`, not `ALL_PYTHON_VERSIONS`.
- **`release/`** — Generates Markdown for release notes, release history, and package lists.
- **`maintenance/update_readme_coverage.py`** — Updates coverage badges and tables in README.
- **`tools/check_missing_packages.py`** — Prints per-platform coverage tables (✓/✗/-) by hitting the GitHub Releases API.
- **`tools/truncate_build_cache_mtimes.py`** — Stand-alone mtime truncator + strict `.ninja_deps` parser used by the cache save step.
- **`tools/validate_build_cache.py`** — Validates a cached ninja build tree before cache save / after restore.
- **`tools/restore_build_cache.py`** — Restores the cached build tree into a fresh clone (validate → move → cutlass init → mtime rewind → ninja restat); used by `build_windows.ps1`.
- **`tools/run_with_timeout.py`** — Windows-aware `timeout(1)` equivalent (process-tree stop, exit 124); used by `_build_windows.yml`.
- **`tools/fetch_all_assets.py`** — Bulk asset retrieval.

### FA3 patches (`patches/fa3/`)

- `setup_linux.py` — plain copy of the pinned upstream `hopper/setup.py` with only `--resource-usage` commented out; fully replaces (not patches) the upstream file in `build_linux.sh`.
- `setup_windows.py` — same, but based on the unmerged upstream PR Dao-AILab/flash-attention#2047 (Windows linker 32KB command-line limit workaround via Ninja response files); used by `build_windows.ps1`.
- `cuda_h_alignment_fix.patch` / `cutlass_alignment_fix.patch` are kept for reference; current build flow does not apply them — overlay the patched setup instead.

### Version Detection

- FA2: Plain version strings like `"2.6.3"`, `"2.7.4"`, `"2.8.3"` (release tags), or `"fa2:<commit-hash>"` to pin an upstream commit (e.g. main for changes not yet released). Commit-pinned FA2 wheels get a `git<short-hash>` local version suffix like FA3 and are otherwise ordinary per-Python FA2 wheels; the coverage tooling keys them as `fa2:<short-hash>`.
- FA3: Distinguished by `"fa3:<commit-hash>"` prefix. FA3 wheels are abi3 (`cp39-abi3`) — one build covers all non-FT pythons.

### Wheel Naming Convention

```text
flash_attn-{version}+cu{cuda}torch{pytorch}-cp{python}-cp{python}-{platform}.whl
flash_attn-{version}+rocm{rocm}torch{pytorch}-cp{python}-cp{python}-linux_x86_64.whl   # ROCm; keeps the dot (rocm7.2), see ADR 0002
```

`scripts/common.parse_wheel_filename` returns `accelerator` (`cuda` / `rocm`) and `accelerator_version`; ROCm wheels are shown as the separate platform "Linux x86_64 (ROCm)".

## Common Commands

```bash
# Generate / inspect the build matrix locally
uv run --python 3.14 --script create_matrix.py | python3 -m json.tool

# Linux build (requires CUDA environment)
./build_linux.sh <flash-attn-version> <python-version> <torch-version> <cuda-version>

# Linux ROCm build (requires hipcc on PATH; mjun0812/setup-rocm in CI)
./build_linux_rocm.sh <flash-attn-version> <python-version> <torch-version> <rocm-version>

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
```

## Key Conventions

- Adding a new version requires updating both `create_matrix.py` (matrix definitions) **and** `scripts/coverage_matrix.py` (`TORCH_SUPPORT_*` tables + `EXCLUDE` rules). For ROCm, `LINUX_ROCM_MATRIX` in both files and `TORCH_SUPPORT_ROCM_VERSIONS`; `linux_rocm` in `create_matrix.main()` is toggled per release like the other platforms. `LINUX_ROCM_MATRIX["gpu-archs"]` (create_matrix.py only) is a scalar, not an axis: every cell of the ROCm job bundles that same target set into one wheel.
- Build resources (`MAX_JOBS`, `NVCC_THREADS`) are auto-calculated from CPU/RAM in `build_linux.sh`.
- FA3 builds replace the upstream `hopper/setup.py` with `patches/fa3/setup_linux.py` / `setup_windows.py` (full file copy, not a patch).
- Cache key prefix is `fa-build-cache-`; the toolchain/script fingerprint in the key already prevents restoring incompatible caches on a layout change (added/removed paths under `~/.fa-build-cache/`).
- `LINUX_ARM64_MATRIX` is frequently scoped down to a single combination for tag releases — restore the broader matrix (or leave a `_ALREADY_RELEASED` exclude list) when finished to make `check_missing_packages` work correctly.

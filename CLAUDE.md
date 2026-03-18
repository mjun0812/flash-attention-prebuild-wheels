# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Pre-built Python wheel distribution for Flash Attention (v2/v3) across multiple platforms (Linux x86_64, Linux ARM64, Windows). Uses GitHub Actions matrix builds to cover many combinations of PyTorch, CUDA, and Python versions.

## Architecture

### Build Flow

1. **`create_matrix.py`** — Generates JSON matrices of all build combinations (flash-attn, python, torch, cuda versions)
2. **`build_linux.sh` / `build_windows.ps1`** — Builds a wheel for a given combination (args: `<flash-attn-version> <python-version> <torch-version> <cuda-version>`)
3. **`.github/actions/build-and-upload/action.yml`** — Composite action: build → test (`import flash_attn`) → upload → `auditwheel repair` → manylinux test & upload

### CI/CD Workflow Structure

- **`build.yml`** — Main workflow. Triggered by `v*` tag push. Creates release → generates matrix → parallel builds (7 job types) → updates release notes & docs
- **`test-build.yml`** — Manual trigger for test builds. Each platform selectable individually. Uses `is-upload: false`
- **`_build_*.yml`** — Reusable workflows per platform (Linux, Windows, Self-hosted, CodeBuild)

### Scripts (`scripts/`)

- **`common.py`** — Shared utilities (wheel filename parsing, version extraction)
- **`coverage_matrix.py`** — Defines supported version mappings (PyTorch↔CUDA, PyTorch↔Python) and exclusion rules
- **`release/`** — Generates Markdown for release notes, release history, and package lists
- **`maintenance/update_readme_coverage.py`** — Updates coverage badges and tables in README
- **`tools/`** — Missing package checks, asset fetching

### Version Detection

- FA2: Plain version strings like `"2.6.3"`, `"2.7.4"`, `"2.8.3"`
- FA3: Distinguished by `"fa3:<commit-hash>"` prefix

### Wheel Naming Convention

```text
flash_attn-{version}+cu{cuda}torch{pytorch}-cp{python}-cp{python}-{platform}.whl
```

## Common Commands

```bash
# Generate build matrix
python create_matrix.py

# Linux build (requires CUDA environment)
./build_linux.sh <flash-attn-version> <python-version> <torch-version> <cuda-version>

# Generate release notes
python -m scripts.release.create_release_note

# Generate package list
python -m scripts.release.create_packages

# Update README coverage
python -m scripts.maintenance.update_readme_coverage

# Check missing packages
python -m scripts.tools.check_missing_packages

# Format and lint
uvx ruff format
uvx ruff check --fix
```

## Key Conventions

- Adding a new version requires updating both `create_matrix.py` (matrix definitions) and `scripts/coverage_matrix.py` (support definitions)
- Build resources (`MAX_JOBS`, `NVCC_THREADS`) are auto-calculated from CPU/RAM in `build_linux.sh`
- FA3 builds replace the upstream `setup.py` with `patches/fa3/setup.py`

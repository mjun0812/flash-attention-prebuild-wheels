# Scripts Reference

This document describes the scripts used in this repository, their organization, and how to run them.

## Directory Structure

```
flash-attention-prebuild-wheels/
├── build_linux.sh                              # Linux wheel build (workflow entry point)
├── build_windows.ps1                           # Windows wheel build (workflow entry point)
├── create_matrix.py                            # Build matrix generation (workflow entry point)
├── get_torch_cuda_version.py                   # CUDA version resolver (called by build scripts)
├── scripts/
│   ├── common.py                               # Shared utilities
│   ├── coverage_matrix.py                      # Coverage matrix & exclusion definitions
│   ├── release/                                # Release documentation generation
│   │   ├── create_release_note.py
│   │   ├── create_release_history.py
│   │   └── create_packages.py
│   ├── maintenance/                            # Scheduled maintenance tasks
│   │   ├── update_download_stats.py
│   │   └── update_readme_coverage.py
│   └── tools/                                  # Manual CLI tools
│       ├── check_missing_packages.py
│       └── fetch_all_assets.py
```

### Why Some Scripts Stay in the Root

`build_linux.sh`, `build_windows.ps1`, `create_matrix.py`, and `get_torch_cuda_version.py` remain in the repository root because they are direct entry points called by GitHub Actions workflows and build scripts. Keeping them in root avoids changes to workflow files and shell scripts that reference them by relative path (e.g., `./build_linux.sh`, `python create_matrix.py`).

### Category Overview

| Location | Purpose | Trigger |
|----------|---------|---------|
| Root | Wheel builds, matrix generation | Tag push via `build.yml` |
| `scripts/release/` | Release notes, history, package docs | Post-build step in `build.yml` |
| `scripts/maintenance/` | README updates, download statistics | Daily cron via `update-download-stats.yml` |
| `scripts/tools/` | Missing package checks, asset fetching | Manual execution |

## Running Scripts

Scripts under `scripts/` must be run as Python modules from the repository root:

```bash
python -m scripts.tools.check_missing_packages --help
python -m scripts.release.create_packages --help
```

Root-level scripts are run directly:

```bash
python create_matrix.py
./build_linux.sh 2.8.3 3.11 2.9.1 12.8
```

## Dependencies

Install required Python packages:

```bash
pip install pandas requests matplotlib rich
```

| Package | Used by |
|---------|---------|
| `pandas` | `scripts/common.py`, `scripts/release/create_packages.py` |
| `requests` | `scripts/maintenance/update_download_stats.py`, `scripts/tools/check_missing_packages.py`, `scripts/tools/fetch_all_assets.py` |
| `matplotlib` | `scripts/maintenance/update_download_stats.py` |
| `rich` | `scripts/tools/check_missing_packages.py` |

## Environment Variables

| Variable | Required | Used by |
|----------|----------|---------|
| `GITHUB_TOKEN` | Optional | `scripts/tools/check_missing_packages.py`, `scripts/tools/fetch_all_assets.py`, `scripts/maintenance/update_readme_coverage.py` |

When `GITHUB_TOKEN` is not set, scripts fall back to unauthenticated GitHub API access (lower rate limits).

---

## Root Scripts

### `build_linux.sh`

Builds Flash-Attention wheels for Linux. Called by GitHub Actions.

```bash
./build_linux.sh <FLASH_ATTN_VERSION> <PYTHON_VERSION> <TORCH_VERSION> <CUDA_VERSION>
```

Example:
```bash
./build_linux.sh 2.8.3 3.11 2.9.1 12.8
```

Automatically determines `MAX_JOBS` and `NVCC_THREADS` based on available CPU cores and RAM. Calls `get_torch_cuda_version.py` internally to resolve the correct PyTorch CUDA variant.

### `build_windows.ps1`

Builds Flash-Attention wheels for Windows. Called by GitHub Actions.

```powershell
.\build_windows.ps1 -FlashAttnVersion 2.8.3 -PythonVersion 3.11 -TorchVersion 2.9.1 -CudaVersion 12.8
```

Imports the Visual Studio DevShell and calls `get_torch_cuda_version.py` internally.

### `create_matrix.py`

Outputs the build matrix as JSON to stdout. Used by `build.yml` to generate the GitHub Actions strategy matrix.

```bash
python create_matrix.py
```

Platforms are enabled/disabled by commenting out lines in the script. The `EXCLUDE` list (incompatible version combinations) is imported from `scripts/coverage_matrix.py`.

### `get_torch_cuda_version.py`

Resolves the closest supported CUDA version for a given PyTorch version. Called internally by `build_linux.sh` and `build_windows.ps1`.

```bash
python get_torch_cuda_version.py <CUDA_VERSION_INT> <TORCH_MINOR_VERSION>
```

Example:
```bash
python get_torch_cuda_version.py 128 2.9
# Output: the closest supported CUDA version string
```

---

## Release Scripts (`scripts/release/`)

These scripts generate release documentation. They are called by `build.yml` after wheel builds complete.

### `create_release_note.py`

Generates a Markdown release note from a GitHub release assets JSON file.

```bash
python -m scripts.release.create_release_note /tmp/assets.json > release_notes.md
```

- **Input**: Path to `assets.json` (positional argument)
- **Output**: Markdown to stdout

### `create_release_history.py`

Updates `doc/release_history.md` with a new release entry.

```bash
python -m scripts.release.create_release_history \
  --assets /tmp/assets.json \
  --tag v2.8.3 \
  --repo mjun0812/flash-attention-prebuild-wheels \
  --output doc/release_history.md
```

| Argument | Required | Description |
|----------|----------|-------------|
| `--assets` | Yes | Path to assets.json |
| `--tag` | Yes | Release tag (e.g., `v2.8.3`) |
| `--repo` | Yes | Repository in `owner/name` format |
| `--output` | Yes | Path to the release history file to update |

### `create_packages.py`

Generates or updates `doc/packages.md` with a comprehensive package listing.

```bash
python -m scripts.release.create_packages --assets /tmp/assets.json --output doc/packages.md
```

| Argument | Default | Description |
|----------|---------|-------------|
| `--assets` | `assets.json` | Path to assets.json |
| `--output` | `doc/packages.md` | Output file path |

---

## Maintenance Scripts (`scripts/maintenance/`)

These scripts run on a daily schedule via `update-download-stats.yml`.

### `update_download_stats.py`

Fetches download counts from the GitHub API and updates `doc/data/download_history.json` and `doc/data/download_graph.png`.

```bash
python -m scripts.maintenance.update_download_stats
```

No arguments. Repository and file paths are configured within the script.

### `update_readme_coverage.py`

Calculates wheel coverage (available vs. expected packages) and updates badges and tables in `README.md`.

```bash
python -m scripts.maintenance.update_readme_coverage
python -m scripts.maintenance.update_readme_coverage --cache --cache-file assets.json
```

| Argument | Default | Description |
|----------|---------|-------------|
| `--repo` | `mjun0812/flash-attention-prebuild-wheels` | GitHub repository |
| `--cache` | `false` | Use a local assets.json instead of fetching from GitHub |
| `--cache-file` | `assets.json` | Path to cached assets file |
| `--readme` | `README.md` | Path to README to update |

Updates content between `<!-- COVERAGE_BADGE_START/END -->` and `<!-- COVERAGE_TABLE_START/END -->` markers in the README.

---

## Tool Scripts (`scripts/tools/`)

These are manual CLI tools for development and debugging.

### `check_missing_packages.py`

Compares published wheels against the expected coverage matrix and displays a colored table of results.

```bash
python -m scripts.tools.check_missing_packages
python -m scripts.tools.check_missing_packages --cache --platform linux --flash-version 2.8.3
python -m scripts.tools.check_missing_packages --show-missing-only --list-missing
```

| Argument | Default | Description |
|----------|---------|-------------|
| `--repo` | `mjun0812/flash-attention-prebuild-wheels` | GitHub repository |
| `--cache` | `false` | Use local assets.json |
| `--cache-file` | `assets.json` | Path to cached assets file |
| `--platform` | `all` | Filter by platform: `linux`, `linux_arm64`, `windows`, or `all` |
| `--flash-version` | (none) | Filter by specific flash-attn version |
| `--show-missing-only` | `false` | Only show tables with missing packages |
| `--list-missing` | `false` | Print a summary list of all missing packages |

### `fetch_all_assets.py`

Fetches all release assets from GitHub and saves them as a JSON file.

```bash
python -m scripts.tools.fetch_all_assets
python -m scripts.tools.fetch_all_assets --repo mjun0812/flash-attention-prebuild-wheels --output assets.json
```

| Argument | Default | Description |
|----------|---------|-------------|
| `--repo` | `mjun0812/flash-attention-prebuild-wheels` | GitHub repository |
| `--output` | `assets.json` | Output file path |

---

## Shared Modules

### `scripts/common.py`

Shared utility functions used by release and tool scripts.

| Function | Description |
|----------|-------------|
| `load_assets_json(path)` | Load and return the asset list from an assets.json file |
| `parse_wheel_filename(filename)` | Parse a wheel filename into a dict of version components |
| `normalize_platform_name(raw)` | Normalize platform strings for display |
| `parse_numeric_version(text)` | Convert a version string to a numeric tuple for sorting |
| `normalize_semantic_version(version)` | Strip patch version, returning `major.minor` only |
| `get_tag_from_url(url)` | Extract the release tag from a GitHub download URL |
| `get_os_emoji(os_name)` | Return an emoji for the given OS name |
| `collect_versions_from_assets(assets)` | Aggregate assets by platform into version sets |
| `format_versions(values)` | Format a set of version strings as a sorted comma-separated string |

### `scripts/coverage_matrix.py`

Defines the expected wheel coverage matrices and exclusion rules.

| Symbol | Description |
|--------|-------------|
| `EXCLUDE` | List of incompatible version combinations (shared with `create_matrix.py`) |
| `LINUX_MATRIX` | Expected Linux x86_64 wheel matrix |
| `LINUX_ARM64_MATRIX` | Expected Linux ARM64 wheel matrix |
| `WINDOWS_MATRIX` | Expected Windows wheel matrix |

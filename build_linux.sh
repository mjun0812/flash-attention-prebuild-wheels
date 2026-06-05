#!/bin/bash

set -e

SCRIPT_DIR=$(dirname "$(realpath "$0")")

# Parameters with defaults
FLASH_ATTN_VERSION=$1
PYTHON_VERSION=$2
TORCH_VERSION=$3
CUDA_VERSION=$4

echo "Building Flash Attention with parameters:"
echo "  Flash-Attention: $FLASH_ATTN_VERSION"
echo "  Python: $PYTHON_VERSION"
echo "  PyTorch: $TORCH_VERSION"
echo "  CUDA: $CUDA_VERSION"

# Set CUDA and PyTorch versions
MATRIX_CUDA_VERSION=$(echo $CUDA_VERSION | awk -F \. {'print $1 $2'})
MATRIX_TORCH_VERSION=$(echo $TORCH_VERSION | awk -F \. {'print $1 "." $2'})

echo "Derived versions:"
echo "  CUDA Matrix: $MATRIX_CUDA_VERSION"
echo "  Torch Matrix: $MATRIX_TORCH_VERSION"

# Install PyTorch
TORCH_CUDA_VERSION=$(python get_torch_cuda_version.py $MATRIX_CUDA_VERSION $MATRIX_TORCH_VERSION)

echo "Installing PyTorch $TORCH_VERSION+cu$TORCH_CUDA_VERSION..."
if [[ $TORCH_VERSION == *"dev"* ]]; then
  pip install --force-reinstall --no-cache-dir --pre torch==$TORCH_VERSION --index-url https://download.pytorch.org/whl/nightly/cu${TORCH_CUDA_VERSION}
else
  pip install --force-reinstall --no-cache-dir torch==$TORCH_VERSION --index-url https://download.pytorch.org/whl/cu${TORCH_CUDA_VERSION}
fi

# Verify installation
echo "Verifying installations..."
nvcc --version
python -V
python -c "import torch; print('PyTorch:', torch.__version__)"
python -c "import torch; print('CUDA:', torch.version.cuda)"
python -c "from torch.utils import cpp_extension; print(cpp_extension.CUDA_HOME)"

# FlashAttention Variant handling
FLASH_ATTN_VARIANT=""
if [[ "$FLASH_ATTN_VERSION" == fa3:* ]]; then
  FLASH_ATTN_VARIANT="Flash Attention 3"
else
  FLASH_ATTN_VARIANT="Flash Attention 2"
fi
echo "Selected Flash Attention variant: $FLASH_ATTN_VARIANT"

# Checkout flash-attn
if [[ "$FLASH_ATTN_VARIANT" == "Flash Attention 3" ]]; then
  FA_COMMIT="${FLASH_ATTN_VERSION#fa3:}"
  echo "Building $FLASH_ATTN_VARIANT (commit: $FA_COMMIT)"
  git clone https://github.com/Dao-AILab/flash-attention.git flash-attention
  git -C flash-attention checkout "$FA_COMMIT"
  # Replace upstream hopper/setup.py with our patched version.
  # The patch suppresses --resource-usage ptxas logs and adds ccache support
  # for the bundled nvcc that FA3 downloads and injects via PYTORCH_NVCC.
  cp "$(dirname "$0")/patches/fa3/setup.py" flash-attention/hopper/setup.py
  # If a previous attempt's ninja build directory was cached by the CI step
  # (Restore FA3 build directory cache), move it into place so ninja sees
  # the existing .o files and skips already-compiled translation units.
  # Touch every file so ninja considers them newer than the freshly cloned
  # .cu sources (otherwise mtime would force recompilation).
  if [ -d "$HOME/.fa-build-cache/build" ]; then
    echo "fa-build-cache: restoring previous ninja build directory"
    du -sh "$HOME/.fa-build-cache/build" || true
    mkdir -p flash-attention/hopper
    rm -rf flash-attention/hopper/build
    mv "$HOME/.fa-build-cache/build" flash-attention/hopper/build
    find flash-attention/hopper/build -exec touch {} + 2>/dev/null || true
  fi
elif [[ "${FLASH_ATTN_VARIANT}" == "Flash Attention 2" ]]; then
  echo "Checking out flash-attention v${FLASH_ATTN_VERSION}..."
  git clone https://github.com/Dao-AILab/flash-attention.git flash-attention -b "v$FLASH_ATTN_VERSION"
  # Remove FA4 (flash_attn/cute) to prevent it from being included in the FA2 wheel
  rm -rf flash-attention/flash_attn/cute
else
  echo "Unknown Flash Attention variant: $FLASH_ATTN_VARIANT"
  exit 1
fi

# Determine MAX_JOBS and NVCC_THREADS based on system resources
NUM_THREADS=$(nproc)
RAM_GB=$(free -g | awk '/^Mem:/{print $2}')
echo "System resources:"
echo "  CPU threads: $NUM_THREADS"
echo "  RAM: ${RAM_GB}GB"
if [[ -z "${MAX_JOBS:-}" && -z "${NVCC_THREADS:-}" ]]; then
  # Calculate max product based on following constraints:
  # - MAX_JOBS x NVCC_THREADS(<= 4) <= NUM_THREADS
  # - 2.8GB x MAX_JOBS x NVCC_THREADS(<= 4) <= RAM_GB

  # Set MAX_PRODUCT from RAM
  MAX_PRODUCT_CPU=$NUM_THREADS
  MAX_PRODUCT_RAM=$(awk -v ram="$RAM_GB" 'BEGIN {print int(ram / 2.8)}')
  MAX_PRODUCT=$((MAX_PRODUCT_CPU < MAX_PRODUCT_RAM ? MAX_PRODUCT_CPU : MAX_PRODUCT_RAM))

  # Set MAX_JOBS and NVCC_THREADS so that MAX_JOBS x NVCC_THREADS ≈ MAX_PRODUCT with NVCC_THREADS <= 4
  BASE_THREADS=$(awk -v max="$MAX_PRODUCT" 'BEGIN {print int(sqrt(max))}')

  if awk "BEGIN {exit !($RAM_GB <= 16)}"; then
    # If RAM is less than 16GB, set NVCC_THREADS to 1 and MAX_JOBS to 2
    NVCC_THREADS=1
    MAX_JOBS=2
  elif (( BASE_THREADS <= 4 )); then
    NVCC_THREADS=$BASE_THREADS
    MAX_JOBS=$BASE_THREADS
  else
    NVCC_THREADS=4
    MAX_JOBS=$((MAX_PRODUCT / NVCC_THREADS))
  fi

  # Ensure minimum values of 1
  MAX_JOBS=$((MAX_JOBS < 1 ? 1 : MAX_JOBS))
  NVCC_THREADS=$((NVCC_THREADS < 1 ? 1 : NVCC_THREADS))
fi
echo "Build parallelism settings:"
echo "  MAX_JOBS: $MAX_JOBS"
echo "  NVCC_THREADS: $NVCC_THREADS"

# Optional ccache setup (enabled with USE_CCACHE=1).
# Speeds up rebuilds by caching compiled objects. Useful for retrying builds
# that hit the GitHub-hosted 6h limit: the second run reuses cached objects.
if [[ "${USE_CCACHE:-0}" == "1" ]]; then
  if command -v ccache >/dev/null 2>&1; then
    echo "ccache: enabled"
    export CCACHE_DIR="${CCACHE_DIR:-$HOME/.ccache}"
    export CCACHE_MAXSIZE="${CCACHE_MAXSIZE:-5G}"
    # Hash only file content, not mtime/path, so cache hits survive fresh clones.
    export CCACHE_COMPILERCHECK="${CCACHE_COMPILERCHECK:-content}"
    # Normalize absolute paths under the build tree to relative paths so cache
    # entries survive across GitHub-hosted runners (different VM hostnames,
    # paths, etc.). Without this, nvcc command lines embed absolute paths and
    # ccache treats every invocation as a miss.
    export CCACHE_BASEDIR="${CCACHE_BASEDIR:-$(pwd)}"
    export CCACHE_NOHASHDIR=1
    ccache -M "$CCACHE_MAXSIZE" >/dev/null 2>&1 || true

    # Host compiler (gcc/g++): use ccache's masquerade dir on PATH so that
    # tools resolving the compiler by name go through ccache.
    if [ -d /usr/lib/ccache ]; then
      export PATH="/usr/lib/ccache:$PATH"
    fi

    # nvcc: PyTorch's cpp_extension invokes $CUDA_HOME/bin/nvcc by absolute
    # path, so PATH masquerade does not apply. Replace nvcc with a wrapper that
    # routes through ccache. The real binary MUST stay in the same bin dir
    # (renamed nvcc.real), otherwise nvcc cannot locate its sibling tools
    # (cicc, ptxas, nvvm) by relative path and fails with "cicc: not found".
    NVCC_BIN=$(command -v nvcc || true)
    if [ -n "$NVCC_BIN" ]; then
      NVCC_DIR=$(dirname "$NVCC_BIN")
      if [ ! -f "$NVCC_DIR/nvcc.real" ]; then
        sudo mv "$NVCC_BIN" "$NVCC_DIR/nvcc.real"
        sudo tee "$NVCC_BIN" >/dev/null <<EOF
#!/usr/bin/env bash
exec ccache "$NVCC_DIR/nvcc.real" "\$@"
EOF
        sudo chmod +x "$NVCC_BIN"
        echo "ccache: wrapped nvcc (real at $NVCC_DIR/nvcc.real)"
      fi
      # The real binary's basename is "nvcc.real", so tell ccache explicitly
      # that this is the CUDA compiler (ccache >= 4.4 supports CCACHE_COMPILERTYPE).
      export CCACHE_COMPILERTYPE=nvcc
    fi
    ccache -z >/dev/null 2>&1 || true
  else
    echo "ccache: USE_CCACHE=1 but ccache not found on PATH; building without it"
  fi
fi

# Build wheels
echo "Building wheels..."
if [[ "$FLASH_ATTN_VARIANT" == "Flash Attention 3" ]]; then
  SHORT_HASH=$(git -C flash-attention rev-parse --short=7 HEAD)
  LOCAL_VERSION_LABEL="cu${MATRIX_CUDA_VERSION}torch${MATRIX_TORCH_VERSION}git${SHORT_HASH}"
  cd flash-attention/hopper
else
  LOCAL_VERSION_LABEL="cu${MATRIX_CUDA_VERSION}torch${MATRIX_TORCH_VERSION}"
  cd flash-attention
fi
NVCC_THREADS=$NVCC_THREADS MAX_JOBS=$MAX_JOBS \
  FLASH_ATTENTION_FORCE_BUILD=TRUE FLASH_ATTN_LOCAL_VERSION=${LOCAL_VERSION_LABEL} \
  NVCC_APPEND_FLAGS="--allow-unsupported-compiler" \
  time python setup.py bdist_wheel --dist-dir=dist
wheel_name=$(basename $(ls dist/*.whl | head -n 1))
echo "Built wheel: $wheel_name"

# Report ccache statistics (hit/miss) when enabled.
if [[ "${USE_CCACHE:-0}" == "1" ]] && command -v ccache >/dev/null 2>&1; then
  echo "=== ccache statistics ==="
  ccache -s || true
fi

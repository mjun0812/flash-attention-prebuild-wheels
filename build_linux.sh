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
  # Replace upstream hopper/setup.py with our patched version, which
  # suppresses verbose --resource-usage ptxas logs that would otherwise
  # clutter CI output with thousands of lines per build.
  cp "$(dirname "$0")/patches/fa3/setup.py" flash-attention/hopper/setup.py
  # If a previous attempt's ninja build directory was cached by the CI step
  # (Restore FA3 build directory cache), move it into place so ninja sees
  # the existing .o files and skips already-compiled translation units.
  #
  # mtime fixup: ninja decides to rebuild a .o when ANY header/source it
  # depends on (recorded in the .o.d depfile) has a newer mtime than the .o.
  # In CI, the venv (torch headers), CUDA toolkit and the freshly cloned
  # flash-attention sources all have mtime = "now", which would force ninja
  # to rebuild everything. Push every relevant input far into the past, then
  # re-touch the restored .o files to "now", so the comparison favors skip.
  if [ -d "$HOME/.fa-build-cache/build" ]; then
    echo "fa-build-cache: restoring previous ninja build directory"
    du -sh "$HOME/.fa-build-cache/build" || true
    mkdir -p flash-attention/hopper
    rm -rf flash-attention/hopper/build
    mv "$HOME/.fa-build-cache/build" flash-attention/hopper/build
    PAST=197001020000
    # FA3 sources + vendored cutlass / cute / etc. Exclude the build dir so
    # we don't downgrade the .o files we are about to re-touch.
    find flash-attention -path flash-attention/hopper/build -prune -o -type f -print 2>/dev/null \
      | xargs -r touch -t "$PAST" 2>/dev/null || true
    # torch + python headers inside the venv
    if [ -d .venv ]; then
      find .venv/lib -path '*/site-packages/torch/include*' -type f \
        -exec touch -t "$PAST" {} + 2>/dev/null || true
    fi
    # CUDA toolkit headers (sudo since /usr/local/cuda is root-owned)
    if [ -d /usr/local/cuda/include ]; then
      sudo find /usr/local/cuda/include -type f \
        -exec touch -t "$PAST" {} + 2>/dev/null || true
    fi
    # Mark the .o tree as "now" — newer than every header/source above.
    find flash-attention/hopper/build -exec touch {} + 2>/dev/null || true
    echo "fa-build-cache: mtime fixup done (sources/headers -> $PAST, .o -> now)"
    # DEBUG: dump ninja state and ask ninja itself why it would rebuild.
    BUILD_TEMP=flash-attention/hopper/build/temp.linux-aarch64-cpython-312
    echo "=== DEBUG: ninja state under $BUILD_TEMP ==="
    if [ -d "$BUILD_TEMP" ]; then
      echo "--- ls -la (top-level):"
      ls -la "$BUILD_TEMP" | head -20 || true
      echo "--- ls -la (instantiations/) sample:"
      ls -la "$BUILD_TEMP/instantiations" 2>/dev/null | head -10 || true
      echo "--- build.ninja:"
      ls -la "$BUILD_TEMP/build.ninja" 2>/dev/null || echo "  missing"
      echo "--- .ninja_log:"
      ls -la "$BUILD_TEMP/.ninja_log" 2>/dev/null || echo "  missing"
      [ -f "$BUILD_TEMP/.ninja_log" ] && head -20 "$BUILD_TEMP/.ninja_log"
      echo "--- .ninja_deps:"
      ls -la "$BUILD_TEMP/.ninja_deps" 2>/dev/null || echo "  missing"
      echo "--- representative mtimes (.o, .cpp, torch.h, cuda.h):"
      stat -c '%y %n' "$BUILD_TEMP/flash_api_stable.o" 2>/dev/null || echo "  no .o"
      stat -c '%y %n' flash-attention/hopper/flash_api_stable.cpp 2>/dev/null || echo "  no .cpp"
      ls .venv/lib/python*/site-packages/torch/include/torch/torch.h 2>/dev/null \
        | head -1 | xargs -r stat -c '%y %n' || echo "  no torch.h"
      stat -c '%y %n' /usr/local/cuda/include/cuda.h 2>/dev/null || echo "  no cuda.h"
      # Ask ninja to dry-run and explain.
      uv pip install --quiet ninja 2>/dev/null || true
      if command -v ninja >/dev/null && [ -f "$BUILD_TEMP/build.ninja" ]; then
        echo "--- ninja --version: $(ninja --version 2>/dev/null || true)"
        echo "--- ninja -d explain -n (first 80 lines):"
        (cd "$BUILD_TEMP" && ninja -d explain -n 2>&1) | head -80 || true
      else
        echo "--- ninja not available or build.ninja missing"
      fi
    else
      echo "  $BUILD_TEMP does not exist"
    fi
    echo "=== END DEBUG ==="
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

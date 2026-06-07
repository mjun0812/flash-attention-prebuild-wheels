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
  # ninja's .ninja_deps records each .o's input header mtimes at nanosecond
  # precision. The cached .o tree keeps its mtimes (tar via actions/cache),
  # but cutlass / cute headers are freshly cloned every CI run and therefore
  # mismatch what .ninja_deps recorded — ninja would mark every dependent .o
  # 'dirty' and rebuild from scratch. To make the recorded mtimes valid
  # again, we also cache the cutlass/cute headers and restore them next to
  # the build dir with their original mtimes preserved (cp/mv keep mtimes,
  # tar in actions/cache preserves them too). The same problem exists for
  # torch and CUDA headers, but the deps info appears to be matchable for
  # them under our setup; if not, add them to the cache stash too.
  if [ -d "$HOME/.fa-build-cache/build" ]; then
    echo "fa-build-cache: restoring previous ninja build directory"
    du -sh "$HOME/.fa-build-cache/build" || true
    mkdir -p flash-attention/hopper
    rm -rf flash-attention/hopper/build
    mv "$HOME/.fa-build-cache/build" flash-attention/hopper/build
    if [ -d "$HOME/.fa-build-cache/cutlass" ]; then
      echo "fa-build-cache: restoring cutlass/cute headers with preserved mtimes"
      du -sh "$HOME/.fa-build-cache/cutlass" || true
      rm -rf flash-attention/csrc/cutlass
      mv "$HOME/.fa-build-cache/cutlass" flash-attention/csrc/cutlass
    fi
    # The cached .o files have whole-second mtimes from the previous cap
    # (e.g. 2026-06-07 07:34:56). The freshly cloned FA3 sources, the
    # uv-installed torch headers and the setup-cuda CUDA headers all have
    # mtime "now". ninja compares output.o vs each input mtime, so without
    # this step every restored .o looks older than its .cu source and ninja
    # rebuilds. Push every non-cached input far into the past so the .o
    # remains strictly newer than its sources/headers.
    PAST=197001020000
    find flash-attention -path flash-attention/hopper/build -prune \
                          -o -path flash-attention/csrc/cutlass -prune \
                          -o -type f -print 2>/dev/null \
      | xargs -r touch -t "$PAST" 2>/dev/null || true
    if [ -d .venv ]; then
      find .venv/lib -path '*/site-packages/torch/include*' -type f \
        -exec touch -t "$PAST" {} + 2>/dev/null || true
    fi
    if [ -d /usr/local/cuda/include ]; then
      sudo find /usr/local/cuda/include -type f \
        -exec touch -t "$PAST" {} + 2>/dev/null || true
    fi
    echo "fa-build-cache: backdated FA3 sources + torch/CUDA headers to $PAST"
    # Reconcile ninja's stat-based view with the restored tree:
    # - the staging step truncated every mtime (including the per-target
    #   mtimes inside .ninja_deps) to whole seconds before save, so the .o
    #   stat values after tar/restore are bit-exact with what .ninja_deps
    #   records;
    # - run `ninja -t restat` over every .o so .ninja_log is also synced to
    #   the restored mtimes. Without this, ninja would treat each .o as if
    #   it had been touched out-of-band and rerun the build edge.
    BUILD_TEMP=flash-attention/hopper/build/temp.linux-aarch64-cpython-312
    if [ -f "$BUILD_TEMP/build.ninja" ]; then
      uv pip install --quiet ninja 2>/dev/null || true
      if command -v ninja >/dev/null; then
        # Pass relative .o paths so `ninja -C $BUILD_TEMP -t restat` finds them
        # via its build graph instead of misinterpreting absolute paths.
        ( cd "$BUILD_TEMP" \
          && find . -name '*.o' -type f -printf '%P\n' \
            | xargs -r -n 500 ninja -t restat \
        ) 2>/dev/null || true
      fi
    fi
    echo "fa-build-cache: restore done (build + cutlass + ninja restat)"
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

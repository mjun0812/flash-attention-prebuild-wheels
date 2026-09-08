#!/bin/bash

set -e

# torch >= 2.14 headers (ATen/ATen.h, torch/all.h) `#error` when
# __cplusplus < 202002L on non-MSVC compilers, but FA2 pins -std=c++17 for
# every extension it builds, so the ROCm path needs the same C++20 bump as
# build_linux.sh. Gated on torch (major.minor) >= 2.14 so torch <= 2.13
# keeps its c++17 path.
fa2_needs_cxx20() {
  awk -v v="$1" 'BEGIN { split(v, a, "."); exit !((a[1] > 2) || (a[1] == 2 && a[2] >= 14)) }'
}

# Parameters
FLASH_ATTN_VERSION=$1
PYTHON_VERSION=$2
TORCH_VERSION=$3
ROCM_VERSION=$4

# Reject FA3 before installing torch or cloning, so the guard is reproducible
# outside a ROCm environment. FA3 (hopper) is CUDA/Hopper only.
if [[ "$FLASH_ATTN_VERSION" == fa3:* ]]; then
  echo "FA3 (Flash Attention 3) is not supported on ROCm; use an FA2 version such as 2.8.3"
  exit 1
fi

echo "Building Flash Attention for ROCm with parameters:"
echo "  Flash-Attention: $FLASH_ATTN_VERSION"
echo "  Python: $PYTHON_VERSION"
echo "  PyTorch: $TORCH_VERSION"
echo "  ROCm: $ROCM_VERSION"

MATRIX_TORCH_VERSION=$(echo $TORCH_VERSION | awk -F \. {'print $1 "." $2'})

echo "Derived versions:"
echo "  Torch Matrix: $MATRIX_TORCH_VERSION"

# Install PyTorch (ROCm build)
echo "Installing PyTorch $TORCH_VERSION for ROCm $ROCM_VERSION..."
pip install --force-reinstall --no-cache-dir torch==$TORCH_VERSION --index-url https://download.pytorch.org/whl/rocm${ROCM_VERSION}

# Verify installation
echo "Verifying installations..."
hipcc --version
python -V
python -c "import torch; print('PyTorch:', torch.__version__)"
python -c "import torch; print('HIP:', torch.version.hip)"

# Checkout flash-attn
echo "Checking out flash-attention v${FLASH_ATTN_VERSION}..."
git clone https://github.com/Dao-AILab/flash-attention.git flash-attention -b "v$FLASH_ATTN_VERSION"
if fa2_needs_cxx20 "$MATRIX_TORCH_VERSION"; then
  if [ "$(grep -c -- '-std=c++17' flash-attention/setup.py)" -eq 0 ]; then
    echo "-std=c++17 not found in flash-attention/setup.py; upstream setup.py may have changed"
    exit 1
  fi
  sed -i 's/-std=c++17/-std=c++20/g' flash-attention/setup.py
  echo "Patched flash-attention/setup.py std to c++20 for torch $MATRIX_TORCH_VERSION"
fi
# Remove FA4 (flash_attn/cute) to prevent it from being included in the FA2 wheel
rm -rf flash-attention/flash_attn/cute

# Determine MAX_JOBS based on system resources. The ROCm path of upstream
# setup.py never calls append_nvcc_threads, so MAX_JOBS is the only knob.
NUM_THREADS=$(nproc)
RAM_GB=$(free -g | awk '/^Mem:/{print $2}')
echo "System resources:"
echo "  CPU threads: $NUM_THREADS"
echo "  RAM: ${RAM_GB}GB"
if [[ -z "${MAX_JOBS:-}" ]]; then
  # Each job peaks at ~2.8GB, so cap by RAM as well as by CPU threads
  MAX_JOBS_CPU=$NUM_THREADS
  MAX_JOBS_RAM=$(awk -v ram="$RAM_GB" 'BEGIN {print int(ram / 2.8)}')
  MAX_JOBS=$((MAX_JOBS_CPU < MAX_JOBS_RAM ? MAX_JOBS_CPU : MAX_JOBS_RAM))
  MAX_JOBS=$((MAX_JOBS < 1 ? 1 : MAX_JOBS))
fi
echo "Build parallelism settings:"
echo "  MAX_JOBS: $MAX_JOBS"

# Build wheels
echo "Building wheels..."
GPU_ARCHS="${GPU_ARCHS:-gfx90a;gfx942;gfx950}"
LOCAL_VERSION_LABEL="rocm${ROCM_VERSION}torch${MATRIX_TORCH_VERSION}"
echo "  GPU_ARCHS: $GPU_ARCHS"
echo "  Local version label: $LOCAL_VERSION_LABEL"
cd flash-attention
export BUILD_TARGET=rocm
export GPU_ARCHS
export MAX_JOBS
export FLASH_ATTENTION_FORCE_BUILD=TRUE
export FLASH_ATTN_LOCAL_VERSION=$LOCAL_VERSION_LABEL
time python setup.py bdist_wheel --dist-dir=dist
wheel_name=$(basename $(ls dist/*.whl | head -n 1))
echo "Built wheel: $wheel_name"

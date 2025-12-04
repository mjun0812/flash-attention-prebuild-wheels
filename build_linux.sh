#!/bin/bash

set -e

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

# Checkout flash-attn
echo "Checking out flash-attention v$FLASH_ATTN_VERSION..."
git clone https://github.com/Dao-AILab/flash-attention.git -b "v$FLASH_ATTN_VERSION"

# Determine MAX_JOBS and NVCC_THREADS based on system resources
NUM_THREADS=$(nproc)
RAM_GB=$(free -g | awk '/^Mem:/{print $2}')
echo "System resources:"
echo "  CPU threads: $NUM_THREADS"
echo "  RAM: ${RAM_GB}GB"

# Calculate max product based on following constraints:
# - MAX_JOBS x NVCC_THREADS <= NUM_THREADS
# - 2.5GB x MAX_JOBS x NVCC_THREADS <= RAM_GB
MAX_PRODUCT_CPU=$NUM_THREADS
MAX_PRODUCT_RAM=$(awk -v ram="$RAM_GB" 'BEGIN {print int(ram / 2.5)}')
MAX_PRODUCT=$((MAX_PRODUCT_CPU < MAX_PRODUCT_RAM ? MAX_PRODUCT_CPU : MAX_PRODUCT_RAM))

# Set MAX_JOBS = NVCC_THREADS = floor(sqrt(MAX_PRODUCT))
MAX_JOBS=$(awk -v max="$MAX_PRODUCT" 'BEGIN {print int(sqrt(max))}')
NVCC_THREADS=$MAX_JOBS

# Ensure minimum values of 1
MAX_JOBS=$((MAX_JOBS < 1 ? 1 : MAX_JOBS))
NVCC_THREADS=$((NVCC_THREADS < 1 ? 1 : NVCC_THREADS))

echo "Build parallelism settings:"
echo "  MAX_JOBS: $MAX_JOBS"
echo "  NVCC_THREADS: $NVCC_THREADS"

# Build wheels
echo "Building wheels..."
cd flash-attention
LOCAL_VERSION_LABEL="cu${MATRIX_CUDA_VERSION}torch${MATRIX_TORCH_VERSION}"
NVCC_THREADS=$NVCC_THREADS MAX_JOBS=$MAX_JOBS FLASH_ATTENTION_FORCE_BUILD=TRUE FLASH_ATTN_LOCAL_VERSION=${LOCAL_VERSION_LABEL} \
  python setup.py bdist_wheel --dist-dir=dist
wheel_name=$(basename $(ls dist/*.whl | head -n 1))
echo "Built wheel: $wheel_name"

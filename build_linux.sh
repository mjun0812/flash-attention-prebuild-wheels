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

# Build wheels
echo "Building wheels..."
cd flash-attention
LOCAL_VERSION_LABEL="cu${MATRIX_CUDA_VERSION}torch${MATRIX_TORCH_VERSION}"
FLASH_ATTENTION_FORCE_BUILD=TRUE FLASH_ATTN_LOCAL_VERSION=${LOCAL_VERSION_LABEL} python setup.py bdist_wheel --dist-dir=dist
base_wheel_name=$(basename $(ls dist/*.whl | head -n 1))
wheel_name=$(echo $base_wheel_name | sed "s/$FLASH_ATTN_VERSION/$FLASH_ATTN_VERSION+cu${MATRIX_CUDA_VERSION}torch${MATRIX_TORCH_VERSION}/")
mv -v dist/$base_wheel_name dist/$wheel_name
echo "Built wheel: $wheel_name"

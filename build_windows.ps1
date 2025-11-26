param(
    [Parameter(Mandatory=$true)]
    [string]$FlashAttnVersion,

    [Parameter(Mandatory=$true)]
    [string]$PythonVersion,

    [Parameter(Mandatory=$true)]
    [string]$TorchVersion,

    [Parameter(Mandatory=$true)]
    [string]$CudaVersion
)

# Error handling
$ErrorActionPreference = "Stop"

Write-Host "Building Flash Attention with parameters:"
Write-Host "  Flash-Attention: $FlashAttnVersion"
Write-Host "  Python: $PythonVersion"
Write-Host "  PyTorch: $TorchVersion"
Write-Host "  CUDA: $CudaVersion"

# Set CUDA and PyTorch versions
$CudaVersionClean = $CudaVersion -replace '\.', ''
$MatrixCudaVersion = $CudaVersionClean.Substring(0, [Math]::Min(3, $CudaVersionClean.Length))
$MatrixTorchVersion = $TorchVersion -replace '^(\d+\.\d+).*', '$1'

Write-Host "Derived versions:"
Write-Host "  CUDA Matrix: $MatrixCudaVersion"
Write-Host "  Torch Matrix: $MatrixTorchVersion"

# Install PyTorch
$env:TORCH_CUDA_VERSION = python get_torch_cuda_version.py $MatrixCudaVersion $MatrixTorchVersion

Write-Host "Installing PyTorch $TorchVersion+cu$env:TORCH_CUDA_VERSION..."
if ($TorchVersion -like "*dev*") {
    pip install --force-reinstall --no-cache-dir --pre torch==$TorchVersion --index-url https://download.pytorch.org/whl/nightly/cu$env:TORCH_CUDA_VERSION
} else {
    pip install --force-reinstall --no-cache-dir torch==$TorchVersion --index-url https://download.pytorch.org/whl/cu$env:TORCH_CUDA_VERSION
}

# Verify installation
Write-Host "Verifying installations..."
nvcc --version
python -V
python -c "import torch; print('PyTorch:', torch.__version__)"
python -c "import torch; print('CUDA:', torch.version.cuda)"
python -c "from torch.utils import cpp_extension; print(cpp_extension.CUDA_HOME)"

# Checkout flash-attn
Write-Host "Checking out flash-attention v$FlashAttnVersion..."
git clone https://github.com/Dao-AILab/flash-attention.git -b "v$FlashAttnVersion"

# Build wheels
Write-Host "Building wheels..."
Import-Module 'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\Common7\Tools\Microsoft.VisualStudio.DevShell.dll'
Enter-VsDevShell -VsInstallPath 'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools' -DevCmdArguments '-arch=x64 -host_arch=x64'
$env:DISTUTILS_USE_SDK = 1
$env:BUILD_TARGET = "cuda"
# Use environment variables from workflow if available, otherwise use defaults
if (-not $env:MAX_JOBS) { $env:MAX_JOBS = "2" }
if (-not $env:NVCC_THREADS) { $env:NVCC_THREADS = "2" }
Write-Host "Environment variables:"
Write-Host "  MAX_JOBS: $env:MAX_JOBS"
Write-Host "  NVCC_THREADS: $env:NVCC_THREADS"
$env:FLASH_ATTENTION_FORCE_BUILD = "TRUE"
$env:NVCC_FLAGS = "-w --disable-warnings"
$env:CXXFLAGS = "/w"
$env:CFLAGS = "/w"
$env:FLASH_ATTN_LOCAL_VERSION = "cu$MatrixCudaVersion" + "torch$MatrixTorchVersion"

cd flash-attention
python setup.py bdist_wheel --dist-dir=dist
$WheelName = Get-ChildItem -Path "dist\*.whl" | Select-Object -First 1 | ForEach-Object { $_.Name }
Write-Host "Built wheel: $wheelName"

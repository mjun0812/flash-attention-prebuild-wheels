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

Write-Host "::group::Installing PyTorch $TorchVersion+cu$env:TORCH_CUDA_VERSION"
if ($TorchVersion -like "*dev*") {
    pip install -q --force-reinstall --no-cache-dir --pre torch==$TorchVersion --index-url https://download.pytorch.org/whl/nightly/cu$env:TORCH_CUDA_VERSION
} else {
    pip install -q --force-reinstall --no-cache-dir torch==$TorchVersion --index-url https://download.pytorch.org/whl/cu$env:TORCH_CUDA_VERSION
}
Write-Host "::endgroup::"

# Verify installation
Write-Host "::group::Verifying installations"
nvcc --version
python -V
python -c "import torch; print('PyTorch:', torch.__version__)"
python -c "import torch; print('CUDA:', torch.version.cuda)"
python -c "from torch.utils import cpp_extension; print(cpp_extension.CUDA_HOME)"
Write-Host "::endgroup::"

# Checkout flash-attn
if ($FlashAttnVersion -like "fa3:*") {
    $IsFa3 = $true
    $Fa3Commit = $FlashAttnVersion.Substring(4)
    Write-Host "::group::Building Flash Attention 3 (commit: $Fa3Commit)"
    git clone -q https://github.com/Dao-AILab/flash-attention.git
    Push-Location flash-attention
    git checkout $Fa3Commit
    Pop-Location
    Write-Host "::endgroup::"
} else {
    $IsFa3 = $false
    Write-Host "::group::Checking out flash-attention v$FlashAttnVersion"
    git clone -q https://github.com/Dao-AILab/flash-attention.git -b "v$FlashAttnVersion"
    # Remove FA4 (flash_attn/cute) to prevent it from being included in the FA2 wheel
    if (Test-Path "flash-attention\flash_attn\cute") {
        Remove-Item -Recurse -Force "flash-attention\flash_attn\cute"
        Write-Host "Removed flash_attn/cute (FA4) from FA2 build"
    }
    Write-Host "::endgroup::"
}

# Build wheels
Write-Host "::group::Setting up build environment"
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
# Suppress compiler warnings and verbose output
$env:NVCC_FLAGS = "-w --disable-warnings"
$env:CXXFLAGS = "/w"
$env:CFLAGS = "/w"
# Suppress ninja verbose output
$env:NINJA_STATUS = ""
if ($IsFa3) {
    Push-Location flash-attention
    $ShortHash = (git rev-parse --short=7 HEAD).Trim()
    Pop-Location
    $env:FLASH_ATTN_LOCAL_VERSION = "cu$MatrixCudaVersion" + "torch$MatrixTorchVersion" + "git$ShortHash"
} else {
    $env:FLASH_ATTN_LOCAL_VERSION = "cu$MatrixCudaVersion" + "torch$MatrixTorchVersion"
}
Write-Host "::endgroup::"

Write-Host "::group::Building Flash Attention wheel (this takes a while...)"
if ($IsFa3) {
    # Replace setup.py with Windows-patched version (based on upstream PR #2047)
    # This handles: Linux-only NVIDIA toolchain download skip, and
    # Windows linker command line length limit via Ninja response files.
    $patchedSetup = Join-Path $PSScriptRoot "patches\fa3\setup.py"
    Copy-Item $patchedSetup "flash-attention\hopper\setup.py" -Force
    Write-Host "Replaced hopper/setup.py with Windows-patched version"
    cd flash-attention\hopper
} else {
    cd flash-attention
}
python setup.py bdist_wheel --dist-dir=dist
Write-Host "::endgroup::"

$WheelName = Get-ChildItem -Path "dist\*.whl" | Select-Object -First 1 | ForEach-Object { $_.Name }
Write-Host "Built wheel: $wheelName"

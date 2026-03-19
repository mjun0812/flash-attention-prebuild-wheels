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

function Invoke-FilteredNativeCommand {
    param(
        [Parameter(Mandatory=$true)]
        [scriptblock]$Command,

        [Parameter(Mandatory=$true)]
        [string]$LogPath
    )

    $includeNotePattern = '^(メモ: インクルード ファイル:|Note: including file:)'
    $duplicateWarningPattern = '^cl : .*warning D9025'
    $templateInstantiationPattern = '^\s*instantiation of "'
    $suppressedIncludeNotes = 0
    $suppressedDuplicateWarnings = 0
    $suppressedTemplateInstantiations = 0
    $templateNoticeShown = $false
    $seenWarnings = New-Object 'System.Collections.Generic.HashSet[string]'

    if (Test-Path $LogPath) {
        Remove-Item -Path $LogPath -Force
    }

    & $Command 2>&1 |
        Tee-Object -FilePath $LogPath |
        ForEach-Object {
            $line = [string]$_
            $shouldEmit = $true

            if ($line -match $includeNotePattern) {
                $suppressedIncludeNotes++
                $shouldEmit = $false
            } elseif ($line -match $duplicateWarningPattern) {
                if (-not $seenWarnings.Add($line)) {
                    $suppressedDuplicateWarnings++
                    $shouldEmit = $false
                }
            } elseif ($line -match $templateInstantiationPattern) {
                $suppressedTemplateInstantiations++
                if (-not $templateNoticeShown) {
                    Write-Host "[log-filter] Suppressing verbose template instantiation traces. Raw log: $LogPath"
                    $templateNoticeShown = $true
                }
                $shouldEmit = $false
            }

            if ($shouldEmit) {
                Write-Host $line
            }
        }

    $exitCode = $LASTEXITCODE
    Write-Host "[log-filter] Suppressed $suppressedIncludeNotes include-note lines, $suppressedDuplicateWarnings duplicate D9025 warnings, and $suppressedTemplateInstantiations template-instantiation lines."
    return $exitCode
}

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

# FlashAttention Variant handling
$FlashAttnVariant = ""
if ($FlashAttnVersion -like "fa3:*") {
    $FlashAttnVariant = "Flash Attention 3"
} else {
    $FlashAttnVariant = "Flash Attention 2"
}
Write-Host "Selected Flash Attention variant: $FlashAttnVariant"

# Checkout flash-attn
if ($FlashAttnVariant -eq "Flash Attention 3") {
    $FaCommit = $FlashAttnVersion.Substring(4)
    Write-Host "::group::Building $FlashAttnVariant (commit: $FaCommit)"
    git clone -q https://github.com/Dao-AILab/flash-attention.git flash-attention
    git -C flash-attention checkout $FaCommit
    # Replace upstream setup.py with patched version
    $patchedSetup = Join-Path $PSScriptRoot "patches\fa3\setup.py"
    Copy-Item $patchedSetup "flash-attention\hopper\setup.py" -Force
    Write-Host "::endgroup::"
} elseif ($FlashAttnVariant -eq "Flash Attention 2") {
    Write-Host "::group::Checking out flash-attention v$FlashAttnVersion"
    git clone -q https://github.com/Dao-AILab/flash-attention.git flash-attention -b "v$FlashAttnVersion"
    # Remove FA4 (flash_attn/cute) to prevent it from being included in the FA2 wheel
    if (Test-Path "flash-attention\flash_attn\cute") {
        Remove-Item -Recurse -Force "flash-attention\flash_attn\cute"
        Write-Host "Removed flash_attn/cute (FA4) from FA2 build"
    }
    Write-Host "::endgroup::"
} else {
    Write-Host "Unknown Flash Attention variant: $FlashAttnVariant"
    exit 1
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
# Avoid verbose dependency-generation output from nvcc on Windows builds.
$env:TORCH_EXTENSION_SKIP_NVCC_GEN_DEPENDENCIES = "1"
# Suppress ninja verbose output
$env:NINJA_STATUS = ""
if ($FlashAttnVariant -eq "Flash Attention 3") {
    $ShortHash = (git -C flash-attention rev-parse --short=7 HEAD).Trim()
    $env:FLASH_ATTN_LOCAL_VERSION = "cu$MatrixCudaVersion" + "torch$MatrixTorchVersion" + "git$ShortHash"
} else {
    $env:FLASH_ATTN_LOCAL_VERSION = "cu$MatrixCudaVersion" + "torch$MatrixTorchVersion"
}
Write-Host "::endgroup::"

$WorkspaceRoot = if ($env:GITHUB_WORKSPACE) { $env:GITHUB_WORKSPACE } else { (Get-Location).Path }
$BuildLogPath = Join-Path $WorkspaceRoot "windows-build-raw.log"
if ($env:GITHUB_ENV) {
    "build_log_path=$BuildLogPath" | Out-File -FilePath $env:GITHUB_ENV -Encoding utf8 -Append
}

Write-Host "::group::Building Flash Attention wheel (this takes a while...)"
if ($FlashAttnVariant -eq "Flash Attention 3") {
    cd flash-attention\hopper
} else {
    cd flash-attention
}
$BuildExitCode = Invoke-FilteredNativeCommand -LogPath $BuildLogPath -Command {
    python setup.py bdist_wheel --dist-dir=dist
}
Write-Host "::endgroup::"

if ($BuildExitCode -ne 0) {
    Write-Host "Build failed. Full raw log saved to: $BuildLogPath"
    exit $BuildExitCode
}

$WheelName = Get-ChildItem -Path "dist\*.whl" | Select-Object -First 1 | ForEach-Object { $_.Name }
Write-Host "Built wheel: $wheelName"

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

    $suppressionRules = @(
        @{
            Name = "include-note lines"
            Pattern = '^(メモ: インクルード ファイル:|Note: including file:)'
        },
        @{
            Name = "duplicate D9025 warnings"
            Pattern = '^cl : .*warning D9025'
            Deduplicate = $true
        },
        @{
            Name = "template-instantiation lines"
            Pattern = '^\s*instantiation of "'
            Notice = "Suppressing verbose template instantiation traces. Raw log: $LogPath"
        },
        @{
            Name = "torch CUDA probe warnings"
            Pattern = 'UserWarning: cudaGetDeviceCount\(\) returned cudaErrorNotSupported'
        },
        @{
            Name = "wheel bdist_wheel FutureWarnings"
            Pattern = "FutureWarning: The 'wheel' package is no longer the canonical location of the 'bdist_wheel' command"
        },
        @{
            Name = "cl D9002 warnings"
            Pattern = '^cl : .*warning D9002'
        },
        @{
            Name = "MSVC C4996 warnings"
            Pattern = 'warning C4996:'
        },
        @{
            Name = "CUDA diagnostic #177-D warnings"
            Pattern = 'warning #177-D:'
            SuppressContinuation = $true
            Notice = "Suppressing verbose CUDA diagnostic blocks. Raw log: $LogPath"
        },
        @{
            Name = "CUDA diagnostic #186-D warnings"
            Pattern = 'warning #186-D:'
            SuppressContinuation = $true
            Notice = "Suppressing verbose CUDA diagnostic blocks. Raw log: $LogPath"
        },
        @{
            Name = "CUDA diagnostic #221-D warnings"
            Pattern = 'warning #221-D:'
            SuppressContinuation = $true
            Notice = "Suppressing verbose CUDA diagnostic blocks. Raw log: $LogPath"
        },
        @{
            Name = "CUDA diagnostic #550-D warnings"
            Pattern = 'warning #550-D:'
            SuppressContinuation = $true
            Notice = "Suppressing verbose CUDA diagnostic blocks. Raw log: $LogPath"
        },
        @{
            Name = "CUDA diagnostic remarks"
            Pattern = '^Remark: The warnings can be suppressed with "-diag-suppress <warning-number>"'
        }
    )
    $suppressedCounts = @{}
    foreach ($rule in $suppressionRules) {
        $suppressedCounts[$rule.Name] = 0
    }
    $diagnosticContinuationPattern = '^(?:\s+\S.*|\s*\^$|\s*detected during:$|\s*$)'
    $suppressedDiagnosticContinuationLines = 0
    $suppressedContinuation = $false
    $shownNotices = New-Object 'System.Collections.Generic.HashSet[string]'
    $seenWarnings = New-Object 'System.Collections.Generic.HashSet[string]'

    if (Test-Path $LogPath) {
        Remove-Item -Path $LogPath -Force
    }

    & $Command 2>&1 |
        Tee-Object -FilePath $LogPath |
        ForEach-Object {
            $line = [string]$_
            $shouldEmit = $true

            if ($suppressedContinuation) {
                if ($line -match $diagnosticContinuationPattern) {
                    $suppressedDiagnosticContinuationLines++
                    $shouldEmit = $false
                } else {
                    $suppressedContinuation = $false
                }
            }

            if ($shouldEmit) {
                foreach ($rule in $suppressionRules) {
                    if ($line -match $rule.Pattern) {
                        if ($rule.Deduplicate) {
                            if (-not $seenWarnings.Add($line)) {
                                $suppressedCounts[$rule.Name]++
                                $shouldEmit = $false
                            }
                        } else {
                            $suppressedCounts[$rule.Name]++
                            $shouldEmit = $false
                        }

                        if (-not $shouldEmit) {
                            if ($rule.SuppressContinuation) {
                                $suppressedContinuation = $true
                            }
                            if ($rule.Notice -and $shownNotices.Add($rule.Notice)) {
                                Write-Host "[log-filter] $($rule.Notice)"
                            }
                        }

                        break
                    }
                }
            }

            if ($shouldEmit) {
                Write-Host $line
            }
        }

    $exitCode = $LASTEXITCODE
    $summaryParts = @()
    foreach ($rule in $suppressionRules) {
        $count = [int]$suppressedCounts[$rule.Name]
        if ($count -gt 0) {
            $summaryParts += "$count $($rule.Name)"
        }
    }
    if ($suppressedDiagnosticContinuationLines -gt 0) {
        $summaryParts += "$suppressedDiagnosticContinuationLines diagnostic-context lines"
    }
    if ($summaryParts.Count -gt 0) {
        Write-Host "[log-filter] Suppressed $($summaryParts -join ', ')."
    } else {
        Write-Host "[log-filter] No lines suppressed."
    }
    return $exitCode
}

function Test-Cuda13OrNewer {
    param(
        [Parameter(Mandatory=$true)]
        [string]$Version
    )

    try {
        return ([Version]$Version -ge [Version]"13.0")
    } catch {
        Write-Warning "Could not parse CUDA version '$Version' for alignment workaround check. Skipping CUDA 13.0+ patches."
        return $false
    }
}

function Apply-GitPatch {
    param(
        [Parameter(Mandatory=$true)]
        [string]$RepoPath,

        [Parameter(Mandatory=$true)]
        [string]$PatchPath,

        [Parameter(Mandatory=$true)]
        [string]$Description
    )

    if (-not (Test-Path $PatchPath)) {
        Write-Error "Patch file not found: $PatchPath"
        exit 1
    }

    Write-Host "Applying $Description..."
    git -C $RepoPath apply --ignore-whitespace $PatchPath
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to apply $Description"
        exit 1
    }
    Write-Host "$Description applied successfully"
}

function Apply-CudaToolkitPatch {
    param(
        [Parameter(Mandatory=$true)]
        [string]$CudaHome,

        [Parameter(Mandatory=$true)]
        [string]$PatchPath,

        [Parameter(Mandatory=$true)]
        [string]$Description
    )

    if (-not (Test-Path $PatchPath)) {
        Write-Error "Patch file not found: $PatchPath"
        exit 1
    }
    if (-not $CudaHome -or -not (Test-Path $CudaHome)) {
        Write-Error "CUDA_HOME not found: $CudaHome"
        exit 1
    }

    $gitExe = (Get-Command git -ErrorAction SilentlyContinue).Source
    if (-not $gitExe) {
        Write-Error "git.exe not found on PATH; cannot locate patch.exe"
        exit 1
    }

    $gitRoot = Split-Path (Split-Path $gitExe -Parent) -Parent
    $patchExe = Join-Path $gitRoot "usr\bin\patch.exe"
    if (-not (Test-Path $patchExe)) {
        Write-Error "patch.exe not found at expected path: $patchExe"
        exit 1
    }

    Write-Host "Applying $Description..."
    & $patchExe --fuzz 2 -p1 --directory $CudaHome -i $PatchPath
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to apply $Description"
        exit 1
    }
    Write-Host "$Description applied successfully"
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
    # MSVC cannot pass 128-byte aligned CUDA-generated types by value on CUDA 13.0+.
    if (Test-Cuda13OrNewer -Version $CudaVersion) {
        $cutlassPatch = Join-Path $PSScriptRoot "patches\fa3\cutlass_alignment_fix.patch"
        $cudaHeaderPatch = Join-Path $PSScriptRoot "patches\fa3\cuda_h_alignment_fix.patch"

        git -C flash-attention submodule update --init csrc/cutlass
        if ($LASTEXITCODE -ne 0) {
            Write-Error "Failed to initialize cutlass submodule for CUDA 13.0+ alignment workaround"
            exit 1
        }

        $cutlassRoot = Join-Path (Resolve-Path "flash-attention").Path "csrc\cutlass"
        Apply-GitPatch -RepoPath $cutlassRoot -PatchPath $cutlassPatch -Description "cutlass alignment workaround for CUDA 13.0+"
        Apply-CudaToolkitPatch -CudaHome $env:CUDA_HOME -PatchPath $cudaHeaderPatch -Description "CUDA header alignment workaround for CUDA 13.0+"
    }
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
# Determine MAX_JOBS and NVCC_THREADS based on system resources
$NumThreads = (Get-CimInstance Win32_ComputerSystem).NumberOfLogicalProcessors
$RamGB = [math]::Floor((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1GB)
Write-Host "System resources:"
Write-Host "  CPU threads: $NumThreads"
Write-Host "  RAM: ${RamGB}GB"
if (-not $env:MAX_JOBS -and -not $env:NVCC_THREADS) {
    # Calculate max product based on following constraints:
    # - MAX_JOBS x NVCC_THREADS(<= 4) <= NUM_THREADS
    # - 5GB x MAX_JOBS x NVCC_THREADS(<= 4) <= RAM_GB
    # SM90 (FA3) kernels require significantly more memory per ptxas process on Windows.
    $MaxProductCpu = $NumThreads
    $MaxProductRam = [math]::Floor($RamGB / 5)
    $MaxProduct = [math]::Min($MaxProductCpu, $MaxProductRam)

    $BaseThreads = [math]::Floor([math]::Sqrt($MaxProduct))

    if ($RamGB -le 16) {
        # If RAM is 16GB or less, set NVCC_THREADS to 1 and MAX_JOBS to 2
        $env:NVCC_THREADS = "1"
        $env:MAX_JOBS = "2"
    } elseif ($BaseThreads -le 4) {
        $env:NVCC_THREADS = "$BaseThreads"
        $env:MAX_JOBS = "$BaseThreads"
    } else {
        $env:NVCC_THREADS = "4"
        $env:MAX_JOBS = "$([math]::Floor($MaxProduct / 4))"
    }

    # Ensure minimum values of 1
    if ([int]$env:MAX_JOBS -lt 1) { $env:MAX_JOBS = "1" }
    if ([int]$env:NVCC_THREADS -lt 1) { $env:NVCC_THREADS = "1" }
}
Write-Host "Build parallelism settings:"
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

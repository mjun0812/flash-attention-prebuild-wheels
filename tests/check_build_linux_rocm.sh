#!/bin/bash
# Acceptance checks for build_linux_rocm.sh (T-001).
#
# Each acceptance criterion is one invocation:
#   tests/check_build_linux_rocm.sh ac1   # syntax is sound
#   tests/check_build_linux_rocm.sh ac2   # FA3 is rejected
#   tests/check_build_linux_rocm.sh ac3   # no CUDA-only env vars
#   tests/check_build_linux_rocm.sh ac4   # hipcc is routed through ccache
#
# These run without a ROCm toolchain, an AMD GPU, or network access.

set -u

REPO_ROOT=$(cd "$(dirname "$0")/.." && pwd)
SCRIPT="$REPO_ROOT/build_linux_rocm.sh"

fail() {
  echo "FAIL: $*"
  exit 1
}

pass() {
  echo "PASS: $*"
  exit 0
}

require_script() {
  [ -f "$SCRIPT" ] || fail "$SCRIPT does not exist"
}

ac1() {
  require_script
  if bash -n "$SCRIPT"; then
    pass "AC-1: bash -n build_linux_rocm.sh exited 0"
  else
    fail "AC-1: bash -n build_linux_rocm.sh exited non-zero"
  fi
}

ac2() {
  require_script
  [ -x "$SCRIPT" ] || fail "AC-2: build_linux_rocm.sh is not executable, so ./build_linux_rocm.sh cannot run"

  # Run from a throwaway directory so a misplaced guard cannot clone or
  # install into the repository, and cap the runtime so a guard that only
  # fires after the torch install is reported as a failure, not a hang.
  timeout_bin=$(command -v timeout || command -v gtimeout) \
    || fail "AC-2: neither timeout nor gtimeout is available"
  workdir=$(mktemp -d)
  trap 'rm -rf "$workdir"' EXIT

  output=$(cd "$workdir" && "$timeout_bin" 60 "$SCRIPT" \
    fa3:e2743ab5b3803bb672b16437ba98a3b1d4576c50 3.12 2.13.0 7.2 2>&1)
  status=$?

  echo "--- exit status: $status"
  echo "--- output ---"
  echo "$output"
  echo "--------------"

  [ "$status" -ne 124 ] || fail "AC-2: timed out after 60s; the FA3 guard must reject before any download"
  [ "$status" -ne 0 ] || fail "AC-2: exited 0, expected non-zero for an fa3: argument"

  echo "$output" | grep -Eiq 'fa3|flash[ -]?attention[ -]?3' \
    || fail "AC-2: output does not mention FA3"
  echo "$output" | grep -Eiq 'rocm' \
    || fail "AC-2: output does not mention ROCm"
  echo "$output" \
    | grep -Eiq 'not[ -]support|unsupport|non-support|not available|cuda[ -]only|非対応|未対応|サポートされ' \
    || fail "AC-2: output does not state that FA3 is unsupported on ROCm"

  pass "AC-2: exited $status and reported FA3 as unsupported on ROCm"
}

ac3() {
  require_script
  count=$(grep -c 'NVCC_APPEND_FLAGS\|NVCC_THREADS' "$SCRIPT")
  echo "--- match count: $count"
  [ "$count" -eq 0 ] \
    || fail "AC-3: found $count line(s) referencing NVCC_APPEND_FLAGS / NVCC_THREADS, expected 0"
  pass "AC-3: build_linux_rocm.sh references no NVCC_APPEND_FLAGS / NVCC_THREADS"
}

# Run the script's ccache block on its own against stub binaries. Building for
# real needs a ROCm toolchain, but the part that decides whether hipcc is
# cached is pure shell, so it can be exercised here.
run_ccache_block() {
  # $1: directory holding the stubs, $2...: extra env assignments
  stubs=$1
  shift
  probe="$stubs/probe.sh"
  sed -n '/^HIPCC_PATH=/,/^fi$/p' "$SCRIPT" > "$probe"
  [ -s "$probe" ] || fail "AC-4: could not find the ccache block in $SCRIPT"
  cat >> "$probe" <<'PROBE'
echo "PYTORCH_NVCC=${PYTORCH_NVCC-<unset>}"
echo "CCACHE_DIR=${CCACHE_DIR-<unset>}"
echo "CCACHE_MAXSIZE=${CCACHE_MAXSIZE-<unset>}"
echo "CCACHE_COMPILERCHECK=${CCACHE_COMPILERCHECK-<unset>}"
PROBE
  env -i HOME="$stubs/home" PATH="$stubs/bin:/usr/bin:/bin" ROCM_HOME="$stubs/rocm" "$@" \
    bash "$probe"
}

ac4() {
  require_script
  stubs=$(mktemp -d)
  trap 'rm -rf "$stubs"' EXIT
  mkdir -p "$stubs/bin" "$stubs/rocm/bin" "$stubs/home"
  printf '#!/bin/sh\necho "ccache version 4.9"\n' > "$stubs/bin/ccache"
  printf '#!/bin/sh\nexit 0\n' > "$stubs/rocm/bin/hipcc"
  chmod +x "$stubs/bin/ccache" "$stubs/rocm/bin/hipcc"

  out=$(run_ccache_block "$stubs")
  echo "--- defaults ---"
  echo "$out"
  echo "$out" | grep -qx "PYTORCH_NVCC=ccache $stubs/rocm/bin/hipcc" \
    || fail "AC-4: PYTORCH_NVCC does not prefix the resolved hipcc with ccache"
  echo "$out" | grep -qx "CCACHE_DIR=$stubs/home/.cache/ccache-rocm" \
    || fail "AC-4: CCACHE_DIR does not default to a ROCm-specific directory"
  echo "$out" | grep -qx "CCACHE_MAXSIZE=20G" \
    || fail "AC-4: CCACHE_MAXSIZE has no bound, so the cache could fill the disk"
  echo "$out" | grep -qx "CCACHE_COMPILERCHECK=content" \
    || fail "AC-4: CCACHE_COMPILERCHECK is not content, so reinstalling ROCm would miss every entry"

  # A caller's own settings must win, so the same cache can be pointed
  # somewhere else outside CI.
  out=$(run_ccache_block "$stubs" CCACHE_DIR=/tmp/elsewhere CCACHE_MAXSIZE=5G)
  echo "--- caller overrides ---"
  echo "$out"
  echo "$out" | grep -qx "CCACHE_DIR=/tmp/elsewhere" \
    || fail "AC-4: CCACHE_DIR set by the caller was overwritten"
  echo "$out" | grep -qx "CCACHE_MAXSIZE=5G" \
    || fail "AC-4: CCACHE_MAXSIZE set by the caller was overwritten"

  # No ccache installed must not be an error: the build just runs uncached.
  rm -f "$stubs/bin/ccache"
  out=$(run_ccache_block "$stubs")
  echo "--- ccache absent ---"
  echo "$out"
  echo "$out" | grep -qx "PYTORCH_NVCC=<unset>" \
    || fail "AC-4: PYTORCH_NVCC was set even though ccache is not installed"

  pass "AC-4: hipcc is routed through a bounded ccache, caller settings win, and a missing ccache is not fatal"
}

case "${1:-}" in
  ac1) ac1 ;;
  ac2) ac2 ;;
  ac3) ac3 ;;
  ac4) ac4 ;;
  *) echo "usage: $0 {ac1|ac2|ac3|ac4}" >&2; exit 2 ;;
esac

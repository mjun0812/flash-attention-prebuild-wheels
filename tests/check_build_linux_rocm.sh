#!/bin/bash
# Acceptance checks for build_linux_rocm.sh (T-001).
#
# Each acceptance criterion is one invocation:
#   tests/check_build_linux_rocm.sh ac1   # syntax is sound
#   tests/check_build_linux_rocm.sh ac2   # FA3 is rejected
#   tests/check_build_linux_rocm.sh ac3   # no CUDA-only env vars
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

case "${1:-}" in
  ac1) ac1 ;;
  ac2) ac2 ;;
  ac3) ac3 ;;
  *) echo "usage: $0 {ac1|ac2|ac3}" >&2; exit 2 ;;
esac

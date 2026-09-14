#!/bin/bash
# Acceptance checks for the ROCm CI wiring (T-002).
#
# Each acceptance criterion is one invocation:
#   tests/check_rocm_ci_wiring.sh ac1   # both workflows pass actionlint
#
# These run without a ROCm toolchain, an AMD GPU, or a GitHub API token.

set -u

REPO_ROOT=$(cd "$(dirname "$0")/.." && pwd)
ROCM_WORKFLOW=".github/workflows/_build_linux_rocm.yml"
TEST_BUILD_WORKFLOW=".github/workflows/test-build.yml"

fail() {
  echo "FAIL: $*"
  exit 1
}

pass() {
  echo "PASS: $*"
  exit 0
}

ac1() {
  command -v actionlint >/dev/null 2>&1 || fail "AC-1: actionlint is not installed"

  cd "$REPO_ROOT" || fail "AC-1: cannot cd to $REPO_ROOT"

  output=$(actionlint -shellcheck= "$ROCM_WORKFLOW" "$TEST_BUILD_WORKFLOW" 2>&1)
  status=$?

  echo "--- exit status: $status"
  echo "--- output ---"
  echo "$output"
  echo "--------------"

  [ "$status" -eq 0 ] \
    || fail "AC-1: actionlint -shellcheck= $ROCM_WORKFLOW $TEST_BUILD_WORKFLOW exited $status, expected 0"

  pass "AC-1: actionlint -shellcheck= reported no problem in $ROCM_WORKFLOW and $TEST_BUILD_WORKFLOW"
}

case "${1:-}" in
  ac1) ac1 ;;
  *) echo "usage: $0 {ac1}" >&2; exit 2 ;;
esac

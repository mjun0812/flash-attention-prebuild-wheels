#!/bin/bash
# Acceptance checks for the ROCm CI wiring (T-002).
#
# Each acceptance criterion is one invocation:
#   tests/check_rocm_ci_wiring.sh ac1   # both workflows pass actionlint
#   tests/check_rocm_ci_wiring.sh ac2   # no forbidden path was touched
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

ac2() {
  cd "$REPO_ROOT" || fail "AC-2: cannot cd to $REPO_ROOT"

  git rev-parse --verify --quiet origin/main >/dev/null \
    || fail "AC-2: origin/main is not available in this clone"

  changed=$(git diff --name-only origin/main)
  status=$?
  [ "$status" -eq 0 ] || fail "AC-2: git diff --name-only origin/main exited $status"

  echo "--- changed files vs origin/main ---"
  echo "$changed"
  echo "------------------------------------"

  # Paths the spec puts under "Does Not Own". Exact file names plus the two
  # directory prefixes; matching is done per line so a substring such as
  # build_linux_rocm.sh is never confused with build_linux.sh.
  violations=""
  while IFS= read -r path; do
    [ -n "$path" ] || continue
    case "$path" in
      build_linux.sh | build_windows.ps1 | create_matrix.py | .github/workflows/build.yml)
        violations="$violations $path"
        ;;
      scripts/* | patches/*)
        violations="$violations $path"
        ;;
    esac
  done <<EOF
$changed
EOF

  [ -z "$violations" ] \
    || fail "AC-2: forbidden path(s) changed vs origin/main:$violations"

  pass "AC-2: no forbidden path (build_linux.sh, build_windows.ps1, create_matrix.py, scripts/, patches/, .github/workflows/build.yml) changed vs origin/main"
}

case "${1:-}" in
  ac1) ac1 ;;
  ac2) ac2 ;;
  *) echo "usage: $0 {ac1|ac2}" >&2; exit 2 ;;
esac

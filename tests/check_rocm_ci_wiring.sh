#!/bin/bash
# Acceptance checks for the ROCm CI wiring (T-002).
#
# Each acceptance criterion is one invocation:
#   tests/check_rocm_ci_wiring.sh ac1   # both workflows pass actionlint
#   tests/check_rocm_ci_wiring.sh ac2   # the build is capped and its cache travels with the run
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

  # The job's GITHUB_TOKEN dies 24h after the job starts, so the cap has to be
  # measured from the job rather than from the build.
  grep -q 'BUILD_JOB_STARTED_AT=\$(date +%s)' "$ROCM_WORKFLOW" \
    || fail "AC-2: the job start time is never recorded, so the cap cannot be relative to it"
  grep -q 'timeout --signal=TERM' "$ROCM_WORKFLOW" \
    || fail "AC-2: the build is not capped, so it can outlive its token"
  grep -q 'BUILD_JOB_STARTED_AT + BUILD_TIMEOUT_MINUTES \* 60' "$ROCM_WORKFLOW" \
    || fail "AC-2: the deadline is not derived from the job start time"

  # The two self-hosted runners share one label, so a re-run lands on either
  # of them. The cache has to travel with the run rather than sit on the disk
  # of whichever machine happened to build first.
  grep -q 'actions/cache/restore@v4' "$ROCM_WORKFLOW" \
    || fail "AC-2: the cache is never restored, so a re-run on the other runner starts from nothing"
  grep -q 'actions/cache/save@v4' "$ROCM_WORKFLOW" \
    || fail "AC-2: the cache is never saved, so a capped build leaves nothing behind"
  grep -q "steps.build.outputs.capped == 'true'" "$ROCM_WORKFLOW" \
    || fail "AC-2: the cache is saved unconditionally instead of only for a capped build"
  grep -q 'github.run_id' "$ROCM_WORKFLOW" \
    || fail "AC-2: the cache key is not tied to the run, so attempts of different runs would share it"

  pass "AC-2: the build is capped from job start and its cache travels with the run"
}

case "${1:-}" in
  ac1) ac1 ;;
  ac2) ac2 ;;
  *) echo "usage: $0 {ac1|ac2}" >&2; exit 2 ;;
esac

"""Run a command with a deadline, like coreutils timeout(1), but Windows-aware.

GitHub-hosted Windows runners have no `timeout --signal=TERM`, and stopping a
build there means stopping a whole process tree (pwsh -> python -> ninja ->
cl/nvcc); killing only the direct child leaves compilers running. On expiry
this script:

1. Sends CTRL_BREAK_EVENT to the child's process group (Windows) or SIGTERM
   (POSIX) so ninja can finish writing its logs.
2. Waits a grace period.
3. Falls back to `taskkill /T /F` (Windows) or SIGKILL (POSIX).

Exits with 124 on timeout (same convention as timeout(1)) so the caller's
capped-build detection works identically on Linux and Windows.

Usage:
    python run_with_timeout.py --deadline-epoch 1750000000 -- cmd arg1 arg2
"""

from __future__ import annotations

import argparse
import os
import signal
import subprocess
import sys
import time

TIMEOUT_EXIT_CODE = 124


def stop_process_tree(proc: subprocess.Popen, grace_seconds: int) -> None:
    """Stop ``proc`` and its descendants, gently first, then forcefully.

    Args:
        proc: The child process (created in its own process group / session).
        grace_seconds: Seconds to wait after the gentle signal before the
            forceful kill.
    """
    if sys.platform == "win32":
        # Reaches every process in the child's console process group.
        proc.send_signal(signal.CTRL_BREAK_EVENT)
    else:
        os.killpg(proc.pid, signal.SIGTERM)
    try:
        proc.wait(timeout=grace_seconds)
        return
    except subprocess.TimeoutExpired:
        pass
    print(
        f"run-with-timeout: process tree still alive after {grace_seconds}s grace; killing",
        file=sys.stderr,
    )
    if sys.platform == "win32":
        subprocess.run(
            ["taskkill", "/PID", str(proc.pid), "/T", "/F"],
            capture_output=True,
            check=False,
        )
    else:
        os.killpg(proc.pid, signal.SIGKILL)
    proc.wait()


def main() -> int:
    """Run the wrapped command under a deadline; entry point for CLI use."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--deadline-epoch",
        type=int,
        required=True,
        help="Unix epoch seconds at which the command is stopped",
    )
    parser.add_argument(
        "--grace-seconds",
        type=int,
        default=30,
        help="Wait this long after the gentle stop before the forceful kill",
    )
    parser.add_argument(
        "command",
        nargs=argparse.REMAINDER,
        help="Command to run (prefix with -- to separate from options)",
    )
    args = parser.parse_args()
    command = args.command
    if command and command[0] == "--":
        command = command[1:]
    if not command:
        parser.error("no command given")

    remaining = args.deadline_epoch - int(time.time())
    if remaining <= 0:
        print(
            f"run-with-timeout: deadline already passed ({-remaining}s ago); not starting",
            file=sys.stderr,
        )
        return TIMEOUT_EXIT_CODE

    print(f"run-with-timeout: deadline in {remaining}s")
    creationflags = (
        subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == "win32" else 0
    )
    start_new_session = sys.platform != "win32"
    proc = subprocess.Popen(
        command,
        creationflags=creationflags,
        start_new_session=start_new_session,
    )
    try:
        return proc.wait(timeout=remaining)
    except subprocess.TimeoutExpired:
        print(
            f"run-with-timeout: deadline reached after {remaining}s; stopping process tree",
            file=sys.stderr,
        )
        stop_process_tree(proc, args.grace_seconds)
        return TIMEOUT_EXIT_CODE
    except KeyboardInterrupt:
        stop_process_tree(proc, args.grace_seconds)
        raise


if __name__ == "__main__":
    sys.exit(main())

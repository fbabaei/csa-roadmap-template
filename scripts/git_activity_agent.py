#!/usr/bin/env python3
"""Monitor local git changes and assist with confirmed commit/push workflow.

This script watches the repository for working-tree changes. When changes are
found, it prompts for confirmation before committing and before pushing.

Default push targets:
- public remote: origin
- private remote: personal

Usage:
  python scripts/git_activity_agent.py
  python scripts/git_activity_agent.py --interval 30
  python scripts/git_activity_agent.py --public-remote origin --private-remote personal
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def run_git(args: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=check,
    )


def get_current_branch() -> str:
    result = run_git(["branch", "--show-current"])
    branch = result.stdout.strip()
    if not branch:
        raise RuntimeError("Unable to determine current branch.")
    return branch


def get_status_lines() -> list[str]:
    result = run_git(["status", "--porcelain"])
    return [line for line in result.stdout.splitlines() if line.strip()]


def summarize_status(lines: list[str]) -> str:
    tracked = 0
    untracked = 0
    for line in lines:
        if line.startswith("??"):
            untracked += 1
        else:
            tracked += 1
    return f"{tracked} tracked changes, {untracked} untracked files"


def prompt_yes_no(message: str, default_no: bool = True) -> bool:
    suffix = "[y/N]" if default_no else "[Y/n]"
    answer = input(f"{message} {suffix} ").strip().lower()
    if not answer:
        return not default_no
    return answer in {"y", "yes"}


def ensure_remote_exists(name: str) -> bool:
    result = run_git(["remote"], check=False)
    if result.returncode != 0:
        return False
    return name in {line.strip() for line in result.stdout.splitlines() if line.strip()}


def commit_changes() -> bool:
    run_git(["add", "-A"])
    message = input("Commit message: ").strip()
    if not message:
        print("Commit cancelled: message is required.")
        return False

    result = run_git(["commit", "-m", message], check=False)
    if result.returncode != 0:
        # Most common case: nothing to commit after a race/change resolution.
        stderr = (result.stderr or "").strip()
        stdout = (result.stdout or "").strip()
        print("Commit did not complete.")
        if stdout:
            print(stdout)
        if stderr:
            print(stderr)
        return False

    print((result.stdout or "").strip())
    return True


def push_to_remote(remote: str, branch: str) -> bool:
    result = run_git(["push", remote, branch], check=False)
    if result.returncode == 0:
        print((result.stdout or "").strip())
        return True

    print(f"Push failed for remote '{remote}'.")
    if result.stdout.strip():
        print(result.stdout.strip())
    if result.stderr.strip():
        print(result.stderr.strip())
    return False


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Monitor git changes and confirm commit/push actions.",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=20,
        help="Polling interval in seconds (default: 20)",
    )
    parser.add_argument(
        "--public-remote",
        default="origin",
        help="Remote name for public repository (default: origin)",
    )
    parser.add_argument(
        "--private-remote",
        default="personal",
        help="Remote name for private repository (default: personal)",
    )
    return parser.parse_args()


def print_header(branch: str, public_remote: str, private_remote: str, interval: int) -> None:
    print("=" * 72)
    print("Git Activity Agent")
    print("=" * 72)
    print(f"Repository : {ROOT}")
    print(f"Branch     : {branch}")
    print(f"Public     : {public_remote}")
    print(f"Private    : {private_remote}")
    print(f"Interval   : {interval}s")
    print()
    print("Behavior:")
    print("1. Watches working tree changes.")
    print("2. Asks you before commit.")
    print("3. Asks you before pushing to both remotes.")
    print("4. Keeps running until Ctrl+C.")
    print("=" * 72)


def main() -> int:
    args = parse_args()

    try:
        branch = get_current_branch()
    except Exception as exc:
        print(f"ERROR: {exc}")
        return 1

    for remote in (args.public_remote, args.private_remote):
        if not ensure_remote_exists(remote):
            print(f"ERROR: Remote not found: {remote}")
            print("Run 'git remote -v' to inspect configured remotes.")
            return 1

    print_header(branch, args.public_remote, args.private_remote, args.interval)

    last_signature = ""

    try:
        while True:
            lines = get_status_lines()
            signature = "\n".join(lines)

            if not lines:
                if last_signature:
                    print("Working tree is clean.")
                    last_signature = ""
                time.sleep(args.interval)
                continue

            if signature == last_signature:
                time.sleep(args.interval)
                continue

            last_signature = signature
            print("\nDetected changes:")
            print(summarize_status(lines))
            for line in lines[:20]:
                print(f"- {line}")
            if len(lines) > 20:
                print(f"- ... and {len(lines) - 20} more")

            if not prompt_yes_no("Create a commit for these changes now?"):
                print("Skipped commit for now. Monitoring continues.")
                time.sleep(args.interval)
                continue

            if not commit_changes():
                time.sleep(args.interval)
                continue

            # Branch may have changed due to user actions.
            branch = get_current_branch()

            if not prompt_yes_no(
                f"Push branch '{branch}' to both '{args.public_remote}' and '{args.private_remote}' now?"
            ):
                print("Commit created. Push skipped by user.")
                time.sleep(args.interval)
                continue

            ok_public = push_to_remote(args.public_remote, branch)
            ok_private = push_to_remote(args.private_remote, branch)

            if ok_public and ok_private:
                print("Push succeeded to both remotes.")
            elif ok_public:
                print("Public push succeeded; private push failed.")
            elif ok_private:
                print("Private push succeeded; public push failed.")
            else:
                print("Push failed on both remotes.")

            time.sleep(args.interval)

    except KeyboardInterrupt:
        print("\nAgent stopped by user.")
        return 0


if __name__ == "__main__":
    sys.exit(main())

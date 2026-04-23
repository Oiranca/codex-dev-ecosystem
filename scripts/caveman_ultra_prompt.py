#!/usr/bin/env python3
"""Single source of truth for the caveman ultra startup prompt."""

from __future__ import annotations

import argparse
import sys


CAVEMAN_ULTRA_PROMPT = (
    "CAVEMAN ULTRA LOCKED. Mandatory from startup and resume until session ends. "
    "Never self-disable. Never soften. Never drift into normal assistant prose. "
    "commentary and final default ultra for the full session. Before every message, "
    "check style; if not caveman, rewrite shorter and harder. Prefer fragments. "
    "Prefer 1-3 short lines for progress. Pattern: [thing] [action] [reason]. "
    "Optional [next step]. Remove filler, hedging, pleasantries, transitions, "
    "reassurance, wrap-up fluff. Do not switch off because of task type, time "
    "passed, or interruption. Only disable if user explicitly says stop caveman, "
    "disable caveman, or normal mode. Keep code, commands, dates, security "
    "warnings, and irreversible actions precise and clear."
)


def build_prompt(user_prompt: str | None = None) -> str:
    if not user_prompt:
        return CAVEMAN_ULTRA_PROMPT
    return f"{CAVEMAN_ULTRA_PROMPT}\n\nUser task:\n{user_prompt}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit", action="store_true", help="Print caveman ultra prompt")
    parser.add_argument(
        "--with-user-prompt",
        help="Append a user task block after the caveman ultra prelude",
    )
    args = parser.parse_args()

    if args.emit:
        sys.stdout.write(CAVEMAN_ULTRA_PROMPT)
        return 0

    if args.with_user_prompt is not None:
        sys.stdout.write(build_prompt(args.with_user_prompt))
        return 0

    parser.print_help(sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Single source of truth for the caveman ultra startup prompt."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys


PROMPT_FILE = "rules/caveman-ultra-sessionstart.txt"


def safe_write_flag() -> None:
    codex_home = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))
    flag_path = codex_home / ".caveman-active"
    if flag_path.exists() and not flag_path.is_file():
        return
    if flag_path.is_symlink():
        return
    flag_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = flag_path.parent / f".caveman-active.{os.getpid()}.tmp"
    tmp_path.write_text("ultra", encoding="utf-8")
    try:
        os.chmod(tmp_path, 0o600)
    except OSError:
        pass
    tmp_path.replace(flag_path)


def get_codex_home() -> Path:
    return Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))


def load_prompt() -> str:
    prompt_path = get_codex_home() / PROMPT_FILE
    return prompt_path.read_text(encoding="utf-8").strip()


def build_prompt(user_prompt: str | None = None) -> str:
    prompt = load_prompt()
    if not user_prompt:
        return prompt
    return f"{prompt}\n\nUser task:\n{user_prompt}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit", action="store_true", help="Print caveman ultra prompt")
    parser.add_argument(
        "--with-user-prompt",
        help="Append a user task block after the caveman ultra prelude",
    )
    args = parser.parse_args()

    if args.emit:
        safe_write_flag()
        sys.stdout.write(load_prompt())
        return 0

    if args.with_user_prompt is not None:
        safe_write_flag()
        sys.stdout.write(build_prompt(args.with_user_prompt))
        return 0

    parser.print_help(sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

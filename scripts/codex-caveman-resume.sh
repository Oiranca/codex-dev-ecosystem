#!/usr/bin/env bash
set -euo pipefail

CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
PROMPT_SCRIPT="$CODEX_HOME/scripts/caveman_ultra_prompt.py"

resume_args=()
task_parts=()
after_delim=0

for arg in "$@"; do
  if [ "$after_delim" -eq 1 ]; then
    task_parts+=("$arg")
    continue
  fi
  if [ "$arg" = "--" ]; then
    after_delim=1
    continue
  fi
  resume_args+=("$arg")
done

if [ "${#task_parts[@]}" -gt 0 ]; then
  task="${task_parts[*]}"
  prompt="$(python3 "$PROMPT_SCRIPT" --with-user-prompt "$task")"
  exec codex resume "${resume_args[@]}" "$prompt"
fi

prompt="$(python3 "$PROMPT_SCRIPT" --emit)"
exec codex resume "${resume_args[@]}" "$prompt"

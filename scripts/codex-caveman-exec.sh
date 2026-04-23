#!/usr/bin/env bash
set -euo pipefail

CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
PROMPT_SCRIPT="$CODEX_HOME/scripts/caveman_ultra_prompt.py"

exec_args=()
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
  exec_args+=("$arg")
done

if [ "${#task_parts[@]}" -gt 0 ]; then
  task="${task_parts[*]}"
  prompt="$(python3 "$PROMPT_SCRIPT" --with-user-prompt "$task")"
  if [ "${#exec_args[@]}" -gt 0 ]; then
    exec codex exec "${exec_args[@]}" "$prompt"
  else
    exec codex exec "$prompt"
  fi
fi

prompt="$(python3 "$PROMPT_SCRIPT" --emit)"
if [ "${#exec_args[@]}" -gt 0 ]; then
  exec codex exec "${exec_args[@]}" "$prompt"
else
  exec codex exec "$prompt"
fi

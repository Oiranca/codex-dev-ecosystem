#!/bin/bash
set -euo pipefail

CODEX_HOME="${HOME}/.codex"
KEEP_DAYS_SESSIONS=14
KEEP_DAYS_SNAPSHOTS=14
KEEP_DAYS_TMP=2
KEEP_DAYS_LOCKS=1
MAX_TUI_LOG_BYTES=1048576

delete_old_files() {
  local target="$1"
  local days="$2"

  [ -d "$target" ] || return 0
  find "$target" -type f -mtime +"$days" -delete 2>/dev/null || true
  find "$target" -type d -empty -delete 2>/dev/null || true
}

delete_old_files "${CODEX_HOME}/sessions" "${KEEP_DAYS_SESSIONS}"
delete_old_files "${CODEX_HOME}/shell_snapshots" "${KEEP_DAYS_SNAPSHOTS}"
delete_old_files "${CODEX_HOME}/.tmp" "${KEEP_DAYS_TMP}"

[ -d "${CODEX_HOME}/tmp/playwright-mcp" ] && find "${CODEX_HOME}/tmp/playwright-mcp" -type f -mtime +"${KEEP_DAYS_TMP}" -delete 2>/dev/null || true
[ -d "${CODEX_HOME}/tmp/arg0" ] && find "${CODEX_HOME}/tmp/arg0" -type f -name '.lock' -mtime +"${KEEP_DAYS_LOCKS}" -delete 2>/dev/null || true
find "${CODEX_HOME}/tmp" -type d -empty -delete 2>/dev/null || true

TUI_LOG="${CODEX_HOME}/log/codex-tui.log"
if [ -f "$TUI_LOG" ]; then
  log_size=$(wc -c < "$TUI_LOG" | tr -d ' ')
  if [ "${log_size:-0}" -gt "$MAX_TUI_LOG_BYTES" ]; then
    tmp_file="$(mktemp "${CODEX_HOME}/log/codex-tui.XXXXXX")"
    tail -c "$MAX_TUI_LOG_BYTES" "$TUI_LOG" > "$tmp_file"
    mv "$tmp_file" "$TUI_LOG"
  fi
fi

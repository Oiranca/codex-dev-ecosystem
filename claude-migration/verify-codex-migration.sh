#!/usr/bin/env bash
set -euo pipefail

CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
SKILLS_DIR="$CODEX_HOME/skills"
MIGRATED="$(find "$SKILLS_DIR" -mindepth 2 -maxdepth 2 -name SKILL.md -not -path '*/.system/*' | wc -l | tr -d ' ')"

fail() { echo "[FAIL] $1"; exit 1; }
pass() { echo "[OK] $1"; }

# 1) expected migrated count
[ "$MIGRATED" -ge 30 ] || fail "Unexpected migrated skill count: $MIGRATED"
pass "Migrated skill count: $MIGRATED"

# 2) frontmatter + required keys
while IFS= read -r f; do
  c=$(sed -n '1,80p' "$f" | rg '^---$' | wc -l | tr -d ' ')
  [ "$c" -eq 2 ] || fail "Invalid frontmatter delimiters in $f"
  sed -n '1,40p' "$f" | rg -q '^name:' || fail "Missing name in $f"
  sed -n '1,40p' "$f" | rg -q '^description:' || fail "Missing description in $f"
done < <(find "$SKILLS_DIR" -mindepth 2 -maxdepth 2 -name SKILL.md -not -path '*/.system/*')
pass "Frontmatter and required fields"

# 3) disallow legacy hard dependencies
BANNED='\\.claude|~/.claude|Task State Engine|shared task list|teammate|agent-runtime\\.py|message inbox|message send|task claim|task update|task complete|task list|timeline append|\\.agent-cache|local metadata cache/locks/'
if rg -n "$BANNED" "$SKILLS_DIR" -g 'SKILL.md' >/tmp/codex-migration-banned.txt 2>/dev/null; then
  cat /tmp/codex-migration-banned.txt
  fail "Legacy references still present"
fi
pass "No legacy hard dependencies in skills"

# 4) native note present on migrated skills
while IFS= read -r f; do
  rg -q '^## Codex Native Note$' "$f" || fail "Missing Codex Native Note in $f"
done < <(find "$SKILLS_DIR" -mindepth 2 -maxdepth 2 -name SKILL.md -not -path '*/.system/*')
pass "Codex Native Note present"

# 5) script syntax
bash -n "$CODEX_HOME/scripts/pre-edit-check.sh" || fail "Syntax error in pre-edit-check.sh"
bash -n "$CODEX_HOME/scripts/validate-local.sh" || fail "Syntax error in validate-local.sh"
bash -n "$CODEX_HOME/scripts/claude-compat/pre-edit-check.sh" || fail "Syntax error in compat pre-edit-check.sh"
bash -n "$CODEX_HOME/scripts/claude-compat/validate-local.sh" || fail "Syntax error in compat validate-local.sh"
PYTHONPYCACHEPREFIX=/tmp/python-cache python3 -m py_compile "$CODEX_HOME/scripts/agent-runtime.py" || fail "Python compile error in agent-runtime.py"
PYTHONPYCACHEPREFIX=/tmp/python-cache python3 -m py_compile "$CODEX_HOME/scripts/claude-compat/agent-runtime.py" || fail "Python compile error in compat agent-runtime.py"
pass "Scripts compile/syntax checks"

echo "All checks passed. Migration is Codex-compatible."

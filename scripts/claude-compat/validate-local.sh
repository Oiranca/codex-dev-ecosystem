#!/usr/bin/env bash
# Ubicación recomendada: ~/.codex/scripts/validate-local.sh
set -euo pipefail

# Notificaciones nativas según OS
notify() {
  local message="$1"
  local title="Codex Agent Team"
  if [[ "${AGENT_SILENT_MODE:-false}" != "true" ]]; then
    case "$OSTYPE" in
      darwin*)
        osascript -e "display notification \"$message\" with title \"$title\" sound name \"Submarine\"" ;;
      linux*)
        if command -v notify-send &>/dev/null; then notify-send "$title" "$message" -i utilities-terminal; fi ;;
    esac
  fi
}

DOCS_DIR="docs"
CACHE_DIR=".agent-cache"
DECISIONS_FILE="$DOCS_DIR/DECISIONS.md"
LAST_RUN_DIR="$CACHE_DIR/last-run"
TIMESTAMP="$(date -u '+%Y-%m-%d %H:%M')"

mkdir -p "$DOCS_DIR" "$LAST_RUN_DIR"

# Detectar Gestor de Paquetes
detect_pkg_manager() {
  if [ -f "yarn.lock" ]; then echo "yarn";
  elif [ -f "pnpm-lock.yaml" ]; then echo "pnpm";
  elif [ -f "bun.lockb" ] || [ -f "bun.lock" ]; then echo "bun";
  else echo "npm"; fi
}

# Ejecución de pasos: lint -> typecheck -> test -> build
PKG_MGR="$(detect_pkg_manager)"
VALIDATE_LOG="$LAST_RUN_DIR/validate.log"
: > "$VALIDATE_LOG"
FAILED=false
FAILED_STEP=""

# Lógica de validación por pasos
for step in lint typecheck test build; do
  # Comprobar si el script existe en package.json usando python3
  HAS_STEP=$(python3 -c "import json, os; print('yes' if os.path.exists('package.json') and '$step' in json.load(open('package.json')).get('scripts', {}) else 'no')" 2>/dev/null || echo "no")
  
  if [ "$HAS_STEP" = "yes" ]; then
    echo "[ROLE: QA] Running $step..." | tee -a "$VALIDATE_LOG"
    if ! $PKG_MGR run "$step" 2>&1 | tee -a "$VALIDATE_LOG"; then
      FAILED=true
      FAILED_STEP="$step"
      break
    fi
  fi
done

if [ "$FAILED" = true ]; then
  # Generar resumen de fallo para el equipo de agentes
  {
    echo "# Failure Summary"
    echo "**Failed step:** \`$FAILED_STEP\` | **Timestamp:** $TIMESTAMP"
    echo "## Last 160 lines of output"
    echo '```'
    tail -n 160 "$VALIDATE_LOG"
    echo '```'
  } > "$LAST_RUN_DIR/failure_summary.md"
  
  echo "- [$TIMESTAMP] QA: validation FAILED at \`$FAILED_STEP\`." >> "$DECISIONS_FILE"
  notify "VALIDATION FAILED at $FAILED_STEP"
  exit 1
fi

echo "- [$TIMESTAMP] QA: validation passed." >> "$DECISIONS_FILE"
notify "Validation passed"
exit 0
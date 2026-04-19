#!/usr/bin/env python3

import json
from datetime import datetime, timezone
from pathlib import Path
import sys


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        payload = {}

    event = payload.get("hook_event_name", "unknown")
    session_id = payload.get("session_id", "unknown")
    cwd = payload.get("cwd", "")
    model = payload.get("model", "")

    log_dir = Path.home() / ".codex" / "log"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "caveman-sessionstart.log"

    # SessionStart matcher emits startup or resume. Record both for resume diagnostics.
    source = payload.get("source") or payload.get("event") or "unknown"
    timestamp = datetime.now(timezone.utc).isoformat()
    line = (
        f"{timestamp} event={event} source={source} "
        f"session_id={session_id} model={model} cwd={cwd}\n"
    )
    log_file.open("a", encoding="utf-8").write(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

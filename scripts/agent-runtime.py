#!/usr/bin/env python3
"""
Codex Agent Ecosystem v2 — Agent Runtime

Provides the Task State Engine, agent messaging, distributed locks,
and timeline for parallel multi-agent coordination.

This script is an optional local compatibility helper.
Native Codex coordination should prefer spawn_agent/send_input/current-thread handoff.

Usage:
  python agent-runtime.py task create --title "..." --owner agent [options]
  python agent-runtime.py task list [--status pending] [--owner agent]
  python agent-runtime.py task claim --id <id> --owner <agent>
  python agent-runtime.py task update --id <id> --status running [--outputs "..."]
  python agent-runtime.py task complete --id <id> [--outputs "..."]
  python agent-runtime.py task fail --id <id> --reason "..."
  python agent-runtime.py message send --from <a> --to <b> --task-id <id> --type handoff --summary "..."
  python agent-runtime.py message inbox --agent <agent> [--unread]
  python agent-runtime.py message mark-read --agent <agent>
  python agent-runtime.py lock acquire --name <name> --owner <agent> [--ttl 1800]
  python agent-runtime.py lock release --name <name>
  python agent-runtime.py lock status [--name <name>]
  python agent-runtime.py timeline append --event "..."
"""

import argparse
import fcntl
import json
import os
import re
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Union

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

CACHE_DIR = Path(".agent-cache")
TASKS_FILE = CACHE_DIR / "tasks.json"
MESSAGES_FILE = CACHE_DIR / "messages.jsonl"
TIMELINE_FILE = CACHE_DIR / "timeline.log"
LOCKS_DIR = CACHE_DIR / "locks"

# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

VALID_TASK_STATES = {"pending", "claimed", "running", "blocked", "review", "done", "failed"}

VALID_MESSAGE_TYPES = {
    "assignment",
    "handoff",
    "question",
    "review_request",
    "review_result",
    "blocked",
    "done",
}

DEFAULT_LOCK_TTL = 1800  # 30 minutes in seconds

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_id() -> str:
    return str(uuid.uuid4())[:8]


def init_cache():
    """Ensure .agent-cache directory structure exists."""
    CACHE_DIR.mkdir(exist_ok=True)
    LOCKS_DIR.mkdir(exist_ok=True)
    if not TASKS_FILE.exists():
        TASKS_FILE.write_text("[]")
    if not MESSAGES_FILE.exists():
        MESSAGES_FILE.write_text("")
    if not TIMELINE_FILE.exists():
        TIMELINE_FILE.write_text("")


def die(msg: str, code: int = 1):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


def _validate_lock_name(name: str):
    """Reject lock names that could escape LOCKS_DIR via path traversal."""
    if not re.match(r"^[A-Za-z0-9_.-]+$", name) or ".." in name:
        die(
            f"Invalid lock name '{name}'. "
            "Use only letters, digits, underscores, hyphens, and dots."
        )


# ---------------------------------------------------------------------------
# Concurrency-safe file I/O
# ---------------------------------------------------------------------------


def _io_lock_path(path: Path) -> Path:
    """Companion lock file used to synchronize JSON reads and writes.

    Kept separate from LOCKS_DIR distributed locks (which use *.lock inside
    that subdirectory) to avoid any naming collision.
    """
    return path.parent / (path.name + ".lk")


def _read_json_locked(path: Path) -> Union[list, dict]:
    """Read JSON file with shared (read) lock via companion lock file."""
    with open(_io_lock_path(path), "a+") as lf:
        fcntl.flock(lf, fcntl.LOCK_SH)
        try:
            with open(path, "r") as f:
                return json.load(f)
        finally:
            fcntl.flock(lf, fcntl.LOCK_UN)


def _write_json_locked(path: Path, data: Union[list, dict]):
    """Write JSON file atomically with exclusive lock via companion lock file.

    The companion lock file is held for the entire write + rename cycle so that
    concurrent readers/writers all contend on the same lock rather than each
    locking their own temp file.
    """
    tmp = path.with_name(path.name + f".{uuid.uuid4().hex[:8]}.tmp")
    with open(_io_lock_path(path), "a+") as lf:
        fcntl.flock(lf, fcntl.LOCK_EX)
        try:
            with open(tmp, "w") as f:
                json.dump(data, f, indent=2)
            tmp.replace(path)
        finally:
            fcntl.flock(lf, fcntl.LOCK_UN)


def _append_line_locked(path: Path, line: str):
    """Append a line to a file with exclusive lock."""
    with open(path, "a") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        try:
            f.write(line + "\n")
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)


# ---------------------------------------------------------------------------
# Task commands
# ---------------------------------------------------------------------------


def task_create(args):
    depends = [d.strip() for d in args.depends_on.split(",")] if args.depends_on else []
    task = {
        "id": new_id(),
        "title": args.title,
        "owner": args.owner,
        "status": "pending",
        "priority": args.priority or "medium",
        "depends_on": depends,
        "inputs": args.inputs or "",
        "outputs": "",
        "reviewer": args.reviewer or "",
        "created_at": now_iso(),
        "updated_at": now_iso(),
    }
    tasks = _read_json_locked(TASKS_FILE)
    tasks.append(task)
    _write_json_locked(TASKS_FILE, tasks)
    _timeline_write(f"task.created id={task['id']} title={task['title']!r} owner={task['owner']}")
    print(json.dumps(task, indent=2))


def task_list(args):
    tasks = _read_json_locked(TASKS_FILE)
    if args.status:
        tasks = [t for t in tasks if t["status"] == args.status]
    if args.owner:
        tasks = [t for t in tasks if t["owner"] == args.owner]
    print(json.dumps(tasks, indent=2))


def task_claim(args):
    tasks = _read_json_locked(TASKS_FILE)
    for t in tasks:
        if t["id"] == args.id:
            if t["status"] not in ("pending",):
                die(f"Task {args.id} is in state '{t['status']}', cannot claim.")
            # Check that all dependencies are done
            dep_ids = t.get("depends_on", [])
            if dep_ids:
                done_ids = {x["id"] for x in tasks if x["status"] == "done"}
                blocked = [d for d in dep_ids if d not in done_ids]
                if blocked:
                    die(f"Task {args.id} is blocked by unresolved deps: {blocked}")
            t["status"] = "claimed"
            t["owner"] = args.owner
            t["updated_at"] = now_iso()
            _write_json_locked(TASKS_FILE, tasks)
            _timeline_write(f"task.claimed id={t['id']} owner={args.owner}")
            print(json.dumps(t, indent=2))
            return
    die(f"Task {args.id} not found.")


def task_update(args):
    tasks = _read_json_locked(TASKS_FILE)
    for t in tasks:
        if t["id"] == args.id:
            if args.status:
                if args.status not in VALID_TASK_STATES:
                    die(f"Invalid status '{args.status}'. Valid: {sorted(VALID_TASK_STATES)}")
                t["status"] = args.status
            if args.outputs:
                t["outputs"] = args.outputs
            if args.reviewer:
                t["reviewer"] = args.reviewer
            t["updated_at"] = now_iso()
            _write_json_locked(TASKS_FILE, tasks)
            _timeline_write(f"task.updated id={t['id']} status={t['status']}")
            print(json.dumps(t, indent=2))
            return
    die(f"Task {args.id} not found.")


def task_complete(args):
    tasks = _read_json_locked(TASKS_FILE)
    for t in tasks:
        if t["id"] == args.id:
            t["status"] = "done"
            if args.outputs:
                t["outputs"] = args.outputs
            t["updated_at"] = now_iso()
            _write_json_locked(TASKS_FILE, tasks)
            _timeline_write(f"task.done id={t['id']} owner={t['owner']}")
            print(json.dumps(t, indent=2))
            return
    die(f"Task {args.id} not found.")


def task_fail(args):
    tasks = _read_json_locked(TASKS_FILE)
    for t in tasks:
        if t["id"] == args.id:
            t["status"] = "failed"
            t["outputs"] = args.reason or ""
            t["updated_at"] = now_iso()
            _write_json_locked(TASKS_FILE, tasks)
            _timeline_write(f"task.failed id={t['id']} reason={args.reason!r}")
            print(json.dumps(t, indent=2))
            return
    die(f"Task {args.id} not found.")


# ---------------------------------------------------------------------------
# Message commands
# ---------------------------------------------------------------------------


def message_send(args):
    if args.type not in VALID_MESSAGE_TYPES:
        die(f"Invalid message type '{args.type}'. Valid: {sorted(VALID_MESSAGE_TYPES)}")
    msg = {
        "id": new_id(),
        "from": args.from_agent,
        "to": args.to_agent,
        "task_id": args.task_id or "",
        "type": args.type,
        "summary": args.summary,
        "files": [f.strip() for f in args.files.split(",")] if args.files else [],
        "needs_reply": args.needs_reply,
        "read": False,
        "created_at": now_iso(),
    }
    _append_line_locked(MESSAGES_FILE, json.dumps(msg))
    _timeline_write(
        f"message.sent id={msg['id']} from={msg['from']} to={msg['to']} type={msg['type']}"
    )
    print(json.dumps(msg, indent=2))


def message_inbox(args):
    if not MESSAGES_FILE.exists():
        print("[]")
        return

    raw_lines = MESSAGES_FILE.read_text().splitlines(keepends=True)
    msgs = []
    updated_lines = []
    dirty = False

    for line in raw_lines:
        stripped = line.strip()
        if not stripped:
            updated_lines.append(line)
            continue
        try:
            m = json.loads(stripped)
            if m.get("to") == args.agent:
                if args.unread and m.get("read"):
                    updated_lines.append(line)
                    continue
                msgs.append(m)
                if args.unread and not m.get("read"):
                    m["read"] = True
                    updated_lines.append(json.dumps(m) + "\n")
                    dirty = True
                else:
                    updated_lines.append(line)
            else:
                updated_lines.append(line)
        except json.JSONDecodeError:
            updated_lines.append(line)
            continue

    if dirty:
        # Rewrite file with read messages marked — use exclusive lock for safety
        with open(MESSAGES_FILE, "w") as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            try:
                f.writelines(updated_lines)
            finally:
                fcntl.flock(f, fcntl.LOCK_UN)

    print(json.dumps(msgs, indent=2))


def message_mark_read(args):
    """Mark all messages addressed to --agent as read."""
    if not MESSAGES_FILE.exists():
        print("No messages file found.")
        return

    raw_lines = MESSAGES_FILE.read_text().splitlines(keepends=True)
    updated_lines = []
    count = 0

    for line in raw_lines:
        stripped = line.strip()
        if not stripped:
            updated_lines.append(line)
            continue
        try:
            m = json.loads(stripped)
            if m.get("to") == args.agent and not m.get("read"):
                m["read"] = True
                updated_lines.append(json.dumps(m) + "\n")
                count += 1
            else:
                updated_lines.append(line)
        except json.JSONDecodeError:
            updated_lines.append(line)

    with open(MESSAGES_FILE, "w") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        try:
            f.writelines(updated_lines)
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)

    print(f"Marked {count} message(s) as read for agent '{args.agent}'.")


# ---------------------------------------------------------------------------
# Lock commands
# ---------------------------------------------------------------------------


def lock_acquire(args):
    _validate_lock_name(args.name)
    lock_file = LOCKS_DIR / f"{args.name}.lock"

    # Evict expired lock if present
    if lock_file.exists():
        try:
            data = json.loads(lock_file.read_text())
            age = time.time() - data.get("acquired_at_ts", 0)
            ttl = data.get("ttl", DEFAULT_LOCK_TTL)
            if age < ttl:
                die(
                    f"Lock '{args.name}' held by '{data.get('owner')}' "
                    f"(age {int(age)}s, TTL {ttl}s). Wait or release first."
                )
            lock_file.unlink(missing_ok=True)
        except (json.JSONDecodeError, KeyError):
            lock_file.unlink(missing_ok=True)

    payload = {
        "owner": args.owner,
        "acquired_at": now_iso(),
        "acquired_at_ts": time.time(),
        "ttl": args.ttl or DEFAULT_LOCK_TTL,
    }
    # O_CREAT | O_EXCL is atomic: only one process succeeds even under concurrency.
    try:
        fd = os.open(str(lock_file), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
        with os.fdopen(fd, "w") as f:
            json.dump(payload, f)
    except FileExistsError:
        die(f"Lock '{args.name}' was acquired concurrently by another process.")

    _timeline_write(f"lock.acquired name={args.name} owner={args.owner}")
    print(f"Lock '{args.name}' acquired by '{args.owner}'.")


def lock_release(args):
    _validate_lock_name(args.name)
    lock_file = LOCKS_DIR / f"{args.name}.lock"
    if lock_file.exists():
        lock_file.unlink()
        _timeline_write(f"lock.released name={args.name}")
        print(f"Lock '{args.name}' released.")
    else:
        print(f"Lock '{args.name}' not found (already released?).")


def lock_status(args):
    if args.name:
        _validate_lock_name(args.name)
        lock_file = LOCKS_DIR / f"{args.name}.lock"
        if not lock_file.exists():
            print(json.dumps({"name": args.name, "status": "free"}))
            return
        data = json.loads(lock_file.read_text())
        age = int(time.time() - data.get("acquired_at_ts", 0))
        print(json.dumps({"name": args.name, "status": "locked", "age_seconds": age, **data}))
        return

    # All locks
    results = []
    for lf in LOCKS_DIR.glob("*.lock"):
        try:
            data = json.loads(lf.read_text())
            age = int(time.time() - data.get("acquired_at_ts", 0))
            results.append({"name": lf.stem, "status": "locked", "age_seconds": age, **data})
        except Exception:
            results.append({"name": lf.stem, "status": "unreadable"})
    print(json.dumps(results, indent=2))


# ---------------------------------------------------------------------------
# Timeline
# ---------------------------------------------------------------------------


def _timeline_write(event: str):
    _append_line_locked(TIMELINE_FILE, f"{now_iso()} {event}")


def timeline_append(args):
    _timeline_write(args.event)
    print(f"Timeline: {args.event}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="agent-runtime",
        description="Codex Agent Ecosystem v2 — Agent Runtime",
    )
    sub = p.add_subparsers(dest="command", required=True)

    # ---- task ----
    task_p = sub.add_parser("task", help="Task State Engine commands")
    task_sub = task_p.add_subparsers(dest="subcommand", required=True)

    # task create
    tc = task_sub.add_parser("create", help="Create a new task")
    tc.add_argument("--title", required=True)
    tc.add_argument("--owner", required=True)
    tc.add_argument("--priority", choices=["low", "medium", "high", "critical"], default="medium")
    tc.add_argument("--depends-on", dest="depends_on", help="Comma-separated task IDs")
    tc.add_argument("--inputs", help="Context/inputs for the task")
    tc.add_argument("--reviewer", help="Agent responsible for reviewing this task")

    # task list
    tl = task_sub.add_parser("list", help="List tasks")
    tl.add_argument("--status", choices=list(VALID_TASK_STATES))
    tl.add_argument("--owner", help="Filter by owner agent")

    # task claim
    tclaim = task_sub.add_parser("claim", help="Claim a pending task")
    tclaim.add_argument("--id", required=True)
    tclaim.add_argument("--owner", required=True)

    # task update
    tu = task_sub.add_parser("update", help="Update task status or outputs")
    tu.add_argument("--id", required=True)
    tu.add_argument("--status", choices=list(VALID_TASK_STATES))
    tu.add_argument("--outputs", help="Output description or artifact paths")
    tu.add_argument("--reviewer", help="Assign a reviewer")

    # task complete
    tcomp = task_sub.add_parser("complete", help="Mark task as done")
    tcomp.add_argument("--id", required=True)
    tcomp.add_argument("--outputs", help="Output description or artifact paths")

    # task fail
    tfail = task_sub.add_parser("fail", help="Mark task as failed")
    tfail.add_argument("--id", required=True)
    tfail.add_argument("--reason", help="Failure reason")

    # ---- message ----
    msg_p = sub.add_parser("message", help="Agent messaging commands")
    msg_sub = msg_p.add_subparsers(dest="subcommand", required=True)

    # message send
    ms = msg_sub.add_parser("send", help="Send a message to another agent")
    ms.add_argument("--from", dest="from_agent", required=True)
    ms.add_argument("--to", dest="to_agent", required=True)
    ms.add_argument("--task-id", dest="task_id")
    ms.add_argument("--type", dest="type", required=True, choices=list(VALID_MESSAGE_TYPES))
    ms.add_argument("--summary", required=True)
    ms.add_argument("--files", help="Comma-separated file paths referenced")
    ms.add_argument("--needs-reply", dest="needs_reply", action="store_true", default=False)

    # message inbox
    mi = msg_sub.add_parser("inbox", help="Read messages for an agent")
    mi.add_argument("--agent", required=True)
    mi.add_argument(
        "--unread",
        action="store_true",
        default=False,
        help="Show only unread messages and mark them as read",
    )

    # message mark-read
    mr = msg_sub.add_parser("mark-read", help="Mark all messages for an agent as read")
    mr.add_argument("--agent", required=True)

    # ---- lock ----
    lock_p = sub.add_parser("lock", help="Distributed lock commands")
    lock_sub = lock_p.add_subparsers(dest="subcommand", required=True)

    la = lock_sub.add_parser("acquire", help="Acquire a named lock")
    la.add_argument("--name", required=True)
    la.add_argument("--owner", required=True)
    la.add_argument("--ttl", type=int, help=f"Lock TTL in seconds (default {DEFAULT_LOCK_TTL})")

    lr = lock_sub.add_parser("release", help="Release a named lock")
    lr.add_argument("--name", required=True)

    ls = lock_sub.add_parser("status", help="Show lock status")
    ls.add_argument("--name", help="Specific lock name (omit for all)")

    # ---- timeline ----
    tl_p = sub.add_parser("timeline", help="Append to the shared timeline")
    tl_sub = tl_p.add_subparsers(dest="subcommand", required=True)

    ta = tl_sub.add_parser("append", help="Append an event")
    ta.add_argument("--event", required=True)

    return p


def main():
    init_cache()
    parser = build_parser()
    args = parser.parse_args()

    dispatch = {
        ("task", "create"): task_create,
        ("task", "list"): task_list,
        ("task", "claim"): task_claim,
        ("task", "update"): task_update,
        ("task", "complete"): task_complete,
        ("task", "fail"): task_fail,
        ("message", "send"): message_send,
        ("message", "inbox"): message_inbox,
        ("message", "mark-read"): message_mark_read,
        ("lock", "acquire"): lock_acquire,
        ("lock", "release"): lock_release,
        ("lock", "status"): lock_status,
        ("timeline", "append"): timeline_append,
    }

    fn = dispatch.get((args.command, args.subcommand))
    if fn is None:
        parser.print_help()
        sys.exit(1)
    fn(args)


if __name__ == "__main__":
    main()

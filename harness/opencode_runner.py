"""Run one OpenCode episode with event streaming and external budget limits.

OpenCode emits each tool_use event after the tool has finished, so a limit is
enforced by terminating the process tree when the counter reaches the limit.
The call that triggered the limit has already completed and its effect remains
in the workspace.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG_TEMPLATE = ROOT / "harness" / "configs" / "main" / "opencode.json"

EDIT_TOOLS = {"edit", "write", "patch"}


@dataclass
class RunLimits:
    tool_calls: int = 10
    edits: int = 8
    seconds: float = 300.0
    cost_usd: float = 0.50


@dataclass
class RunResult:
    exit_code: int
    timed_out: bool
    budget_exhausted: bool
    budget_reasons: list[str] = field(default_factory=list)
    duration_s: float = 0.0
    tool_calls: int = 0
    edits: int = 0
    steps: int = 0
    cost_usd: float = 0.0
    tool_breakdown: dict[str, int] = field(default_factory=dict)
    first_edit_after_read: bool | None = None
    events: list[dict] = field(default_factory=list)


def prepare_config(config_home: Path, template: Path = CONFIG_TEMPLATE) -> Path:
    """Write the experiment OpenCode config into an isolated XDG directory."""
    target = config_home / "opencode" / "opencode.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(template, target)
    return target


def kill_process_tree(process: subprocess.Popen) -> None:
    subprocess.run(
        ["taskkill", "/PID", str(process.pid), "/T", "/F"],
        capture_output=True,
    )


def _event_counters(event: dict, counters: dict) -> None:
    kind = event.get("type")
    part = event.get("part", {}) or {}
    if kind == "tool_use":
        counters["tool_calls"] += 1
        tool = str(part.get("tool", "unknown"))
        counters["tool_breakdown"][tool] = counters["tool_breakdown"].get(tool, 0) + 1
        if tool in EDIT_TOOLS:
            counters["edits"] += 1
        if tool in {"read", "glob", "grep", "list"} and counters["first_edit_index"] is None:
            counters["read_before_edit"] = True
        if tool in EDIT_TOOLS and counters["first_edit_index"] is None:
            counters["first_edit_index"] = counters["tool_calls"]
    elif kind == "step_finish":
        counters["steps"] += 1
        counters["cost_usd"] += float(part.get("cost", 0.0) or 0.0)


def run_opencode(
    repo: Path,
    prompt: str,
    model: str,
    limits: RunLimits,
    raw_log: Path,
    config_home: Path,
    data_home: Path,
    config_template: Path = CONFIG_TEMPLATE,
) -> RunResult:
    prepare_config(config_home, config_template)
    data_home.mkdir(parents=True, exist_ok=True)

    env = dict(os.environ)
    env["XDG_CONFIG_HOME"] = str(config_home)
    env["XDG_DATA_HOME"] = str(data_home)
    env["PYTHONDONTWRITEBYTECODE"] = "1"

    command = [
        "opencode",
        "run",
        "--dir",
        str(repo),
        "--model",
        model,
        "--agent",
        "build",
        "--format",
        "json",
        "--pure",
        "--auto",
        prompt,
    ]
    started = time.monotonic()
    process = subprocess.Popen(
        command,
        cwd=repo,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
    )

    stdout_lines: list[str] = []
    stderr_lines: list[str] = []
    counters = {
        "tool_calls": 0,
        "edits": 0,
        "steps": 0,
        "cost_usd": 0.0,
        "tool_breakdown": {},
        "first_edit_index": None,
        "read_before_edit": False,
        "timed_out": False,
        "reasons": [],
    }
    lock = threading.Lock()

    def read_stderr() -> None:
        for line in process.stderr:
            stderr_lines.append(line)

    def read_stdout() -> None:
        for line in process.stdout:
            stdout_lines.append(line)
            stripped = line.strip()
            if not stripped.startswith("{"):
                continue
            try:
                event = json.loads(stripped)
            except json.JSONDecodeError:
                continue
            with lock:
                _event_counters(event, counters)
                reasons = counters["reasons"]
                if counters["tool_calls"] >= limits.tool_calls:
                    if "tool_calls" not in reasons:
                        reasons.append("tool_calls")
                if counters["edits"] >= limits.edits:
                    if "edits" not in reasons:
                        reasons.append("edits")
                if counters["cost_usd"] > limits.cost_usd:
                    if "cost" not in reasons:
                        reasons.append("cost")
                stop = bool(reasons)
            if stop:
                kill_process_tree(process)
                return

    stderr_thread = threading.Thread(target=read_stderr, daemon=True)
    stdout_thread = threading.Thread(target=read_stdout, daemon=True)
    stderr_thread.start()
    stdout_thread.start()
    try:
        process.wait(timeout=limits.seconds)
    except subprocess.TimeoutExpired:
        with lock:
            counters["timed_out"] = True
        kill_process_tree(process)
        process.wait()
    stdout_thread.join(timeout=30)
    stderr_thread.join(timeout=30)

    duration = time.monotonic() - started
    stdout = "".join(stdout_lines)
    stderr = "".join(stderr_lines)
    raw_log.write_text(stdout + "\n--- STDERR ---\n" + stderr, encoding="utf-8")

    events = []
    for line in stdout.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue

    return RunResult(
        exit_code=process.returncode,
        timed_out=counters["timed_out"],
        budget_exhausted=bool(counters["reasons"]),
        budget_reasons=list(counters["reasons"]),
        duration_s=duration,
        tool_calls=counters["tool_calls"],
        edits=counters["edits"],
        steps=counters["steps"],
        cost_usd=counters["cost_usd"],
        tool_breakdown=dict(counters["tool_breakdown"]),
        first_edit_after_read=(
            counters["read_before_edit"] if counters["first_edit_index"] else None
        ),
        events=events,
    )

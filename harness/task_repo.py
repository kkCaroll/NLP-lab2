"""Task repository handling for the main experiment.

A workspace is a copy of a task repository under a temporary run root. It is
initialised as a git repository so that every episode state can be committed,
diffed and branched without touching the task sources under tasks/.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASKS = ROOT / "tasks"

TEST_CONFIG_FILES = [
    "pyproject.toml",
    "pytest.ini",
    "setup.cfg",
    "tox.ini",
    "conftest.py",
    "tests/conftest.py",
    "sitecustomize.py",
    "usercustomize.py",
]

BASELINE = "baseline"
ROUND1 = "round1"
ROUND2 = "round2"


def load_meta(task_name: str) -> dict:
    path = TASKS / task_name / "meta.json"
    return json.loads(path.read_text(encoding="utf-8"))


def copy_repo(task_name: str, destination: Path) -> Path:
    source = TASKS / task_name / "repo"
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(source, destination)
    return destination


def snapshot_repo(task_name: str, destination: Path) -> Path:
    source = TASKS / task_name / "repo"
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(source, destination)
    return destination


def _git(workspace: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args],
        cwd=workspace,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def init_repo(workspace: Path) -> None:
    git_dir = workspace / ".git"
    if git_dir.exists():
        shutil.rmtree(git_dir)
    _git(workspace, "init", "-q")
    _git(workspace, "config", "user.name", "experiment")
    _git(workspace, "config", "user.email", "experiment@local")
    _git(workspace, "config", "core.autocrlf", "false")
    _git(workspace, "config", "core.safecrlf", "false")
    _git(workspace, "add", "-A")
    _git(workspace, "commit", "-q", "-m", BASELINE)
    tag(workspace, BASELINE)


def tag(workspace: Path, name: str) -> None:
    _git(workspace, "tag", "-f", name)


def is_dirty(workspace: Path) -> bool:
    result = _git(workspace, "status", "--porcelain")
    return bool(result.stdout.strip())


def commit_all(workspace: Path, message: str) -> bool:
    _git(workspace, "add", "-A")
    if not is_dirty(workspace):
        return False
    _git(workspace, "commit", "-q", "-m", message)
    return True


def rev_parse(workspace: Path, name: str) -> str:
    return _git(workspace, "rev-parse", "--verify", name).stdout.strip()


def wait_for_stable_tree(root: Path, timeout: float = 5.0, interval: float = 0.2) -> bool:
    """Wait until two consecutive tree hashes match.

    OpenCode may finish an in-flight file write just after the process tree is
    killed. Waiting for a stable hash prevents a late write from landing
    between the commit and the branch copies.
    """
    import time

    last = None
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        current = tree_hash(root)
        if current == last:
            return True
        last = current
        time.sleep(interval)
    return False


def diff_text(workspace: Path, base: str, target: str = "HEAD") -> str:
    result = _git(workspace, "diff", "--no-color", "--no-ext-diff", base, target)
    return result.stdout


def numstat(workspace: Path, base: str, target: str = "HEAD") -> list[tuple[int, int, str]]:
    result = _git(workspace, "diff", "--numstat", base, target)
    rows = []
    for line in result.stdout.splitlines():
        parts = line.split("\t")
        if len(parts) != 3:
            continue
        added, deleted, path = parts
        if added == "-" or deleted == "-":
            continue
        rows.append((int(added), int(deleted), path.replace("\\", "/")))
    return rows


def is_source_file(path: str) -> bool:
    if not path.endswith(".py"):
        return False
    if path.startswith("tests/") or "/tests/" in path:
        return False
    return True


def source_diff_stats(workspace: Path, base: str, target: str = "HEAD") -> tuple[int, list[str]]:
    lines = 0
    files = []
    for added, deleted, path in numstat(workspace, base, target):
        if not is_source_file(path):
            continue
        lines += added + deleted
        files.append(path)
    return lines, files


def normalize_paths(text: str, workspace: Path) -> str:
    variants = {
        str(workspace),
        str(workspace).replace("\\", "/"),
        str(workspace).replace("/", "\\"),
    }
    result = text
    for variant in sorted(variants, key=len, reverse=True):
        result = result.replace(variant, "<workspace>")
    return result


def _hash_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def hash_tests(workspace: Path) -> dict[str, str]:
    result = {}
    tests = workspace / "tests"
    if tests.exists():
        for path in sorted(tests.rglob("*")):
            if not path.is_file():
                continue
            if "__pycache__" in path.parts:
                continue
            result[path.relative_to(workspace).as_posix()] = _hash_file(path)
    for name in TEST_CONFIG_FILES:
        path = workspace / name
        if path.is_file():
            result[name] = _hash_file(path)
    return result


def restore_tests(snapshot: Path, workspace: Path) -> None:
    source = snapshot / "tests"
    target = workspace / "tests"
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(source, target)
    for name in TEST_CONFIG_FILES:
        src = snapshot / name
        dst = workspace / name
        if src.is_file():
            shutil.copyfile(src, dst)
        elif dst.is_file():
            dst.unlink()


def tree_hash(root: Path) -> dict[str, str]:
    result = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if any(part in {"__pycache__", ".pytest_cache", ".git"} for part in path.parts):
            continue
        result[path.relative_to(root).as_posix()] = _hash_file(path)
    return result

"""Create independent round 2 branches from the round 1 workspace."""

from __future__ import annotations

import shutil
from pathlib import Path


def create_branches(
    round1_workspace: Path, branch_root: Path, conditions: list[str]
) -> dict[str, Path]:
    """Copy the round 1 workspace, including .git, once per condition."""
    if branch_root.exists():
        shutil.rmtree(branch_root)
    branch_root.mkdir(parents=True)
    branches = {}
    for condition in conditions:
        target = branch_root / condition / "repo"
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(round1_workspace, target)
        branches[condition] = target
    return branches

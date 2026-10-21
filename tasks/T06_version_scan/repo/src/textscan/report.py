"""Summary helpers for version strings."""

from collections import Counter


def version_majors(versions):
    """Return the major number of each version in order."""
    majors = []
    for version in versions:
        core = version.split("-", 1)[0]
        majors.append(int(core.split(".", 1)[0]))
    return majors


def group_by_major(versions):
    """Return versions grouped by their major number."""
    groups = {}
    for version in versions:
        core = version.split("-", 1)[0]
        major = int(core.split(".", 1)[0])
        groups.setdefault(major, []).append(version)
    return groups


def summarize_versions(versions):
    """Return the number of versions and counts per major number."""
    if not versions:
        return {"count": 0, "majors": {}}
    counts = Counter(version_majors(versions))
    return {
        "count": len(versions),
        "majors": dict(sorted(counts.items())),
    }


def format_versions(versions):
    """Return versions joined by commas."""
    return ", ".join(versions)

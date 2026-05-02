"""Fail CI if any SKILL.md is missing required frontmatter or has too-short description."""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2] / ".claude" / "skills"
REQUIRED = {"name", "description"}
MIN_DESC_LEN = 60


def main() -> int:
    failures: list[str] = []
    skill_files = list(ROOT.glob("*/SKILL.md"))
    for skill_md in skill_files:
        text = skill_md.read_text(encoding="utf-8")
        if not text.startswith("---"):
            failures.append(f"{skill_md}: missing frontmatter delimiter")
            continue
        try:
            _, fm, _ = text.split("---", 2)
        except ValueError:
            failures.append(f"{skill_md}: malformed frontmatter")
            continue
        data = yaml.safe_load(fm) or {}
        missing = REQUIRED - set(data)
        if missing:
            failures.append(f"{skill_md}: missing fields {sorted(missing)}")
        desc = data.get("description", "")
        if len(desc) < MIN_DESC_LEN:
            failures.append(f"{skill_md}: description too short ({len(desc)} chars, need ≥{MIN_DESC_LEN})")

    if failures:
        for f in failures:
            print(f"FAIL: {f}", file=sys.stderr)
        return 1
    print(f"OK: All {len(skill_files)} SKILL.md files passed frontmatter checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())

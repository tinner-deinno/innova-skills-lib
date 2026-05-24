"""
generate_adapters.py
--------------------
Reads manifests/skills_manifest.json and generates Claude adapter files.

For each skill entry:
  - Reads source SKILL.md from ~/.claude/skills/<path>/SKILL.md
  - Strips YAML frontmatter (--- ... ---)
  - Writes adapters/claude/<skill-id>.md with a header comment

Usage:
    python tools/generate_adapters.py

Stats printed on completion: created / skipped / errors.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = REPO_ROOT / "manifests" / "skills_manifest.json"
# Prefer repo-local copy of skills (CI-friendly), fall back to user home
_LOCAL_SKILLS = REPO_ROOT / "core"
_HOME_SKILLS = Path.home() / ".claude" / "skills"
SKILLS_BASE = _HOME_SKILLS  # generate_adapters reads from the live global skills
ADAPTERS_OUT = REPO_ROOT / "adapters" / "claude"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

FRONTMATTER_RE = re.compile(r"^---\s*\n.*?\n---\s*\n", re.DOTALL)


def strip_frontmatter(text: str) -> str:
    """Remove YAML frontmatter block (--- ... ---) from the top of a string."""
    return FRONTMATTER_RE.sub("", text, count=1).lstrip("\n")


def build_header(skill_id: str, skill_path: str, source_file: Path) -> str:
    """Return a Markdown comment-style header for the adapter file."""
    return (
        f"<!-- skill-id: {skill_id} -->\n"
        f"<!-- source-path: {skill_path} -->\n"
        f"<!-- source-file: {source_file.as_posix()} -->\n"
        f"<!-- runtime: claude -->\n\n"
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    # 1. Load manifest ---------------------------------------------------------
    if not MANIFEST_PATH.exists():
        print(f"[ERROR] Manifest not found: {MANIFEST_PATH}", file=sys.stderr)
        sys.exit(1)

    with MANIFEST_PATH.open(encoding="utf-8") as fh:
        try:
            raw_manifest = json.load(fh)
        except json.JSONDecodeError as exc:
            print(f"[ERROR] Invalid JSON in manifest: {exc}", file=sys.stderr)
            sys.exit(1)

    # Support both array format and wrapped {skills: [...]} format
    if isinstance(raw_manifest, list):
        manifest: list[dict] = raw_manifest
    elif isinstance(raw_manifest, dict) and "skills" in raw_manifest:
        manifest = raw_manifest["skills"]
    else:
        print("[ERROR] Manifest must be a JSON array or a dict with 'skills' key.", file=sys.stderr)
        sys.exit(1)

    # 2. Ensure output directory exists ----------------------------------------
    ADAPTERS_OUT.mkdir(parents=True, exist_ok=True)

    # 3. Process each skill ----------------------------------------------------
    created = 0
    skipped = 0
    errors = 0

    for entry in manifest:
        skill_id: str | None = entry.get("id")
        skill_path: str | None = entry.get("path")

        if not skill_id or not skill_path:
            print(f"[SKIP] Entry missing 'id' or 'path': {entry}", file=sys.stderr)
            skipped += 1
            continue

        # Check that 'claude' is listed in runtimes (skip if not targeted)
        runtimes: list[str] = entry.get("runtimes", [])
        if runtimes and "claude" not in runtimes:
            print(f"[SKIP] {skill_id}: runtime 'claude' not listed, skipping.")
            skipped += 1
            continue

        source_file = SKILLS_BASE / skill_path / "SKILL.md"

        if not source_file.exists():
            print(f"[ERROR] {skill_id}: source not found: {source_file}", file=sys.stderr)
            errors += 1
            continue

        try:
            raw = source_file.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"[ERROR] {skill_id}: cannot read source: {exc}", file=sys.stderr)
            errors += 1
            continue

        cleaned = strip_frontmatter(raw)
        header = build_header(skill_id, skill_path, source_file)
        adapter_content = header + cleaned

        out_file = ADAPTERS_OUT / f"{skill_id}.md"
        try:
            out_file.write_text(adapter_content, encoding="utf-8")
        except OSError as exc:
            print(f"[ERROR] {skill_id}: cannot write adapter: {exc}", file=sys.stderr)
            errors += 1
            continue

        print(f"[OK]   {skill_id} -> {out_file.relative_to(REPO_ROOT).as_posix()}")
        created += 1

    # 4. Stats -----------------------------------------------------------------
    total = created + skipped + errors
    print()
    print(f"=== generate_adapters stats ===")
    print(f"  Total entries : {total}")
    print(f"  Created       : {created}")
    print(f"  Skipped       : {skipped}")
    print(f"  Errors        : {errors}")

    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()

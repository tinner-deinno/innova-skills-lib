<!-- skill-id: jit-path-discipline -->
<!-- source-path: jit-path-discipline -->
<!-- source-file: C:/Users/MDES-DEV-NB/.claude/skills/jit-path-discipline/SKILL.md -->
<!-- runtime: claude -->

# Jit Path Discipline

แก้ทุกครั้งที่ path ผิด โดยไม่ต้องรอให้สั่ง

## ปัญหา

Jit architecture ใช้ `ψ/` (Unicode Greek letter U+03C8, อ่านว่า "psi" = จิต/วิญญาณ)
แทน `psi/` (ASCII fallback) เป็น **Brain Structure root**:
- `Jit/ψ/inbox/` — bus messages
- `Jit/ψ/memory/` — resonance, learnings, retrospectives
- `Jit/ψ/outbox/` — public outputs
- `Jit/ψ/bus/inbox/<organ>/` — file bus
- `Jit/ψ/vault/` — Obsidian vault

Boss rule: **ใช้ `ψ/` เสมอ** — เขียน `psi/` ผิด = สร้าง directory ใหม่ทับ canonical,
สูญเสีย history references, ทำให้ agents อ่านไม่เจอ.

## When this skill runs (autonomous)

1. **PreToolUse hook** (Edit/Write/NotebookEdit) — auto-correct path ใน
   `tool_input.content` หรือ `tool_input.file_path` ก่อน execute
2. **Session start** — scan working tree ของ Jit + URL-Checker + innova-bot
   หา `Jit/psi/` (ASCII dir) ที่อาจหลงเหลือ
3. **Every 30 min** (loop `eb9513b5`) — scan for any new `psi/` paths in
   recent file changes; emit `task:correct` to jit if found

## Pattern

```python
def correct_path(path: str) -> tuple[str, bool]:
    """Return (corrected_path, did_correct)."""
    if "Jit/psi/" in path or "/Jit/psi" in path:
        return path.replace("Jit/psi/", "Jit/ψ/").replace("/Jit/psi", "/Jit/ψ"), True
    return path, False
```

ASCII `psi` is only wrong when **adjacent to `/` and a Jit relative path**.
Standalone mentions of "psi" in comments/docs are fine (e.g. "the
character ψ represents the mind").

## Discipline rules

1. **Never create `Jit/psi/` (ASCII)** — always `Jit/ψ/` (Unicode)
2. **Migrate, don't clobber** — if `Jit/ψ/<file>` already exists, copy the
   ASCII version to `Jit/ψ/archive/migrated-from-psi-<date>/` instead of
   overwriting
3. **Self-correct in transcripts** — when you see `psi/` in a tool call
   you just made, file a self-retrospective in
   `Jit/ψ/memory/retrospectives/<date>_psi-path-miss.md` (append-only
   history, never delete)
4. **Never `git push --force`** — even when "fixing" a path miss, preserve
   history (Nothing is Deleted)

## Commands

```bash
# Standalone scan
python -m jit_path_discipline.scan --repo Jit

# Standalone correct (dry-run, then apply)
python -m jit_path_discipline.scan --repo Jit --dry-run
python -m jit_path_discipline.scan --repo Jit --apply

# Hook mode (called by PreToolUse)
python -m jit_path_discipline.hook < tool_input.json
```

## Provenance

- Born 2026-07-20 from Boss feedback "นายfail psi fix to ψ"
- First miss: created `Jit/psi/outbox/tick-*.md` 4 ไฟล์ + `psi/` in
  SKILL.md (5 จุด) + `psi/` in claude-provider.ps1 (1 จุด)
- Second miss: discovered pre-existing `Jit/psi/` tree (23 files) created
  by Sonnet earlier, parallel to canonical `Jit/ψ/` (3269 files)
- Recovery: 11 NEW files migrated to `Jit/ψ/`, 12 DUP files archived to
  `Jit/ψ/archive/migrated-from-psi-2026-07-20/`, ASCII tree deleted

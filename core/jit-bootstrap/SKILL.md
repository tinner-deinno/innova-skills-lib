---
name: jit-bootstrap
description: "Skill workflow for jit-bootstrap."
---

# Skill: /jit-bootstrap — บูตสแตรป + เช็คสุขภาพ Jit ข้าม runtime

> **เป้าหมาย**: หลัง `git pull` Jit เสร็จ ให้รันคำสั่งเดียวแล้วทุกอวัยวะพร้อมทำงาน

## คำสั่ง

```
/jit-bootstrap              # เต็มรูปแบบ: sync skills → agents → health checks
/jit-bootstrap --skills-only  # บูต skills/agents อย่างเดียว
/jit-bootstrap --health-only  # เช็ค body-check + soul-check อย่างเดียว
/jit-bootstrap --no-pull    # ไม่ git pull innova-skills-lib
```

## สิ่งที่ทำ (idempotent)

1. **หา Jit root** จาก `JIT_ROOT` env หรือ `git rev-parse --show-toplevel`
2. **หา/clone `innova-skills-lib`** จาก GitHub ถ้ายังไม่มี
3. **`git pull`** skills-lib ให้เป็นปัจจุบัน (ยกเว้น `--no-pull`)
4. **Rebuild manifest + adapters**
   - `python tools/register_skills.py`
   - `python tools/generate_adapters.py`
5. **Sync skills → global `~/.claude/skills/`**
   - รองรับ Windows junction / POSIX symlink / fallback copy
6. **Sync skills → project `.claude/skills/`** (Claude Code project-local)
7. **Health checks**
   - `bash eval/body-check.sh` (ร่างกายดิจิทัล 41 รายการ)
   - `bash eval/soul-check.sh` (จิตวิญญาณ 9 รายการ)
8. **รายงานผล** พร้อม item ไหนต้องแก้ด้วยตนเอง (เช่น `.env` ขาด)

## ข้อกำหนด

- `JIT_ROOT` ต้องชี้ Jit repo
- บน Windows ต้องมี Git Bash สำหรับ `.sh` health checks
- บน Codespaces/Linux ต้องมี `git`, `python3`, `bash`

## ไม่ทำอะไรบ้าง

- ไม่ rotate secrets
- ไม่ force-push
- ไม่รัน production mode ของ URL-Checker
- ไม่เขียนทับ history (Nothing is Deleted)

## ตัวอย่างผลลัพธ์

```
[OK] innova-skills-lib @ C:\Users\MDES-DEV-NB\DEV\innova-skills-lib
[OK] 294 skills registered, 294 adapters generated
[OK] global skills synced: 294 entries
[OK] project skills synced: 294 entries
[OK] body-check: 40 PASS / 1 WARN / 0 FAIL
[OK] soul-check: 9 PASS / 0 FAIL
🌟 Jit is ready
```

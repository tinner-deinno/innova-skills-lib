---
name: workflow-codify
description: |
  Detect recurring workflow patterns from recent sessions, design a minimal skill spec,
  and turn it into a reusable Claude Code skill in innova-skills-lib without disrupting
  running agents. Trigger proactively after retrospectives, root-cause fixes, or repeated
  friction in session metrics.
---

# /workflow-codify — บันทึกจังหวะงานที่ดีให้กลายเป็นทักษะ

> "ช่างฝีมือไม่เก็บวิชาไว้คนเดียว — เมื่อไหร่จังหวะการทำงานซ้ำ 3 ครั้ง จงคัดลอกมันเป็นทักษะ"

## คืออะไร

ทักษะนี้ช่วยให้ Jit Oracle กลายรูป **workflow ที่ใช้ได้ผลจริง** จาก session ล่าสุดให้เป็น skill ที่ agents ทุกตัวใช้ได้ โดยไม่ต้องรอ Boss สั่ง

เหมาะกับสถานการณ์:
- มี friction เดิมซ้ำ 3 sessions ติด (session metrics บันทึกไว้)
- แก้ root cause แล้วอยากให้วิธีแก้กลายเป็นมาตรฐาน
- พบว่าขั้นตอนการทำงานดีมาก น่าจะนำกลับใช้ซ้ำได้
- ทำ `/rrr` แล้วได้บทเรียนที่เป็นขั้นตอนชัดเจน

## การใช้งาน

```
/workflow-codify                                    # สรุป pattern ล่าสุด + สร้าง draft skill
/workflow-codify from <path-to-retro.md>           # อ่าน retro ที่ระบุแล้วคัด pattern
/workflow-codify propose-only                       # ออกแบบ spec แต่ยังไม่สร้างไฟล์
/workflow-codify apply                              # สร้าง skill + register + sync
```

## ขั้นตอนการทำงาน

### 1. เก็บ evidence (ล่าสุด 7 วัน)

อ่านแหล่งข้อมูลต่อไปนี้ตามลำดับ:
- `ψ/memory/retrospectives/` — retro ที่มี "Recurring Pattern Detected"
- `ψ/memory/learnings/session-metrics.md` — แถว friction ซ้ำ
- git log 7 วันของ Jit, URL-Checker, innova-skills-lib
- `ψ/memory/learnings/` — learnings ล่าสุด

หยุดทันทีถ้าไม่พบ pattern ที่ชัดเจน (ไม่สร้าง skill ที่ไม่จำเป็น)

### 2. ตั้งชื่อและเลือก category

| Pattern type | Category | ชื่อตัวอย่าง |
|---|---|---|
| Root-cause operational fix | `core/` | `windows-subprocess-isolation`, `path-discipline` |
| Code review workflow | `core/` | `scrutinize`, `debug-mantra` |
| Multi-agent handoff | `core/` | `learnself`, `gang` |
| Coding standard | `ECC/` | `skill-frontmatter` |

ชื่อ skill ต้อง:
- สั้น เข้าใจได้ทันที
- ไม่ซ้ำกับ skill ที่มีอยู่ (check `skills_index.md` หรือ `manifests/skills_manifest.json`)
- ไม่ใช้ชื่อกว้างเกินไป เช่น `fix-everything`

### 3. เขียน spec ก่อนสร้างไฟล์

บันทึก draft ไว้ใน:
```
ψ/writing/workflow-codify/<skill-name>-spec-YYYY-MM-DD.md
```

Spec ต้องมี:
- **Problem**: ปัญหาหรือ friction ที่พบ
- **Trigger**: เมื่อไหร่ควรใช้ skill นี้
- **Workflow**: ขั้นตอนที่ทำซ้ำได้
- **Safety gates**: อะไรห้ามทำ (เช่น ไม่กระทบ agents ที่กำลังทำงาน)
- **Verification**: วัดผลยังไงว่า skill ใช้ได้
- **Simpler alternative**: มีวิธีง่ายกว่าหรือไม่ (mandatory)

### 4. สร้าง skill file

- สร้าง directory ใน `innova-skills-lib/core/<skill-name>/`
- เขียน `SKILL.md` พร้อม YAML frontmatter (`name`, `description`)
- เนื้อหาต้อง actionable: มีคำสั่ง ตัวอย่าง และ pitfalls

### 5. Register และ sync

```bash
cd C:\Users\MDES-DEV-NB\DEV\innova-skills-lib
python tools/register_skills.py
python tools/generate_adapters.py --runtime claude
```

Sync ไปยัง global skills:
```powershell
New-Item -ItemType Junction -Path "$env:USERPROFILE\.claude\skills\<skill-name>" -Target "C:\Users\MDES-DEV-NB\DEV\innova-skills-lib\core\<skill-name>"
```

### 6. แทรก trigger ตามธรรมชาติ

หลังจาก skill พร้อม ให้แทรกข้อความเชิญใช้ในจุดเหล่านี้:
- ท้าย `/rrr` — ถ้า retro พบ recurring pattern
- ท้าย `/scrutinize` — ถ้า finding เป็น systemic risk
- ท้าย root-cleanup / path migration — ถ้า load-bearing contract ถูกค้นพบ
- ท้าย skill-frontmatter fix — ถ้า format issue ซ้ำ

## Safety gates

- **ไม่แก้ไขไฟล์ที่ agents อื่นกำลังทำงานอยู่** — ตรวจสอบ git worktree list / task list ก่อน
- **ไม่ลบหรือ overwrite skill เก่า** — ถ้าซ้ำให้ merge หรือ retire ด้วยการย้ายไป `deprecated/`
- **ไม่ force-push** innova-skills-lib
- **push หลัง register/adapters สำเร็จและ manifest ถูกต้อง**

## ตัวอย่าง skill ที่เกิดจาก pattern จริง

| Pattern | Skill | Born from |
|---|---|---|
| `psi/` vs `ψ/` path confusion | `jit-path-discipline` | Boss feedback + 23 dup files |
| Windows pythonw subprocess + singleton | `jit-autonomous-loop` | Overnight canary false-negatives |
| Skill frontmatter parser failures | implicit workflow | 56 file mass fix |
| Root cleanup must preserve load-bearing contracts | `workflow-codify` itself | backlog.md rescue |

## ตรวจสอบก่อนเสร็จ

- [ ] มี YAML frontmatter ถูกต้อง
- [ ] `register_skills.py` ผ่าน (errors=0)
- [ ] `generate_adapters.py --runtime claude` ผ่าน
- [ ] มี junction ใน `~/.claude/skills/<skill-name>/`
- [ ] ไม่มีไฟล์ถูก overwrite โดยไม่ตั้งใจ
- [ ] commit message ใช้ conventional commits (`feat(skill): ...`)

## ดูเพิ่มเติม

- `/rrr` — session retrospective
- `/scrutinize` — outsider review
- `/skill-stocktake` — audit existing skills
- `innova-skills-lib/SETUP.md`

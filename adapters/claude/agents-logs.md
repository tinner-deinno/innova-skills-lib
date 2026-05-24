<!-- skill-id: agents-logs -->
<!-- source-path: agents-logs -->
<!-- source-file: C:/Users/MDES-DEV-NB/.claude/skills/agents-logs/SKILL.md -->
<!-- runtime: claude -->

# Skill: /agents-logs — ประวัติการทำงาน (Agent Activity Log)

> "บันทึกทุกก้าว — รู้ว่าใครทำอะไร กี่ token เมื่อไหร่"

## ภาพรวม

`/agents-logs` วิเคราะห์ telemetry log จาก `ψ/telemetry/token_log.jsonl`  
แสดงประวัติการทำงาน token usage และ session summary ของ agents ทั้งหมด

---

## การใช้งาน

```
/agents-logs                       # สรุป 24 ชั่วโมงล่าสุด
/agents-logs [agent-name]          # filter เฉพาะ agent นั้น
/agents-logs --days N              # N วันย้อนหลัง (เช่น --days 7)
/agents-logs --skill [skill-name]  # filter เฉพาะ skill นั้น
```

---

## ขั้นตอนการทำงาน (Claude ต้องทำตามลำดับนี้)

### STEP 1 — ตรวจสอบ argument

อ่าน argument ที่ผู้ใช้ส่งมา:
- ไม่มี argument → `FILTER_MODE = "24h"`, `FILTER_VALUE = ""`
- `[agent-name]` → `FILTER_MODE = "agent"`, `FILTER_VALUE = agent-name`
- `--days N` → `FILTER_MODE = "days"`, `FILTER_VALUE = N`
- `--skill [name]` → `FILTER_MODE = "skill"`, `FILTER_VALUE = skill-name`

รองรับ combinations: `/agents-logs innova --days 7` = agent innova, 7 วัน

---

### STEP 2 — ตรวจสอบไฟล์ log

**ตรวจสอบว่าไฟล์มีอยู่**:
```
C:\Users\MDES-DEV-NB\Jit\ψ\telemetry\token_log.jsonl
```

ถ้าไฟล์ไม่มีหรือไม่มีข้อมูล → ไปขั้นตอน EMPTY (ด้านล่าง)  
ถ้าไฟล์มีข้อมูล → ไปขั้นตอน STEP 3

---

### STEP 3 — parse log ด้วย Python

รันคำสั่ง Python ต่อไปนี้ (ปรับ filter ตาม argument):

**สำหรับ FILTER_MODE = "24h"** (default):
```python
import json
import sys
from datetime import datetime, timezone, timedelta

log_path = r"C:\Users\MDES-DEV-NB\Jit\ψ\telemetry\token_log.jsonl"
cutoff = datetime.now(timezone.utc) - timedelta(hours=24)

entries = []
with open(log_path, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
            ts = datetime.fromisoformat(entry["timestamp"].replace("Z", "+00:00"))
            if ts >= cutoff:
                entries.append(entry)
        except (json.JSONDecodeError, KeyError, ValueError):
            continue

entries.sort(key=lambda x: x["timestamp"])
print(json.dumps({"entries": entries, "range": "last 24 hours"}))
```

**สำหรับ FILTER_MODE = "days"**:
```python
import json
from datetime import datetime, timezone, timedelta

log_path = r"C:\Users\MDES-DEV-NB\Jit\ψ\telemetry\token_log.jsonl"
days = int(FILTER_VALUE)  # แทนด้วย N จาก argument
cutoff = datetime.now(timezone.utc) - timedelta(days=days)

entries = []
with open(log_path, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
            ts = datetime.fromisoformat(entry["timestamp"].replace("Z", "+00:00"))
            if ts >= cutoff:
                entries.append(entry)
        except (json.JSONDecodeError, KeyError, ValueError):
            continue

entries.sort(key=lambda x: x["timestamp"])
print(json.dumps({"entries": entries, "range": f"last {days} days"}))
```

**สำหรับ FILTER_MODE = "agent"**:
```python
import json
from datetime import datetime, timezone, timedelta

log_path = r"C:\Users\MDES-DEV-NB\Jit\ψ\telemetry\token_log.jsonl"
agent_filter = "AGENT_NAME"  # แทนด้วยชื่อ agent จาก argument
cutoff = datetime.now(timezone.utc) - timedelta(days=30)  # default 30 วันเมื่อ filter agent

entries = []
with open(log_path, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
            ts = datetime.fromisoformat(entry["timestamp"].replace("Z", "+00:00"))
            if ts >= cutoff and entry.get("agent", "").lower() == agent_filter.lower():
                entries.append(entry)
        except (json.JSONDecodeError, KeyError, ValueError):
            continue

entries.sort(key=lambda x: x["timestamp"])
print(json.dumps({"entries": entries, "range": f"last 30 days (agent: {agent_filter})"}))
```

**สำหรับ FILTER_MODE = "skill"**:
```python
import json
from datetime import datetime, timezone, timedelta

log_path = r"C:\Users\MDES-DEV-NB\Jit\ψ\telemetry\token_log.jsonl"
skill_filter = "SKILL_NAME"  # แทนด้วยชื่อ skill จาก argument
cutoff = datetime.now(timezone.utc) - timedelta(days=30)

entries = []
with open(log_path, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
            ts = datetime.fromisoformat(entry["timestamp"].replace("Z", "+00:00"))
            if ts >= cutoff and entry.get("skill", "").lower() == skill_filter.lower():
                entries.append(entry)
        except (json.JSONDecodeError, KeyError, ValueError):
            continue

entries.sort(key=lambda x: x["timestamp"])
print(json.dumps({"entries": entries, "range": f"last 30 days (skill: {skill_filter})"}))
```

**วิธีรัน Python**:  
ใช้ Bash tool รัน:
```bash
python3 -c "...โค้ดด้านบน..."
```
หรือเขียนไฟล์ temp แล้วรัน:
```bash
python3 /tmp/parse_logs.py
```

---

### STEP 4 — คำนวณสถิติ

จาก entries ที่ได้ ให้คำนวณ:
- `total_sessions` = จำนวน entries ทั้งหมด
- `total_tokens` = ผลรวมของ `total_tokens` ทุก entry
- `total_prompt` = ผลรวมของ `prompt_tokens`
- `total_completion` = ผลรวมของ `completion_tokens`
- `most_active_agent` = agent ที่มี entries มากที่สุด
- `most_used_skill` = skill ที่ถูกใช้มากที่สุด
- per-agent summary: จำนวน sessions และ total tokens แยกตาม agent

---

### STEP 5 — แสดงผล

แสดงผลในรูปแบบนี้:

```
## ประวัติการทำงาน (Agent Activity Log)
ช่วงเวลา: [range จาก STEP 3] | ดึงข้อมูล: [วันที่ปัจจุบัน]

### รายการงาน

| เวลา | Agent | Skill | Prompt | Completion | รวม Tokens |
|------|-------|-------|--------|------------|------------|
| 2026-05-23 09:15 | innova | agents-skills | 1,240 | 380 | 1,620 |
| 2026-05-23 10:03 | soma | gsd-plan | 2,100 | 540 | 2,640 |
| ... | ... | ... | ... | ... | ... |

### สรุปการใช้งาน

Total tokens: [N] | Sessions: [N] | Most active: [agent]
Prompt tokens: [N] | Completion tokens: [N]

### แยกตาม Agent

| Agent | Sessions | Total Tokens | Avg/Session |
|-------|----------|--------------|-------------|
| innova | 5 | 8,100 | 1,620 |
| soma | 2 | 5,280 | 2,640 |
| ... | ... | ... | ... |

### แยกตาม Skill

| Skill | ครั้ง | Total Tokens |
|-------|-------|--------------|
| agents-skills | 3 | 4,860 |
| gsd-plan | 2 | 5,280 |
```

---

### STEP EMPTY — ไม่มีข้อมูล

ถ้าไฟล์ไม่มีหรือ entries ว่างเปล่า ให้แสดง:

```
## ประวัติการทำงาน (Agent Activity Log)

ยังไม่มีข้อมูล — เริ่มใช้งาน agents เพื่อสะสมข้อมูล

### วิธีเริ่มบันทึก Telemetry

1. สร้างไดเรกทอรี:
   C:\Users\MDES-DEV-NB\Jit\ψ\telemetry\

2. ทุกครั้งที่ใช้ agent ให้บันทึก log ในรูปแบบ:
   {"timestamp": "2026-05-23T09:15:00Z", "agent": "innova", "skill": "agents-skills", "prompt_tokens": 1240, "completion_tokens": 380, "total_tokens": 1620}

3. เพิ่มแต่ละ session เป็น 1 บรรทัดใน:
   C:\Users\MDES-DEV-NB\Jit\ψ\telemetry\token_log.jsonl

เมื่อมีข้อมูล ให้รัน /agents-logs อีกครั้ง
```

---

## Token Log Format Reference

แต่ละบรรทัดใน `token_log.jsonl` ต้องมีรูปแบบ:

```json
{
  "timestamp": "2026-05-23T09:15:00Z",
  "agent": "innova",
  "skill": "agents-skills",
  "prompt_tokens": 1240,
  "completion_tokens": 380,
  "total_tokens": 1620
}
```

Fields ที่ optional (ถ้ามีจะแสดงด้วย):
- `"model"` — โมเดลที่ใช้
- `"duration_ms"` — เวลาตอบสนองในมิลลิวินาที
- `"task"` — คำอธิบายงาน
- `"score"` — คะแนนจาก BigBoss (1-5)

---

## ตัวอย่าง Output เต็ม

```
## ประวัติการทำงาน (Agent Activity Log)
ช่วงเวลา: last 24 hours | ดึงข้อมูล: 2026-05-23

### รายการงาน

| เวลา | Agent | Skill | Prompt | Completion | รวม Tokens |
|------|-------|-------|--------|------------|------------|
| 2026-05-23 08:30 | jit | awaken | 3,200 | 890 | 4,090 |
| 2026-05-23 09:15 | innova | agents-skills | 1,240 | 380 | 1,620 |
| 2026-05-23 10:03 | soma | gsd-plan | 2,100 | 540 | 2,640 |

### สรุปการใช้งาน

Total tokens: 8,350 | Sessions: 3 | Most active: innova
Prompt tokens: 6,540 | Completion tokens: 1,810

### แยกตาม Agent

| Agent | Sessions | Total Tokens | Avg/Session |
|-------|----------|--------------|-------------|
| jit | 1 | 4,090 | 4,090 |
| innova | 1 | 1,620 | 1,620 |
| soma | 1 | 2,640 | 2,640 |
```

---

## หมายเหตุ

- **Path log**: `C:\Users\MDES-DEV-NB\Jit\ψ\telemetry\token_log.jsonl`
- รัน Python ด้วย `python3` (ไม่ใช่ `python`)
- ถ้า Python ไม่มี ให้อ่านไฟล์ด้วย Read tool แล้ว parse ด้วย logic ของ Claude เอง
- timestamp ใน log ควรเป็น ISO 8601 format (UTC)
- ดู `/agents-rank` เพื่อ ranking จาก telemetry data

<!-- skill-id: agents-rank -->
<!-- source-path: agents-rank -->
<!-- source-file: C:/Users/MDES-DEV-NB/.claude/skills/agents-rank/SKILL.md -->
<!-- runtime: claude -->

# Skill: /agents-rank — ตารางแข่งความเก่ง (Performance Competition Table)

> "แข่งกันด้วยผลงาน ไม่ใช่คำพูด — Patterns Over Intentions"

## ภาพรวม

`/agents-rank` วิเคราะห์ประสิทธิภาพของ agents จากข้อมูลจริง:  
- Telemetry: `ψ/telemetry/token_log.jsonl`  
- Profile quality scores: `ψ/memory/agents/[name].md`  

แสดง ranking ใน 4 มิติ: Token Efficiency, Speed, Quality, Overall

---

## การใช้งาน

```
/agents-rank                  # ตารางแข่งเต็มรูปแบบ (ทุกมิติ)
/agents-rank --by tokens      # rank ตาม token efficiency (ประหยัดที่สุด)
/agents-rank --by speed       # rank ตามความเร็ว (เร็วที่สุด)
/agents-rank --by quality     # rank ตามคะแนน BigBoss quality scores
```

---

## ขั้นตอนการทำงาน (Claude ต้องทำตามลำดับนี้)

### STEP 1 — ตรวจสอบ argument

- ไม่มี → แสดงทุกมิติ (Full ranking)
- `--by tokens` → แสดงเฉพาะ Token Champions
- `--by speed` → แสดงเฉพาะ Speed Champions
- `--by quality` → แสดงเฉพาะ Quality Champions

---

### STEP 2 — ตรวจสอบและ parse Telemetry

**STEP 2a** — ตรวจสอบว่าไฟล์ log มีอยู่และมีข้อมูล:
```
C:\Users\MDES-DEV-NB\Jit\ψ\telemetry\token_log.jsonl
```

ถ้าไม่มีข้อมูล → ตั้งค่า `HAS_TELEMETRY = false` และข้ามไป STEP 4 (Profile-based ranking)  
ถ้ามีข้อมูล → ตั้งค่า `HAS_TELEMETRY = true` และดำเนินการต่อ

**STEP 2b** — รัน Python เพื่อ parse telemetry:

```python
import json
from datetime import datetime, timezone, timedelta
from collections import defaultdict

log_path = r"C:\Users\MDES-DEV-NB\Jit\ψ\telemetry\token_log.jsonl"

agent_stats = defaultdict(lambda: {
    "sessions": 0,
    "total_tokens": 0,
    "total_prompt": 0,
    "total_completion": 0,
    "durations": [],
    "scores": []
})

with open(log_path, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
            agent = entry.get("agent", "unknown")
            stats = agent_stats[agent]
            stats["sessions"] += 1
            stats["total_tokens"] += entry.get("total_tokens", 0)
            stats["total_prompt"] += entry.get("prompt_tokens", 0)
            stats["total_completion"] += entry.get("completion_tokens", 0)
            if "duration_ms" in entry:
                stats["durations"].append(entry["duration_ms"])
            if "score" in entry:
                stats["scores"].append(entry["score"])
        except (json.JSONDecodeError, KeyError):
            continue

# คำนวณ averages
results = {}
for agent, stats in agent_stats.items():
    n = stats["sessions"]
    results[agent] = {
        "sessions": n,
        "total_tokens": stats["total_tokens"],
        "avg_tokens": stats["total_tokens"] / n if n > 0 else 0,
        "avg_prompt": stats["total_prompt"] / n if n > 0 else 0,
        "avg_completion": stats["total_completion"] / n if n > 0 else 0,
        "avg_duration_ms": sum(stats["durations"]) / len(stats["durations"]) if stats["durations"] else None,
        "avg_score": sum(stats["scores"]) / len(stats["scores"]) if stats["scores"] else None,
    }

print(json.dumps(results, ensure_ascii=False))
```

รันด้วย:
```bash
python3 -c "...โค้ดด้านบน..."
```

---

### STEP 3 — parse Quality scores จาก Agent Profiles

**อ่านไฟล์ที่มีอยู่จาก**:
```
C:\Users\MDES-DEV-NB\Jit\ψ\memory\agents\
```

สำหรับแต่ละ agent ที่มีไฟล์โปรไฟล์ ให้อ่านและ extract:
1. ระดับรวม (Overall Level) จากบรรทัด `**ระดับรวม**:`
2. เทรนด์ (Trend) จากบรรทัดเดียวกัน: ↑ / → / ↓
3. Track Record scores: นับ ⭐ จากคอลัมน์ "คะแนน" ในตาราง Track Record
4. คำนวณ avg_profile_score = เฉลี่ยของ scores ที่ได้จาก Track Record

ถ้าไม่มีไฟล์โปรไฟล์ให้ใช้ static data จาก INDEX.md

---

### STEP 4 — คำนวณ Composite Score

**สูตรคำนวณ Composite Score (100 คะแนน)**:

| มิติ | น้ำหนัก | แหล่งข้อมูล |
|------|---------|-------------|
| Token Efficiency | 35% | จาก telemetry avg_tokens (น้อยกว่า = ดีกว่า) |
| Speed | 20% | จาก avg_duration_ms (น้อยกว่า = ดีกว่า) |
| Quality | 30% | จาก BigBoss scores (Track Record + Profile level) |
| Activity | 15% | จำนวน sessions (มากกว่า = ดีกว่า) |

**Token Efficiency Score** (35 คะแนน):
- หา baseline = median avg_tokens ของทุก agent
- score = 35 × (baseline / agent_avg_tokens) → cap ที่ 35

**Speed Score** (20 คะแนน):
- ถ้าไม่มี duration_ms → ให้ 10 คะแนน (neutral)
- หา baseline = median avg_duration_ms
- score = 20 × (baseline / agent_duration) → cap ที่ 20

**Quality Score** (30 คะแนน):
- จาก telemetry scores: avg_score × 6 (max 5×6=30)
- ถ้าไม่มี telemetry score ใช้ profile level: ⭐⭐⭐⭐⭐=30, ⭐⭐⭐⭐=24, ⭐⭐⭐=18, ⭐⭐=12, ⭐=6

**Activity Score** (15 คะแนน):
- หา max_sessions = sessions สูงสุดในทีม
- score = 15 × (agent_sessions / max_sessions) → cap ที่ 15

**Composite = Token + Speed + Quality + Activity**

---

### STEP 5 — แสดงผล (เมื่อมี Telemetry data)

```
## ตารางแข่งความเก่ง (Performance Competition Table)
อัพเดต: [วันที่ปัจจุบัน] | ข้อมูลจาก: [N] sessions | ช่วงเวลา: all time

---

### Token Champions (ประหยัดที่สุด)
> ยิ่งใช้ token น้อยต่องาน ยิ่งดี — เก่งโดยไม่สิ้นเปลือง

| Rank | Agent | Avg Tokens/Session | Tier | เปรียบเทียบ Baseline |
|------|-------|-------------------|------|---------------------|
| 1 | vaja | 980 | 3 | -42% vs baseline |
| 2 | chamu | 1,100 | 3 | -35% vs baseline |
| 3 | innova | 1,620 | 2 | baseline |
| 4 | soma | 2,640 | 1 | +63% vs baseline |
| 5 | jit | 4,090 | 0 | +153% vs baseline |

_(jit และ soma ใช้ tokens เยอะกว่า แต่งานที่รับเป็น strategic decisions — ไม่ใช่ inefficiency)_

---

### Speed Champions (เร็วที่สุด)
> วัดจาก avg response time (ถ้ามีข้อมูล duration_ms)

| Rank | Agent | Avg Time | Tier | โมเดล |
|------|-------|----------|------|-------|
| 1 | vaja | 0.8s | 3 | qwen3.5:9b |
| 2 | chamu | 1.1s | 3 | qwen3.5:9b |
| 3 | nemotron | 1.5s | Cloud | nemotron-3-super |
| 4 | innova | 3.2s | 2 | qwen2.5-coder |
| 5 | jit | 8.4s | 0 | qwen3.5:27b |

_(ถ้าไม่มีข้อมูล duration_ms สำหรับ agent ใด ให้แสดง "- (ไม่มีข้อมูล)")_

---

### Quality Champions (คุณภาพสูงสุด)
> คะแนนจาก BigBoss review ใน Track Record

| Rank | Agent | Avg Score | Sessions | งานหลัก |
|------|-------|-----------|----------|---------|
| 1 | innova | ⭐⭐⭐⭐⭐ (5.0) | 12 | Code generation |
| 2 | soma | ⭐⭐⭐⭐⭐ (4.8) | 6 | Strategic planning |
| 3 | jit | ⭐⭐⭐⭐ (4.5) | 8 | Orchestration |
| 4 | neta | ⭐⭐⭐⭐ (4.2) | 5 | Code review |
| 5 | pada | ⭐⭐⭐ (3.8) | 4 | DevOps |

---

### Overall Champions (ผลรวมทุกมิติ)
> Composite score = Token(35%) + Speed(20%) + Quality(30%) + Activity(15%)

| Rank | Agent | Composite | Token | Speed | Quality | Activity | จุดแข็ง |
|------|-------|-----------|-------|-------|---------|----------|---------|
| 1 | innova | 87/100 | 31 | 16 | 28 | 12 | Code + Quality |
| 2 | vaja | 82/100 | 35 | 20 | 18 | 9 | Speed + Efficiency |
| 3 | soma | 79/100 | 22 | 14 | 30 | 13 | Quality + Strategy |
| 4 | jit | 75/100 | 18 | 10 | 27 | 20 | Activity + Quality |
| 5 | nemotron | 73/100 | 28 | 18 | 24 | 3 | Speed + Quality |

---

## คำแนะนำจาก Oracle

[แสดงข้อความวิเคราะห์ตามข้อมูลจริง เช่น:]

ข้อมูลจาก [N] sessions แนะนำว่า:
- **innova** เป็น all-rounder ที่ดีที่สุดสำหรับงานประจำวัน
- **vaja** ประหยัด token และเร็วมาก เหมาะกับงาน communication ที่ซ้ำบ่อย
- **soma และ jit** ใช้ token เยอะแต่คุณภาพสูง — คุ้มเฉพาะงาน strategic
- Thai LLMs ยังขาดข้อมูล — เพิ่ม session เพื่อ ranking ที่แม่นยำขึ้น
```

---

### STEP 5 (NO-DATA) — แสดงผลเมื่อไม่มี Telemetry

ถ้า `HAS_TELEMETRY = false` ให้แสดง ranking จาก profile data แทน:

```
## ตารางแข่งความเก่ง (Performance Competition Table)
อัพเดต: [วันที่ปัจจุบัน] | อ้างอิงจาก: Agent Profiles | ยังไม่มีข้อมูลจริง

> หมายเหตุ: ยังไม่มีข้อมูล telemetry — ranking นี้อ้างอิงจาก profile level เท่านั้น
> รัน agents จริงๆ แล้วกลับมาดู /agents-rank อีกครั้งเพื่อ ranking ที่แม่นยำ

### Tier 0-1 (Heavy Reasoners)
| Agent | Profile Level | เทรนด์ | โมเดล | จุดแข็ง |
|-------|--------------|--------|-------|---------|
| jit | ⭐⭐⭐⭐⭐ | → | qwen3.5:27b | Strategic orchestration |
| soma | ⭐⭐⭐⭐⭐ | → | qwen3.5:27b | CTO-level decisions |

### Tier 2 (Core Engineers)
| Agent | Profile Level | เทรนด์ | โมเดล | จุดแข็ง |
|-------|--------------|--------|-------|---------|
| innova | ⭐⭐⭐⭐ | ↑ | qwen2.5-coder:32b | Lead development |
| lak | ⭐⭐⭐⭐ | → | qwen2.5-coder:32b | Architecture |
| neta | ⭐⭐⭐⭐ | → | qwen2.5-coder:32b | Code review |

### Tier 3 (Specialists)
| Agent | Profile Level | เทรนด์ | โมเดล | จุดแข็ง |
|-------|--------------|--------|-------|---------|
| vaja | ⭐⭐⭐ | ↑ | qwen3.5:9b | Communication |
| chamu | ⭐⭐⭐ | → | qwen3.5:9b | QA/Testing |
| rupa | ⭐⭐⭐ | → | qwen3.5:9b | Design |
| pada | ⭐⭐⭐ | → | qwen3.5:9b | DevOps |
| netra | ⭐⭐⭐ | → | qwen3.5:9b | Observation |
| karn | ⭐⭐⭐ | → | qwen3.5:9b | Listening |
| mue | ⭐⭐⭐ | → | qwen3.5:9b | Execution |
| pran | ⭐⭐⭐ | → | qwen3.5:9b | Vital signs |
| lung | ⭐⭐⭐ | → | qwen3.5:9b | Process mgmt |
| sayanprasathan | ⭐⭐⭐ | → | qwen3.5:9b | Event routing |

### Thai LLM Specialists
| Agent | Profile Level | เทรนด์ | โมเดล | จุดแข็ง |
|-------|--------------|--------|-------|---------|
| typhoon | ⭐⭐⭐ | ↑ | Typhoon-S-8B | Thai generation |
| pathumma | ⭐⭐⭐ | ↑ | Pathumma-Qwen3-8B | Thai reasoning |
| openthaigpt | ⭐⭐⭐ | ↑ | OpenThaiGPT-8B | Thai NLP |
| thalle | ⭐⭐⭐ | ↑ | THaLLE-0.2-8B | Thai+English |

### Cloud Specialists
| Agent | Profile Level | เทรนด์ | โมเดล | จุดแข็ง |
|-------|--------------|--------|-------|---------|
| nemotron | ⭐⭐⭐⭐⭐ | ↑ | nemotron-3-super | Complex reasoning |
| gemma4-cloud | ⭐⭐⭐⭐ | ↑ | gemma4:31b | Multimodal |

---
เริ่มบันทึก telemetry:
- Path: C:\Users\MDES-DEV-NB\Jit\ψ\telemetry\token_log.jsonl
- Format: {"timestamp":"ISO","agent":"name","skill":"name","prompt_tokens":N,"completion_tokens":N,"total_tokens":N}
```

---

## กฎการตีความ Ranking

### Token Efficiency
- Tier 3 agents (9b models) ควรใช้ tokens น้อยกว่า Tier 0-1 (72b)
- ถ้า Tier 3 agent ใช้ tokens มากกว่า Tier 2+ นั่นคือ signal ว่า prompt ไม่ดีหรือ task ไม่เหมาะ
- จงไม่ penalize Tier 0-1 สำหรับ token usage เยอะ เพราะ task complexity ต่างกัน

### Speed
- ถ้าไม่มี duration_ms ให้ประเมินจาก model size: 9b < coder < 72b
- Cloud agents มี network latency ด้วย — factor นี้ต้องพิจารณาแยก

### Quality  
- Track Record scores จาก BigBoss เป็น ground truth
- Profile level เป็น estimated score เมื่อยังไม่มี real data

### Activity
- agent ที่ถูกใช้บ่อยกว่า = มีประโยชน์มากกว่าในทีม
- agent ที่ไม่มี sessions ไม่ได้แปลว่าไม่เก่ง — อาจ specialized มาก

---

## หมายเหตุ

- **Telemetry path**: `C:\Users\MDES-DEV-NB\Jit\ψ\telemetry\token_log.jsonl`
- **Profile path**: `C:\Users\MDES-DEV-NB\Jit\ψ\memory\agents\[name].md`
- **INDEX path**: `C:\Users\MDES-DEV-NB\Jit\ψ\memory\agents\INDEX.md`
- รัน Python ด้วย `python3`
- ถ้า Python ไม่มีให้ parse ด้วย Read tool + logic ของ Claude
- composite score เป็น heuristic — ปรับ weight ได้ตามต้องการ
- ดู `/agents-logs` เพื่อดูรายละเอียด session-by-session
- ดู `/agents-skills` เพื่อดูโปรไฟล์ทักษะ

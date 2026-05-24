<!-- skill-id: agents-skills -->
<!-- source-path: agents-skills -->
<!-- source-file: C:/Users/MDES-DEV-NB/.claude/skills/agents-skills/SKILL.md -->
<!-- runtime: claude -->

# Skill: /agents-skills — สมุดทักษะ (Agent Skill Book)

> "รู้จักทีม รู้จักเครื่องมือ — ใช้คนให้ถูกงาน ใช้โมเดลให้ถูกเวลา"

## ภาพรวม

`/agents-skills` แสดงโปรไฟล์ทักษะของ agents ทั้งหมดในระบบมนุษย์ Agent (21 agents)  
อ่านข้อมูลจาก `ψ/memory/agents/` และแสดงผลแบบ BigBoss-friendly

---

## การใช้งาน

```
/agents-skills                     # ตารางสรุปทุก agent
/agents-skills [agent-name]        # โปรไฟล์เต็มของ agent นั้น
/agents-skills --tier 0            # กรองตาม tier (0/1/2/3/thai/cloud)
/agents-skills --tier thai         # เฉพาะ Thai LLM agents
/agents-skills --tier cloud        # เฉพาะ Cloud agents
```

---

## ขั้นตอนการทำงาน (Claude ต้องทำตามลำดับนี้)

### STEP 1 — ตรวจสอบ argument

อ่าน argument ที่ผู้ใช้ส่งมา:
- ไม่มี argument → ไปขั้นตอน A (ตารางสรุป)
- มี `--tier [value]` → ไปขั้นตอน B (filter ตาม tier)
- มีชื่อ agent → ไปขั้นตอน C (โปรไฟล์เต็ม)

---

### STEP A — ตารางสรุปทุก agent (ไม่มี argument)

**A1.** อ่านไฟล์ INDEX:
```
C:\Users\MDES-DEV-NB\Jit\ψ\memory\agents\INDEX.md
```

**A2.** สำหรับ agent ที่มีไฟล์โปรไฟล์ ให้อ่านด้วย:
```
C:\Users\MDES-DEV-NB\Jit\ψ\memory\agents\[agent-name].md
```
ตรวจสอบว่าไฟล์มีอยู่จริงก่อนอ่าน — ถ้าไม่มีให้ใช้ข้อมูลจาก INDEX แทน

**A3.** แสดงผลในรูปแบบนี้:

```
## สมุดทักษะ (Agent Skill Book)
อัพเดต: [วันที่ปัจจุบัน] | จำนวน agents: 21 ตัว

### Tier 0 — Master
| Agent | อวัยวะ | โมเดล | ทักษะหลัก | ระดับ | เทรนด์ |
|-------|--------|-------|-----------|-------|--------|
| jit | จิต | qwen2.5:72b | Strategic Orchestration | ⭐⭐⭐⭐⭐ | → |

### Tier 1 — Leadership  
| Agent | อวัยวะ | โมเดล | ทักษะหลัก | ระดับ | เทรนด์ |
|-------|--------|-------|-----------|-------|--------|
| soma | สมอง | qwen2.5:72b | Strategic Planning | ⭐⭐⭐⭐⭐ | → |

### Tier 2 — Core Engineering
| Agent | อวัยวะ | โมเดล | ทักษะหลัก | ระดับ | เทรนด์ |
|-------|--------|-------|-----------|-------|--------|
| innova | จิตใจ | qwen2.5-coder | Code Generation | ⭐⭐⭐⭐ | ↑ |
| lak | กระดูกสันหลัง | qwen2.5-coder | System Architecture | ⭐⭐⭐⭐ | → |
| neta | ตา (review) | qwen2.5-coder | Code Review | ⭐⭐⭐⭐ | → |

### Tier 3 — Specialist Organs
| Agent | อวัยวะ | โมเดล | ทักษะหลัก | ระดับ | เทรนด์ |
|-------|--------|-------|-----------|-------|--------|
| vaja | ปาก | gemma2:9b | Communication | ⭐⭐⭐ | ↑ |
| chamu | จมูก | gemma2:9b | QA Testing | ⭐⭐⭐ | → |
| rupa | รูปลักษณ์ | gemma2:9b | UI/UX Design | ⭐⭐⭐ | → |
| pada | ขา | gemma2:9b | DevOps/Deploy | ⭐⭐⭐ | → |
| netra | ตา (observe) | gemma2:9b | System Observation | ⭐⭐⭐ | → |
| karn | หู | gemma2:9b | Input Listening | ⭐⭐⭐ | → |
| mue | มือ | gemma2:9b | Task Execution | ⭐⭐⭐ | → |
| pran | หัวใจ | gemma2:9b | Vital Coordination | ⭐⭐⭐ | → |
| lung | ปอด | gemma2:9b | Process Breathing | ⭐⭐⭐ | → |
| sayanprasathan | ระบบประสาท | gemma2:9b | Event Network | ⭐⭐⭐ | → |

### Thai LLM Specialists
| Agent | อวัยวะ | โมเดล | ทักษะหลัก | ระดับ | เทรนด์ |
|-------|--------|-------|-----------|-------|--------|
| openthaigpt | ปัญญา-ไทย | OpenThaiGPT-8B | Thai Language | ⭐⭐⭐ | ↑ |
| pathumma | ปัญญา-ไทย | Pathumma-Qwen3-8B | Thai Reasoning | ⭐⭐⭐ | ↑ |
| typhoon | ปัญญา-ไทย | Typhoon-S-8B | Thai Generation | ⭐⭐⭐ | ↑ |
| thalle | ปัญญา-ไทย | THaLLE-0.2-8B | Thai + English | ⭐⭐⭐ | ↑ |

### Cloud Specialists
| Agent | อวัยวะ | โมเดล | ทักษะหลัก | ระดับ | เทรนด์ |
|-------|--------|-------|-----------|-------|--------|
| nemotron | สมอง-คลาวด์ | nemotron-3-super | Complex Reasoning | ⭐⭐⭐⭐⭐ | ↑ |
| gemma4-cloud | สมอง-คลาวด์ | gemma4:31b | Multimodal Tasks | ⭐⭐⭐⭐ | ↑ |
```

**A4.** แสดง Right Model routing guide (ดู SECTION ROUTING ด้านล่าง)

---

### STEP B — filter ตาม tier

**B1.** อ่าน INDEX.md เพื่อดูรายชื่อ agents ในแต่ละ tier

**B2.** Map tier argument:
- `--tier 0` → แสดงเฉพาะ jit
- `--tier 1` → แสดงเฉพาะ soma
- `--tier 2` → แสดงเฉพาะ innova, lak, neta
- `--tier 3` → แสดงเฉพาะ vaja, chamu, rupa, pada, netra, karn, mue, pran, lung, sayanprasathan
- `--tier thai` → แสดงเฉพาะ openthaigpt, pathumma, typhoon, thalle
- `--tier cloud` → แสดงเฉพาะ nemotron, gemma4-cloud

**B3.** แสดงตารางเฉพาะ agents ที่ตรงกับ tier ที่เลือก (ใช้ format เดียวกับ Step A)

---

### STEP C — โปรไฟล์เต็มของ agent

**C1.** ค้นหาชื่อ agent จาก argument (เปรียบเทียบ case-insensitive)

**C2.** ตรวจสอบว่าไฟล์มีอยู่ที่:
```
C:\Users\MDES-DEV-NB\Jit\ψ\memory\agents\[agent-name].md
```

**C3a.** ถ้าไฟล์มีอยู่ → อ่านและแสดงเนื้อหาทั้งหมดของไฟล์นั้น verbatim

**C3b.** ถ้าไฟล์ไม่มี → แสดง:
```
## [agent-name] — ยังไม่มีโปรไฟล์

ข้อมูลจาก INDEX:
[แสดงข้อมูลพื้นฐานจาก INDEX.md สำหรับ agent นั้น]

สร้างโปรไฟล์:
ใช้ template จาก: C:\Users\MDES-DEV-NB\Jit\ψ\memory\agents\_templates\agent-profile.md
บันทึกไปที่: C:\Users\MDES-DEV-NB\Jit\ψ\memory\agents\[agent-name].md
```

---

## SECTION ROUTING — Right Model for Right Task

แสดงส่วนนี้ต่อท้ายตารางสรุปเสมอ:

```
## คู่มือเลือก Agent ที่ถูกต้อง (Right Model for Right Task)

### งานหนัก — ต้องคิดลึก
- **jit** (qwen2.5:72b) — System-wide decision, orchestration ข้ามหลาย agents
- **soma** (qwen2.5:72b) — Architectural decision, CTO-level trade-off analysis
- **nemotron** (cloud) — Complex reasoning ที่ต้องการ reasoning chain ยาว

### งาน Code
- **innova** (qwen2.5-coder) — Lead development, Oracle queries, creative code
- **lak** (qwen2.5-coder) — Architecture design, solution blueprints
- **neta** (qwen2.5-coder) — Code review, quality gate

### งานภาษาไทย
- **typhoon** — Thai text generation, ร้อยแก้วภาษาไทย
- **pathumma** — Thai reasoning, ตอบคำถามเป็นภาษาไทย
- **openthaigpt** — Thai NLP, วิเคราะห์ข้อความไทย
- **thalle** — Thai + English bilingual tasks

### งาน Cloud/หนัก
- **gemma4-cloud** (31b) — Multimodal tasks, vision + text
- **nemotron** — High-quality reasoning ที่ต้องการ accuracy สูง

### งาน Operational (Tier 3)
- **vaja** — การสื่อสาร, report drafting
- **chamu** — QA, test cases, bug detection
- **rupa** — UI mockup, design feedback
- **pada** — Deploy, infrastructure tasks
- **netra** — System monitoring, observation
- **karn** — Listening, event capture
- **mue** — Task execution, file operations
- **pran** — Health monitoring, vital signs
- **lung** — Process management
- **sayanprasathan** — Event routing, nerve signals

### กฎทอง
1. Tier 0-1 (72b models) → เฉพาะงาน strategic ที่ต้องการ deep reasoning
2. Tier 2 (coder models) → งาน code ทุกประเภท
3. Tier 3 (9b models) → งาน operational ที่ชัดเจน ไม่ซับซ้อน
4. Thai LLMs → งานที่ต้องการภาษาไทยคุณภาพสูง
5. Cloud → งานที่ต้องการ accuracy สูงสุดหรือ multimodal
```

---

## ข้อมูล Agent Registry (Static Reference)

ใช้ข้อมูลนี้เมื่อไม่มีไฟล์โปรไฟล์หรือ INDEX ไม่สมบูรณ์:

| Agent | Tier | อวัยวะ | โมเดล | Provider |
|-------|------|--------|-------|----------|
| jit | 0 | จิต | qwen3.5:27b | MDES Ollama |
| soma | 1 | สมอง | qwen3.5:27b | MDES Ollama |
| innova | 2 | จิตใจ | qwen2.5-coder:32b | MDES Ollama |
| lak | 2 | กระดูกสันหลัง | qwen2.5-coder:32b | MDES Ollama |
| neta | 2 | ตา (review) | qwen2.5-coder:32b | MDES Ollama |
| vaja | 3 | ปาก | qwen3.5:9b | MDES Ollama |
| chamu | 3 | จมูก | qwen3.5:9b | MDES Ollama |
| rupa | 3 | รูปลักษณ์ | qwen3.5:9b | MDES Ollama |
| pada | 3 | ขา | qwen3.5:9b | MDES Ollama |
| netra | 3 | ตา (observe) | qwen3.5:9b | MDES Ollama |
| karn | 3 | หู | qwen3.5:9b | MDES Ollama |
| mue | 3 | มือ | qwen3.5:9b | MDES Ollama |
| pran | 3 | หัวใจ | qwen3.5:9b | MDES Ollama |
| lung | 3 | ปอด | qwen3.5:9b | MDES Ollama |
| sayanprasathan | 3 | ระบบประสาท | qwen3.5:9b | MDES Ollama |
| openthaigpt | Thai | ปัญญา-ไทย | OpenThaiGPT-8B | thaillm-gang |
| pathumma | Thai | ปัญญา-ไทย | Pathumma-Qwen3-8B | thaillm-gang |
| typhoon | Thai | ปัญญา-ไทย | Typhoon-S-8B | thaillm-gang |
| thalle | Thai | ปัญญา-ไทย | THaLLE-0.2-8B | thaillm-gang |
| nemotron | Cloud | สมอง-คลาวด์ | nemotron-3-super | soma/cloud |
| gemma4-cloud | Cloud | สมอง-คลาวด์ | gemma4:31b | soma/cloud |

---

## หมายเหตุ

- **Path โปรไฟล์**: `C:\Users\MDES-DEV-NB\Jit\ψ\memory\agents\[name].md`
- **Path INDEX**: `C:\Users\MDES-DEV-NB\Jit\ψ\memory\agents\INDEX.md`
- **Template**: `C:\Users\MDES-DEV-NB\Jit\ψ\memory\agents\_templates\agent-profile.md`
- ถ้าไฟล์ไม่มีให้แสดงข้อมูล static จากตารางด้านบน
- อ่านจริงจากไฟล์เสมอเมื่อมี — ไม่เดาข้อมูล

---
name: gang
description: "Skill workflow for gang."
---

# Skill: /gang — ระบบ Multi-Agent Gangs

> "ช่างฝีมือจัดการฝูง — ประสานงานหลาย agent ให้ทำงานเป็นทีม"

## ภาพรวม

`/gang` เป็น skill สำหรับโต้ตอบและจัดการระบบ multi-agent-gangs — กรอบการทำงานแบบ demonstration ที่ประกอบด้วย 4 gangs เฉพาะทาง ได้แก่ DevOps, CI/CD, Jarvis และ Special

## Endpoint หลัก

**mdes.ollama** — endpoint สำหรับทุก gang operations

```bash
# ตั้งค่า endpoint
$env:OLLAMA_HOST = "https://mdes.ollama"
```

## คำสั่งที่ใช้ได้

### /gang

แสดงภาพรวมของระบบ gang ทั้งหมด

```bash
/gang
```

### /gang list

แสดงรายการ gangs ทั้งหมดที่มีอยู่ในระบบ

```bash
/gang list
```

**gangs ที่มีอยู่:**
- `a-devops` — DevOps Auto-Repair (ตรวจจับ, วิเคราะห์, แก้ไข, ทดสอบ และ deploy ปัญหาของระบบ)
- `b-ci` — CI/CD Quality Gate (ตรวจสอบ PR, linting, security scanning และจัดการ pipeline)
- `c-jarvis` — Jarvis Autonomous Assistant (ผู้ช่วยที่หันหน้าเข้าหาผู้ใช้ ตีความคำสั่งและทำงานอย่างปลอดภัย)
- `d-special` — Special Gang from นาย (การวางแผนเชิงกลยุทธ์และการ optimize)

### /gang activate <gang>

เปิดใช้งาน gang เฉพาะ

```bash
/gang activate a-devops
/gang activate b-ci
/gang activate c-jarvis
/gang activate d-special
```

**ตัวอย่าง:**
```bash
/gang activate a-devops    # เปิดใช้งาน DevOps Auto-Repair gang
/gang activate c-jarvis    # เปิดใช้งาน Jarvis Assistant
```

### /gang run <gang> <script>

รัน script จาก gang เฉพาะ

```bash
/gang run <gang> <script>
```

**ตัวอย่าง:**
```bash
/gang run a-devops monitor    # รัน monitor agent ของ DevOps gang
/gang run b-ci linter         # รัน linter agent ของ CI/CD gang
/gang run c-jarvis frontline  # รัน frontline agent ของ Jarvis gang
/gang run d-special boss_orchestrator  # รัน boss orchestrator ของ Special gang
```

**Scripts ที่มีอยู่ในแต่ละ gang:**

| Gang | Scripts |
|------|---------|
| a-devops | `monitor.sh`, `analyzer.sh`, `fixer.sh` |
| b-ci | `linter.sh`, `reviewer.sh`, `autopatch.sh` |
| c-jarvis | `frontline.sh`, `executor.sh`, `safety_gate.sh` |
| d-special | `boss_orchestrator.sh`, `strategic_analyst.sh`, `resource_manager.sh`, `jit_agent.sh` |

### /gang status

แสดงสถานะของ gangs ทั้งหมด

```bash
/gang status
```

### /gang logs <gang>

แสดง logs จาก gang เฉพาะ

```bash
/gang logs <gang>
```

**ตัวอย่าง:**
```bash
/gang logs c-jarvis    # แสดง logs ของ Jarvis gang
/gang logs a-devops    # แสดง logs ของ DevOps gang
```

### /gang demo

รัน script demo ของระบบ

```bash
/gang demo
```

## Model Fallback to Auto-Model

หากโมเดลหลักไม่ทำงาน ให้ใช้ `/auto-model`:

```bash
/auto-model              # ค้นหาโมเดลที่ทำงานได้อัตโนมัติ
/auto-model --current   # แสดงโมเดลปัจจุบัน
/auto-model --fallback  # ทดสอบ fallback providers
```

### Fallback Chain:

1. nemotron-3-super:cloud → mdes.ollama
2. minimax-m2.5:cloud → mdes.ollama
3. deepseek-v4-flash:cloud → mdes.ollama
4. หากทุกอย่างล้มเหลว → codex (OpenAI)
5. หาก codex ล้มเหลว → gpt-pro
6. หาก gpt-pro ล้มเหลว → github-copilot

## GSD Workflow Skills Integration

### ทำงานร่วมกับ GSD skills:

- **/gsd-execute-phase** — ใช้ gang เป็น execution engine
- **/gsd-manager** — ใช้ gang สำหรับ task management
- **/gsd-code-review** — ใช้ b-ci gang สำหรับ review
- **/gsd-debug** — ใช้ a-devops gang สำหรับ debugging
- **/gsd-spike** — ใช้ d-special gang สำหรับ investigation

### ตัวอย่างการใช้งานใน GSD workflow:

```bash
# เริ่ม GSD execute phase ด้วย gang
/gang activate b-ci
/gang run b-ci linter

# ใช้ auto-model ก่อนเริ่มงาน
/auto-model

# รัน devops monitoring
/gang activate a-devops
/gang run a-devops monitor
```

## ตัวอย่างการใช้งาน

### ตัวอย่างที่ 1: ตรวจสอบสุขภาพระบบด้วย DevOps Gang

```bash
# เปิดใช้งาน DevOps gang
/gang activate a-devops

# รันการตรวจสอบระบบ
/gang run a-devops monitor

# รันการวิเคราะห์ระบบ
/gang run a-devops analyzer

# รันการแก้ไขปัญหา
/gang run a-devops fixer
```

### ตัวอย่างที่ 2: ตรวจสอบคุณภาพก่อน Deploy ด้วย CI/CD Gang

```bash
# เปิดใช้งาน CI/CD gang
/gang activate b-ci

# รันการตรวจสอบคุณภาพโค้ด
/gang run b-ci linter

# รันการ review
/gang run b-ci reviewer

# รัน autopatch
/gang run b-ci autopatch
```

### ตัวอย่างที่ 3: ขอความช่วยเหลือจาก Jarvis

```bash
# เปิดใช้งาน Jarvis gang
/gang activate c-jarvis

# รัน frontline agent
/gang run c-jarvis frontline

# รัน safety gate
/gang run c-jarvis safety_gate
```

### ตัวอย่างที่ 4: การวางแผนเชิงกลยุทธ์ด้วย Special Gang

```bash
# เปิดใช้งาน Special gang
/gang activate d-special

# รัน strategic analyst
/gang run d-special strategic_analyst

# รัน resource manager
/gang run d-special resource_manager

# รัน boss orchestrator
/gang run d-special boss_orchestrator
```

## รายละเอียดทางเทคนิค

### โครงสร้างไดเรกทอรี

```
multi-agent-gangs/
├── CLAUDE.md
├── README.md
├── demo.sh
├── config/
│   ├── model_mappings.json
│   └── prompt_templates.json
├── gangs/
│   ├── a_devops/
│   ├── b_ci/
│   ├── c_jarvis/
│   └── d_special/
├── logs/
├── pids/
├── psi/
└── script/
    ├── gang_selector/
    ├── gang_a_devops/
    ├── gang_b_ci/
    ├── gang_c_jarvis/
    ├── gang_d_special/
    └── monitor_tui.sh
```

### Gang Selector

การเลือกและเปิดใช้งาน gang ผ่าน script:

```bash
./script/gang_selector/gang-selector.sh list        # แสดงรายการ gangs
./script/gang_selector/gang-selector.sh a-devops     # เปิดใช้งาน DevOps
./script/gang_selector/gang-selector.sh b-ci        # เปิดใช้งาน CI/CD
./script/gang_selector/gang-selector.sh c-jarvis     # เปิดใช้งาน Jarvis
./script/gang_selector/gang-selector.sh d-special   # เปิดใช้งาน Special
```

### การตั้งค่า Model

ระบบใช้ **mdes.ollama** เป็น primary endpoint พร้อม fallback mechanism สำหรับความน่าเชื่อถือ

- **Model Mappings**: `config/model_mappings.json`
- **Prompt Templates**: `config/prompt_templates.json`

### ความปลอดภัย

- Safety Gate agents สำหรับ operations ที่มีความเสี่ยงสูง
- Sandbox execution สำหรับคำสั่งที่อาจเป็นอันตราย
- ต้องยืนยันสำหรับการกระทำที่ทำลายล้าง
- ใช้ `/auto-model` เพื่อตรวจสอบโมเดลก่อนเริ่มงาน

## หมายเหตุ

นี่คือระบบ demonstration ที่แสดงแนวคิดของ multi-agent gangs ที่มีบทบาทเฉพาะทาง สำหรับการใช้งานจริงใน production จะต้อง:

- ใช้ mdes.ollama เป็น endpoint หลัก
- เพิ่มการ integrate Ollama API จริง
- เพิ่ม persistent storage สำหรับ agent memories และ learnings
- เพิ่มการ reasoning และ task execution จริง
- เพิ่ม monitoring และ logging systems
- เพิ่ม authentication และ authorization
- ผสานกับ GSD workflow skills สำหรับ end-to-end operations
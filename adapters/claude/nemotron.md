<!-- skill-id: nemotron -->
<!-- source-path: nemotron -->
<!-- source-file: C:/Users/MDES-DEV-NB/.claude/skills/nemotron/SKILL.md -->
<!-- runtime: claude -->

# /nemotron — Nemotron Sub-Agent Skill

> "ช่างฝีมือประสานพลัง NVIDIA — สร้าง sub-agent ด้วยปัญญา"

## ภาพรวม

`/nemotron` คือ skill ที่ช่วยให้สามารถเรียกใช้ sub-agent ที่ใช้ nemotron-3-super:cloud เป็น AI engine หลัก สำหรับงาน multi-agent orchestration ที่ทรงพลัง

## การใช้งาน

```
/nemotron <prompt>           # รัน prompt ด้วย nemotron-3-super:cloud
/nemotron --agent <prompt>  # เหมือนข้างบน (explicit)
/nemotron --chat            # เริ่มต้น interactive chat กับ nemotron
/nemotron --info            # แสดงข้อมูล model
```

## Endpoint หลัก

**mdes.ollama** — endpoint หลักสำหรับทุกการทำงาน

```
OLLAMA_HOST=https://mdes.ollama
```

## Token Limit Awareness

nemotron-3-super มี context window และ token limit ที่ต้องตรวจสอบ:

| Model | Context | Output | สถานะ |
|-------|---------|--------|-------|
| nemotron-3-super:cloud | 128K | 8K | พร้อมใช้งาน |
| nemotron-3-nano:cloud | 4K | 4K | fallback ย่อย |

**การตรวจสอบ token:**
- ก่อนส่ง prompt ยาว ตรวจสอบความยาวก่อน
- ใช้ `--verbose` เพื่อดู token usage
- หากเกิน limit ให้ fallback ไปยัง `nemotron-3-nano:cloud`

## Fallback to Auto-Model

หาก nemotron ไม่ทำงาน ให้ใช้ `/auto-model`:

```
/auto-model              # ค้นหาโมเดลที่ทำงานได้อัตโนมัติ
/auto-model --current   # แสดงโมเดลปัจจุบัน
```

Fallback Chain:
1. nemotron-3-super:cloud → mdes.ollama
2. หากล้มเหลว → minimax-m2.5:cloud
3. หากล้มเหลว → deepseek-v4-flash:cloud
4. หากทุกอย่างล้มเหลว → codex (OpenAI)

## GSD System Integration

### ทำงานร่วมกับ GSD workflow skills:

- **/gsd-execute-phase** — ใช้ nemotron เป็น executor agent
- **/gsd-code-review** — ใช้ nemotron สำหรับ code review
- **/gsd-debug** — ใช้ nemotron สำหรับ debugging
- **/gsd-spike** — ใช้ nemotron สำหรับ spike investigation

### การเรียกใช้ใน GSD workflow:

```
# ใน GSD phase execution
/nemotron --agent ทำการ execute phase ตาม task ที่ได้รับ

# ใน code review
/nemotron ตรวจสอบโค้ดที่เปลี่ยนแปลงและให้ feedback
```

## Nemotron-3-Super:Cloud คืออะไร?

**Nemotron-3-Super** คือ AI model จาก NVIDIA ที่ออกแบบมาเพื่อการใช้งานในองค์กรและ multi-agent workflows มีความสามารถในการ:

- **Code Generation** — เขียนโค้ดคุณภาพสูงในหลายภาษา
- **Reasoning** — ความสามารถในการคิดวิเคราะห์เชิงลึก
- **Tool Use** — การใช้งาน tools และ functions ได้อย่างมีประสิทธิภาพ
- **Multi-turn Conversation** — สนทนาต่อเนื่องได้ดี
- **Cloud-based** — ใช้งานผ่าน mdes.ollama endpoint มีความยืดหยุ่นในการ scale

## ตัวอย่างการใช้งาน

### 1. รัน prompt พื้นฐาน

```
/nemotron วิเคราะห์โครงสร้างโปรเจกต์นี้และเสนอแนวทางการ refactor
```

### 2. สร้าง sub-agent สำหรับงานเฉพาะทาง

```
/nemotron --agent เขียน unit tests สำหรับฟังก์ชัน authentication ในไฟล์ auth.py
```

### 3. ดูข้อมูล model

```
/nemotron --info
```

## การทำงานกับ Multi-Agent-Gangs

Skill นี้ถูกออกแบบให้ทำงานร่วมกับระบบ multi-agent-gangs โดย:

- **Spawn sub-agent** ด้วย nemotron model เพื่อแบ่งเบาภาระงาน
- **Delegate complex tasks** ให้ nemotron agent จัดการ
- **Parallel execution** รันหลาย agent พร้อมกันได้
- **ใช้ mdes.ollama** เป็น endpoint หลัก

## หมายเหตุทางเทคนิค

- Model parameter อาจยังไม่ได้รับการสนับสนุนโดยตรงใน Agent tool แต่ skill นี้เตรียมโครงสร้างไว้สำหรับการใช้งานในอนาคต
- ในกรณีที่ต้องการใช้ nemotron จริงๆ อาจต้องใช้งานผ่าน MCP server หรือ API ที่รองรับ
- ติดต่อ BigBoss เพื่อขอข้อมูลเพิ่มเติมเกี่ยวกับการตั้งค่า nemotron API
- **Token usage ต้องตรวจสอบก่อนส่ง** เพื่อหลีกเลี่ยง context overflow

## ข้อมูลเพิ่มเติม

- **Author**: Jit Oracle (ช่างฝีมือด้าน multi-agent)
- **Created**: 2026-05-07
- **Purpose**: Multi-agent workflow orchestration ด้วย NVIDIA AI
- **Endpoint**: mdes.ollama
- **Integration**: GSD workflow skills + multi-agent-gangs
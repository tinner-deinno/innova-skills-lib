---
name: model-claude
description: "Skill workflow for model-claude."
---

# Skill: /model-claude — ใช้ Claude API โดยตรง (session ปัจจุบัน)

> "ปัญญา Anthropic — ใช้ Claude ในงานที่ต้องการ reasoning ลึก หรือ coding ระดับสูง"

## ภาพรวม

`/model-claude` เป็น meta-skill สำหรับ clarify ว่า BigBoss ต้องการใช้ Claude model ตัวใด
สำหรับงานปัจจุบัน — session นี้รัน `claude-sonnet-4-6` อยู่แล้ว

## การใช้งาน

```
/model-claude                          — แสดงโมเดลปัจจุบัน + routing guidance
/model-claude [งาน]                    — วิเคราะห์งานและแนะนำ Claude model ที่เหมาะสม
/model-claude --model [sonnet|opus|haiku] [งาน]  — ระบุ model ที่ต้องการ
/model-claude --compare                — เปรียบเทียบ 3 models
```

## Claude Models

| Model | Model ID | เชี่ยวชาญ | ราคา |
|-------|----------|-----------|------|
| **Sonnet** | claude-sonnet-4-6 | Main work / Coding | ปานกลาง |
| **Opus** | claude-opus-4-5 | Deep reasoning / Architecture | สูง |
| **Haiku** | claude-haiku-4-5 | Fast checks / Simple tasks | ต่ำ |

## Routing Guidance

```
งานประเภท: Architecture / Design decision / Complex analysis
→ OPUS — reasoning ลึกที่สุด คุ้มค่าสำหรับงานสำคัญ

งานประเภท: Main coding / Code review / Feature dev / Debugging
→ SONNET (claude-sonnet-4-6) — DEFAULT — ดีที่สุดสำหรับ coding

งานประเภท: Quick check / Format / Simple summary / Grep result
→ HAIKU — เร็ว ราคาถูก เหมาะงานเบา

งานปัจจุบัน: ใช้ SONNET (session นี้รันอยู่แล้ว)
```

## สถานะโมเดลปัจจุบัน

```
Session นี้: claude-sonnet-4-6
Provider:    Anthropic Claude API
บิล:         Anthropic (ใช้ ANTHROPIC_API_KEY)
Context:     200K tokens
```

## วิธีเปลี่ยน Model

Claude Code ไม่สามารถเปลี่ยน model ระหว่าง session ได้อัตโนมัติ
BigBoss ต้องเปลี่ยนเองตามวิธีต่อไปนี้:

**วิธีที่ 1: ผ่าน CLI flag**
```bash
claude --model claude-opus-4-5
claude --model claude-haiku-4-5
```

**วิธีที่ 2: ผ่าน settings.json**
```bash
# ดู settings ปัจจุบัน
cat ~/.claude/settings.json | python3 -m json.tool

# แก้ไข model
# ใน settings.json: "model": "claude-opus-4-5"
```

**วิธีที่ 3: ผ่าน /config**
```
/config
→ เลือก model settings
```

## ตัวอย่างการใช้งาน

```
/model-claude
→ Model ปัจจุบัน: claude-sonnet-4-6
→ Routing guidance แสดง...

/model-claude ออกแบบ architecture ระบบ multi-agent
→ แนะนำ: claude-opus-4-5 (architecture decision)
→ เหตุผล: ต้องการ deep reasoning, complex trade-off analysis
→ วิธีเปลี่ยน: claude --model claude-opus-4-5

/model-claude --model haiku ตรวจสอบ syntax ไฟล์นี้
→ แนะนำ: ใช้ Haiku สำหรับงานนี้
→ วิธีเปลี่ยน: claude --model claude-haiku-4-5

/model-claude --compare
→ แสดงตารางเปรียบเทียบ 3 models
```

## เปรียบเทียบ Models (--compare)

```
┌─────────────────────────────────────────────────────────────────────┐
│  Claude Model Comparison                                             │
├──────────┬────────────────┬──────────────┬───────────┬─────────────┤
│  Model   │  Model ID      │  Best For    │  Speed    │  Cost       │
├──────────┼────────────────┼──────────────┼───────────┼─────────────┤
│  Haiku   │ haiku-4-5      │ Quick tasks  │ เร็วมาก  │ ถูก (~3x)   │
│  Sonnet  │ sonnet-4-6     │ Main coding  │ เร็ว      │ ปานกลาง     │
│  Opus    │ opus-4-5       │ Deep reason  │ ช้ากว่า   │ แพง (~5x)   │
└──────────┴────────────────┴──────────────┴───────────┴─────────────┘

Current session: claude-sonnet-4-6 (SONNET)
บิล: Anthropic Claude API — ใช้ ANTHROPIC_API_KEY
```

## เมื่อควรใช้ Claude แทน Local/MDES/ThaiLLM

| สถานการณ์ | แนะนำ |
|-----------|-------|
| งาน code ระดับสูง / complex refactor | Claude Sonnet |
| Architecture decision สำคัญ | Claude Opus |
| งานภาษาไทยทั่วไป ราคาถูก | MDES Ollama (gemma4:26b) |
| งานภาษาไทยเฉพาะทาง (กฎหมาย/ราชการ) | ThaiLLM |
| ข้อมูลลับ / offline | Local Ollama |
| Quick check / grep / format | Claude Haiku |

## คำสั่งที่รันจริง

```bash
# ดู model ปัจจุบัน
claude --version

# ดู settings
cat ~/.claude/settings.json

# เริ่ม session ใหม่ด้วย Opus
claude --model claude-opus-4-5

# เริ่ม session ใหม่ด้วย Haiku
claude --model claude-haiku-4-5

# ดู token usage session ปัจจุบัน
/cost-report
```

## หมายเหตุสำคัญ

- `/model-claude` ไม่เปลี่ยน model ใน session ปัจจุบัน — แค่แสดง guidance
- การเปลี่ยน model ต้องเริ่ม session ใหม่ หรือแก้ settings.json
- บิล Claude API ตรงไปที่ Anthropic — ดูใน Anthropic Console
- Token ที่ใช้ใน session นี้นับรวมใน Claude usage

## ข้อมูลเพิ่มเติม

- **Author**: Jit Oracle
- **Created**: 2026-05-23
- **Current Model**: claude-sonnet-4-6
- **Provider**: Anthropic
- **Billing**: Anthropic API (ANTHROPIC_API_KEY)
- **Related**: `/model-thaiLLM`, `/model-MDES`, `/model-local`
- **Cost visibility**: `/cost-report`

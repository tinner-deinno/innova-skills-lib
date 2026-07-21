---
name: model-copilot
description: "Skill workflow for model-copilot."
---

# Skill: /model-copilot — ส่งงานผ่าน GitHub Copilot API

> "ปัญญา GitHub — Copilot เข้าถึง GPT-4o + Claude + o1 ผ่าน GitHub subscription"

## ภาพรวม

`/model-copilot` ส่งงานผ่าน GitHub Copilot Chat API
ใช้ `GITHUB_COPILOT_TOKEN` (GitHub PAT with `copilot` scope) จาก `~/Jit/.env`

**จุดเด่น**: เข้าถึง GPT-4o, Claude 3.5/3.7, o1, o3-mini ผ่าน GitHub Copilot subscription เดียว

## การใช้งาน

```
/model-copilot [prompt]                               — GPT-4o (default)
/model-copilot --model claude-3.5-sonnet [prompt]    — Claude via Copilot
/model-copilot --model o3-mini [prompt]              — OpenAI reasoning
/model-copilot --list                                — แสดงโมเดลทั้งหมด
/model-copilot --status                              — ทดสอบ token + connection
```

## โมเดลที่รองรับ (GitHub Models API — account นี้)

| Model ID | Provider | เชี่ยวชาญ | เมื่อใช้ |
|----------|----------|-----------|----------|
| `gpt-4o` | OpenAI | ทั่วไป / ไทย | **Default** |
| `gpt-4o-mini` | OpenAI | เร็ว / ราคาถูก | งานง่าย, summary |
| `Meta-Llama-3.1-405B-Instruct` | Meta | Reasoning ลึก | งานที่ต้องการ reasoning |
| `Meta-Llama-3.1-8B-Instruct` | Meta | เร็ว / เบา | งานง่ายเร็ว |

> **หมายเหตุ**: โมเดลที่มีขึ้นกับ GitHub account และ marketplace ที่ได้รับอนุญาต
> รัน `/model-copilot --list` เพื่อดูรายการล่าสุด

## Auth Flow

```
GITHUB_COPILOT_TOKEN (GitHub PAT — standard read scope ก็พอ)
    ↓ ใช้ตรงๆ เป็น Bearer token
POST https://models.inference.ai.azure.com/chat/completions
```

> endpoint: `models.inference.ai.azure.com` — GitHub Models Marketplace API

## ขั้นตอนการรัน

**1. ระบุโมเดลอัตโนมัติ:**

```bash
TASK="[งานจากผู้ใช้]"
MODEL="gpt-4o"  # default

if [[ "$TASK" =~ (code|โค้ด|debug|review|refactor|python|typescript) ]]; then
  MODEL="claude-3.5-sonnet"   # Claude ดีกว่าสำหรับ coding
elif [[ "$TASK" =~ (math|proof|logic|คิด|วิเคราะห์|reason) ]]; then
  MODEL="o3-mini"
elif [[ "$TASK" =~ (สรุป|สั้น|fast|quick|translate) ]]; then
  MODEL="gpt-4o-mini"
fi

echo "→ เลือก: $MODEL"
```

**2. เรียก GitHub Copilot:**

```bash
CURRENT_AGENT="jit" CURRENT_SKILL="model-copilot" \
  bash ~/Jit/limbs/copilot.sh ask "$TASK" "$MODEL"
```

**3. แสดงผลพร้อม attribution:**

```
[ผลลัพธ์]

— ตอบโดย gpt-4o (GitHub Copilot)
```

## Configuration

**`.env` ที่ต้องใส่:**
```bash
GITHUB_COPILOT_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
# Token ต้องมี scope: copilot
# สร้างที่: github.com/settings/tokens → New token → copilot scope
```

## ตัวอย่างการใช้งาน

```
/model-copilot อธิบาย architecture ของ มนุษย์ Agent
→ gpt-4o (default)

/model-copilot --model claude-3.5-sonnet review โค้ดนี้: [โค้ด]
→ Claude 3.5 Sonnet (ดีที่สุดสำหรับ code review)

/model-copilot --model o3-mini หา bug ใน logic นี้
→ o3-mini (reasoning)

/model-copilot --status
→ ทดสอบ token exchange + chat
```

## Error Handling

```bash
# Token ไม่มี copilot scope:
❌ Copilot HTTP 403: Not authorized for GitHub Copilot

# Token หมดอายุ:
❌ Copilot HTTP 401: Bad credentials

# ไม่มี Copilot subscription:
❌ Copilot HTTP 402: GitHub Copilot is not enabled

# แก้ไข:
# 1. ตรวจ scope: github.com/settings/tokens → ดูว่ามี copilot checkbox
# 2. ตรวจ subscription: github.com/settings/copilot
```

## Token Logging

ทุก call จะ log ลง `~/Jit/ψ/telemetry/token_log.jsonl`:
```json
{"timestamp":"...","source":"github_copilot","model":"gpt-4o","prompt_tokens":150}
```

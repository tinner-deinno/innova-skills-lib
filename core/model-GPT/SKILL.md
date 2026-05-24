# Skill: /model-GPT — ส่งงานไปยัง OpenAI GPT API

> "ปัญญา OpenAI — GPT-4o สำหรับงานทั่วไป, o1/o3 สำหรับ reasoning ลึก"

## ภาพรวม

`/model-GPT` ส่งงานไปยัง OpenAI API โดยตรง
ใช้ `OPENAI_API_KEY` จาก `~/Jit/.env`
รองรับ GPT-4o, GPT-4o-mini, GPT-4-turbo, o1-mini, o3-mini

## การใช้งาน

```
/model-GPT [prompt]                        — GPT-4o (default)
/model-GPT --model gpt-4o-mini [prompt]   — ระบุโมเดล
/model-GPT --model o1 [prompt]            — OpenAI reasoning
/model-GPT --list                         — แสดงรายการโมเดล
/model-GPT --status                       — ทดสอบ connection
```

## โมเดลที่มี

| Model | เชี่ยวชาญ | เมื่อใช้ |
|-------|-----------|----------|
| `gpt-4o` | ทั่วไป / สมดุล | **Default** — ดีที่สุดสำหรับงานทั่วไป |
| `gpt-4o-mini` | เร็ว / ราคาถูก | งานง่าย, summary, format |
| `gpt-4-turbo` | ยาว / context 128K | งานที่ต้องการ context ยาว |
| `o1` | Reasoning ลึก | Math, logic, planning ซับซ้อน |
| `o3-mini` | Reasoning เร็ว | Reasoning แต่ต้องการความเร็ว |

## Auto-routing (เมื่อไม่ระบุ --model)

```
งานมีคำว่า:  math, proof, logic, plan, architect, design, reason, คิด, วิเคราะห์
→ o1 หรือ o3-mini

งานมีคำว่า:  สรุป, format, translate, list, quick, fast, สั้น
→ gpt-4o-mini

งานยาว หรือ context > 32K tokens:
→ gpt-4-turbo (128K context)

ทั่วไป:
→ gpt-4o (DEFAULT)
```

## ขั้นตอนการรัน

**1. ระบุโมเดลอัตโนมัติ:**

```bash
TASK="[งานจากผู้ใช้]"
MODEL="gpt-4o"  # default

if [[ "$TASK" =~ (math|proof|logic|plan|architect|reason|คิด|วิเคราะห์) ]]; then
  MODEL="o3-mini"
elif [[ "$TASK" =~ (สรุป|format|translate|quick|fast|สั้น|simple) ]]; then
  MODEL="gpt-4o-mini"
fi

echo "→ เลือก: $MODEL"
```

**2. เรียก OpenAI:**

```bash
CURRENT_AGENT="jit" CURRENT_SKILL="model-GPT" \
  bash ~/Jit/limbs/openai.sh ask "$TASK" "$MODEL"
```

**3. แสดงผลพร้อม attribution:**

```
[ผลลัพธ์จาก GPT]

— ตอบโดย gpt-4o (OpenAI)
```

## Configuration

**`.env` ที่ต้องใส่:**
```bash
OPENAI_API_KEY=sk-proj-...
OPENAI_DEFAULT_MODEL=gpt-4o    # optional, default คือ gpt-4o
OPENAI_BASE_URL=https://api.openai.com/v1  # optional
```

## ตัวอย่างการใช้งาน

```
/model-GPT อธิบาย multi-agent systems ภาษาไทย
→ gpt-4o (default)
→ bash ~/Jit/limbs/openai.sh ask "อธิบาย multi-agent..."

/model-GPT --model o3-mini วิเคราะห์ algorithm นี้และหาจุดอ่อน
→ o3-mini (reasoning task)

/model-GPT --model gpt-4o-mini สรุปข้อความนี้
→ gpt-4o-mini (fast, cheap)

/model-GPT --status
→ ทดสอบ connection และแสดงสถานะ
```

## Error Handling

```bash
# ถ้า OPENAI_API_KEY ว่าง:
❌ OPENAI_API_KEY ว่างเปล่า
❌ กรุณาใส่ใน ~/Jit/.env: OPENAI_API_KEY=sk-...

# ถ้า quota หมด / invalid key:
❌ OpenAI HTTP 401: Incorrect API key provided
❌ OpenAI HTTP 429: Rate limit exceeded

# แก้ไข:
# 1. ตรวจสอบ ~/Jit/.env
# 2. ดู usage ที่ platform.openai.com/usage
```

## Token Logging

ทุก call จะ log ลง `~/Jit/ψ/telemetry/token_log.jsonl`:
```json
{"timestamp":"...","source":"openai","model":"gpt-4o","prompt_tokens":150,"completion_tokens":200}
```

# Skill: /model-MDES — ส่งงานไปยัง MDES Ollama

> "วิริยะ — ความพยายามที่ถูกทิศทาง ผ่าน MDES Ollama ของทีม"

## ภาพรวม

`/model-MDES` ส่งงานไปยัง MDES Ollama endpoint (`https://ollama.mdes-innova.online`)
ซึ่งเป็น infrastructure ภายในของ MDES Innova — เร็ว, รองรับภาษาไทย, และมีโมเดลหลายตัวให้เลือก

## การใช้งาน

```
/model-MDES [งาน/prompt]
/model-MDES --model [gemma4:26b|qwen2.5:72b|qwen2.5-coder|gemma2:9b] [prompt]
/model-MDES --status
```

## โมเดลที่มี

| Model | ขนาด | เชี่ยวชาญ | เมื่อใช้ |
|-------|------|-----------|----------|
| `gemma4:26b` | 26B | ภาษาไทย/ทั่วไป | **Default** — เร็วที่สุด, ดีที่สุดสำหรับภาษาไทย |
| `qwen2.5:72b` | 72B | Reasoning/วิเคราะห์ | การตัดสินใจซับซ้อน, วิเคราะห์เชิงลึก |
| `qwen2.5-coder` | — | โค้ด/เทคนิค | เขียนโค้ด, debugging, code review |
| `gemma2:9b` | 9B | งานเบา/เร็ว | งานง่าย, ต้องการความเร็วสูง |

## Auto-routing

เมื่อไม่ระบุ `--model` จะแนะนำโมเดลตามประเภทงาน:

```
ประเภทงาน: Reasoning / Architecture / Design → qwen2.5:72b
ประเภทงาน: Code / Debug / Script / Review   → qwen2.5-coder
ประเภทงาน: งานเบา / Quick / Summary         → gemma2:9b
ประเภทงาน: ทั่วไป / Thai / Default          → gemma4:26b (DEFAULT)
```

## ขั้นตอนการรัน

**1. ตรวจสอบ connection:**

```bash
bash ~/Jit/limbs/ollama.sh status
```

**2. ส่งงานไปยัง MDES Ollama:**

```bash
# Default model (gemma4:26b)
CURRENT_AGENT="jit" CURRENT_SKILL="model-MDES" \
  bash ~/Jit/limbs/ollama.sh ask "[prompt]"

# ระบุ model
# (แก้ไข model ใน JSON_BODY ของ ollama.sh หรือใช้ think command)
CURRENT_AGENT="jit" CURRENT_SKILL="model-MDES" \
  bash ~/Jit/limbs/ollama.sh think "[prompt]"
```

**3. แสดงผลพร้อม attribution:**

```
[ผลลัพธ์]

— ตอบโดย gemma4:26b (MDES Ollama)
```

## ตัวอย่างการใช้งาน

```
/model-MDES อธิบาย concept ของ multi-agent systems ภาษาไทย
→ ใช้ gemma4:26b (default, ดีสำหรับภาษาไทย)
→ bash ~/Jit/limbs/ollama.sh ask "อธิบาย concept ของ multi-agent..."

/model-MDES --model qwen2.5:72b วิเคราะห์ architecture ของระบบ
→ ใช้ qwen2.5:72b (reasoning task)

/model-MDES --model qwen2.5-coder review โค้ดนี้: [โค้ด]
→ ใช้ qwen2.5-coder (code task)

/model-MDES --status
→ ทดสอบ connection และแสดงสถานะ
```

## คำสั่งที่รันจริง

```bash
# ถามตรงๆ (gemma4:26b)
CURRENT_AGENT="jit" CURRENT_SKILL="model-MDES" \
  bash ~/Jit/limbs/ollama.sh ask "your prompt here"

# ถามพร้อม Oracle context
CURRENT_AGENT="jit" CURRENT_SKILL="model-MDES" \
  bash ~/Jit/limbs/ollama.sh think "your question" "optional extra context"

# สร้างสรรค์
CURRENT_AGENT="jit" CURRENT_SKILL="model-MDES" \
  bash ~/Jit/limbs/ollama.sh create "task description"

# แปล/อธิบาย
CURRENT_AGENT="jit" CURRENT_SKILL="model-MDES" \
  bash ~/Jit/limbs/ollama.sh translate "text to translate"

# ตรวจสอบสถานะ
bash ~/Jit/limbs/ollama.sh status

# ดู token log
cat ~/Jit/ψ/telemetry/token_log.jsonl | python3 -c "
import sys, json
for line in sys.stdin:
    e = json.loads(line)
    if e.get('source') == 'mdes_ollama':
        print(e['timestamp'], e['model'], e['total_tokens'], 'tokens')
"
```

## Telemetry

ทุกการเรียกจะบันทึกไปที่ `~/Jit/ψ/telemetry/token_log.jsonl`:
```json
{
  "timestamp": "2026-05-23T10:00:00",
  "source": "mdes_ollama",
  "model": "gemma4:26b",
  "agent": "jit",
  "skill": "model-MDES",
  "prompt_tokens": 85,
  "completion_tokens": 420,
  "total_tokens": 505
}
```

## ข้อกำหนด

- ต้องมี `OLLAMA_TOKEN` หรือ `OLLAMA_API_TOKEN` ใน `~/Jit/.env`
- ต้องเข้าถึง `https://ollama.mdes-innova.online` ได้
- `~/Jit/limbs/ollama.sh` ต้องพร้อมใช้งาน

## ข้อมูลเพิ่มเติม

- **Author**: Jit Oracle
- **Created**: 2026-05-23
- **Endpoint**: `https://ollama.mdes-innova.online`
- **Source**: `~/Jit/limbs/ollama.sh`
- **Log**: `~/Jit/ψ/telemetry/token_log.jsonl`
- **Related**: `/model-thaiLLM`, `/model-local`, `/model-claude`

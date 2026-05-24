<!-- skill-id: model-compare -->
<!-- source-path: model-compare -->
<!-- source-file: C:/Users/MDES-DEV-NB/.claude/skills/model-compare/SKILL.md -->
<!-- runtime: claude -->

# /model-compare — เปรียบเทียบโมเดล AI แบบ Side-by-Side

ส่ง prompt เดียวกันไปหลายโมเดล แล้วแสดงผลเปรียบเทียบพร้อมกัน

**Trigger**: `/model-compare <prompt>` หรือ `/model-compare --models <set> <prompt>`

---

## Usage

```
/model-compare "อธิบายหลักพุทธปรัชญา 3 ข้อสั้นๆ"
/model-compare --models mdes "เขียน Python function sort list"
/model-compare --models thaillm "สรุปข่าวเศรษฐกิจ"
/model-compare --models mdes,thaillm,claude "แก้ bug นี้: ..."
/model-compare --models all "ทดสอบทุกโมเดล"
```

---

## ขั้นตอนปฏิบัติ

### Step 1 — Parse Arguments

อ่าน args จาก invocation:

1. ถ้ามี `--models <set>` ให้ใช้ชุดโมเดลตามที่ระบุ:
   - `mdes` → gemma4:26b + qwen2.5:72b
   - `thaillm` → typhoon + openthaigpt
   - `claude` → claude-haiku-4-5 + claude-sonnet-4-6
   - `mdes,thaillm` → gemma4:26b + typhoon
   - `all` → gemma4:26b + typhoon + claude-haiku-4-5
2. Default (ไม่ระบุ `--models`) → 3 โมเดล: gemma4:26b (MDES) + typhoon (ThaiLLM) + claude-haiku-4-5

3. Prompt = ส่วนที่เหลือหลัง flag หรือทั้งหมดถ้าไม่มี flag
4. ถ้าไม่มี prompt เลย → ถาม user ก่อนดำเนินการต่อ

### Step 2 — อ่าน Tokens

```bash
JIT_ROOT="$HOME/Jit"
if [ -f "$JIT_ROOT/.env" ]; then
  source "$JIT_ROOT/.env"
fi
# ต้องการ: OLLAMA_TOKEN, THAILLM_TOKEN
```

### Step 3 — เรียกแต่ละโมเดลพร้อมกัน (Parallel)

รัน bash commands ต่อไปนี้ **พร้อมกัน** ด้วย Bash tool หลายตัว วัดเวลาแต่ละตัว

#### Template: วิธีวัดเวลาและเรียก MDES Ollama

```bash
START=$(date +%s%3N)

PROMPT="$PROMPT_TEXT"  # แทนด้วย prompt จริง
MODEL="gemma4:26b"     # หรือ qwen2.5:72b, qwen2.5-coder, gemma2:9b

BODY=$(python3 -c "
import json, sys
print(json.dumps({
  'model': '$MODEL',
  'prompt': sys.argv[1],
  'stream': False
}))
" "$PROMPT")

RESPONSE=$(curl -s --max-time 60 \
  "https://ollama.mdes-innova.online/api/generate" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OLLAMA_TOKEN" \
  --data "$BODY" 2>/dev/null)

END=$(date +%s%3N)
ELAPSED=$(( (END - START) ))  # milliseconds

TEXT=$(echo "$RESPONSE" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(data.get('response', '(no response)'))
    # token count (ถ้ามี)
    ec = data.get('eval_count', 0)
    print(f'__TOKENS__:{ec}', file=sys.stderr)
except:
    print('(parse error)')
" 2>/tmp/ollama_meta.txt)

TOKENS=$(cat /tmp/ollama_meta.txt | grep __TOKENS__ | cut -d: -f2)

echo "ELAPSED_MS=$ELAPSED"
echo "TOKENS=$TOKENS"
echo "---RESPONSE---"
echo "$TEXT"
```

#### Template: วิธีเรียก ThaiLLM

```bash
# ใช้ limbs/thaillm.sh จาก Jit repo:
JIT_ROOT="$HOME/Jit"

START=$(date +%s%3N)

RESPONSE=$(bash "$JIT_ROOT/limbs/thaillm.sh" ask typhoon "$PROMPT_TEXT" 2>/dev/null)
# หรือ openthaigpt, pathumma, thalle

END=$(date +%s%3N)
ELAPSED=$(( (END - START) ))

echo "ELAPSED_MS=$ELAPSED"
echo "TOKENS=~unknown"  # ThaiLLM ไม่ return token count เสมอ
echo "---RESPONSE---"
echo "$RESPONSE"
```

#### Template: เรียกผ่าน curl โดยตรง (ThaiLLM)

```bash
START=$(date +%s%3N)

BODY=$(python3 -c "
import json, sys
print(json.dumps({
  'model': 'Typhoon-S-ThaiLLM-8B-Instruct',
  'messages': [{'role': 'user', 'content': sys.argv[1]}],
  'max_tokens': 2048,
  'temperature': 0.3
}))
" "$PROMPT_TEXT")

RESPONSE=$(curl -s --max-time 60 \
  "http://thaillm.or.th/api/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $THAILLM_TOKEN" \
  -H "User-Agent: Mozilla/5.0" \
  --data "$BODY" 2>/dev/null)

END=$(date +%s%3N)
ELAPSED=$(( (END - START) ))

TEXT=$(echo "$RESPONSE" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    content = data['choices'][0]['message']['content']
    print(content)
    usage = data.get('usage', {})
    total = usage.get('total_tokens', 0)
    print(f'__TOKENS__:{total}', file=sys.stderr)
except Exception as e:
    print(f'(error: {e})')
" 2>/tmp/thaillm_meta.txt)

TOKENS=$(cat /tmp/thaillm_meta.txt | grep __TOKENS__ | cut -d: -f2 || echo "~")

echo "ELAPSED_MS=$ELAPSED"
echo "TOKENS=$TOKENS"
echo "---RESPONSE---"
echo "$TEXT"
```

#### Template: เรียก Claude (ใช้ Claude tool ใน session นี้)

สำหรับ Claude models — Claude ไม่จำเป็นต้องเรียกผ่าน bash เพราะมันคือ session ปัจจุบัน แต่ให้จำลอง:
- วัดเวลาด้วย `date +%s%3N` ก่อนและหลัง
- ใช้ claude-haiku-4-5 (default สำหรับ compare เพื่อประหยัด cost)
- แจ้งไว้ในผลว่า "response จาก Claude ในตัว session"

### Step 4 — ประเมินคุณภาพ (AI Self-Scoring)

หลังได้ผลทั้งหมด ให้ประเมิน 1-5 สำหรับแต่ละโมเดลตามเกณฑ์:

| คะแนน | ความหมาย |
|-------|----------|
| 5 | ตรงประเด็น, ครบ, ใช้ได้จริงทันที |
| 4 | ดี แต่มีรายละเอียดเล็กน้อยที่ขาด |
| 3 | พอใช้ได้ แต่ต้องปรับเพิ่ม |
| 2 | ผิดทิศทางหรือขาดสาระ |
| 1 | ผิดพลาดหรือ hallucinate |

ปัจจัยที่ใช้ประเมิน (ตาม context ของ prompt):
- ถ้าเป็น **ภาษาไทย**: ความเป็นธรรมชาติของภาษา, ไม่แข็ง, เข้าใจง่าย
- ถ้าเป็น **code**: ถูกต้อง syntax, logic ถูก, รันได้จริง
- ถ้าเป็น **reasoning**: ลึก, มีเหตุผล, ไม่วนซ้ำ
- ถ้าเป็น **creative**: สร้างสรรค์, ไม่ซ้ำซาก

### Step 5 — แสดงผล

แสดงในรูปแบบนี้:

```markdown
## ผลเปรียบเทียบ: "[25 ตัวอักษรแรกของ prompt]..."

**Prompt**: [full prompt]
**โมเดลที่ทดสอบ**: [รายชื่อ]
**วันที่**: YYYY-MM-DD HH:MM

---

### ตารางสรุป

| โมเดล | Provider | เวลา | Token | คุณภาพ (1-5) | สรุปคำตอบ |
|-------|----------|------|-------|-------------|-----------|
| gemma4:26b | MDES Ollama | Xs | ~N | ⭐⭐⭐⭐ (4) | [20 คำแรก...] |
| typhoon-s | ThaiLLM | Xs | ~N | ⭐⭐⭐⭐⭐ (5) | [20 คำแรก...] |
| claude-haiku | Anthropic | Xs | ~N | ⭐⭐⭐⭐ (4) | [20 คำแรก...] |

---

### ผลลัพธ์เต็ม

#### gemma4:26b (MDES Ollama)
> เวลา: Xs | Token: ~N

[full response text]

---

#### typhoon-s (ThaiLLM)
> เวลา: Xs | Token: ~N

[full response text]

---

#### claude-haiku-4-5 (Anthropic Claude)
> เวลา: Xs | Token: ~N

[full response text]

---

## สรุปผู้ชนะ

**[ชื่อโมเดล]** ดีที่สุดสำหรับ prompt นี้เพราะ [เหตุผล 1-2 ประโยค]

### Insights:
- **เร็วที่สุด**: [โมเดล] (~Xs)
- **คุณภาพภาษาไทยดีที่สุด**: [โมเดล]
- **ตอบครบที่สุด**: [โมเดล]
- **คุ้มค่าที่สุด**: [โมเดล] (เร็ว + คุณภาพดี)

### แนะนำสำหรับงานประเภทนี้
[1-2 ประโยคแนะนำว่าควรใช้โมเดลไหนสำหรับงานแบบ prompt นี้ในอนาคต]
```

---

## Model Sets Reference

| Flag | โมเดลที่รัน |
|------|-------------|
| (default) | gemma4:26b + typhoon + claude-haiku-4-5 |
| `--models mdes` | gemma4:26b + qwen2.5:72b |
| `--models thaillm` | typhoon + openthaigpt |
| `--models claude` | claude-haiku-4-5 + claude-sonnet-4-6 |
| `--models mdes,thaillm` | gemma4:26b + typhoon |
| `--models all` | gemma4:26b + qwen2.5:72b + typhoon + openthaigpt + claude-haiku-4-5 |

---

## Model IDs ที่ใช้งาน

### MDES Ollama (`https://ollama.mdes-innova.online`)
| ชื่อสั้น | Model ID สำหรับ API |
|---------|---------------------|
| gemma4:26b | `gemma4:26b` |
| qwen2.5:72b | `qwen2.5:72b` |
| qwen2.5-coder | `qwen2.5-coder` |
| gemma2:9b | `gemma2:9b` |

API Endpoint: `POST /api/generate`
Body: `{"model": "...", "prompt": "...", "stream": false}`
Auth: `Authorization: Bearer $OLLAMA_TOKEN`

### ThaiLLM (`http://thaillm.or.th/api/v1`)
| ชื่อสั้น | Model ID สำหรับ API |
|---------|---------------------|
| typhoon | `Typhoon-S-ThaiLLM-8B-Instruct` |
| openthaigpt | `OpenThaiGPT-ThaiLLM-8B-Instruct-v7.2` |
| pathumma | `Pathumma-ThaiLLM-qwen3-8b-think-3.0.0` |
| thalle | `THaLLE-0.2-ThaiLLM-8B-fa` |

API Endpoint: `POST /api/v1/chat/completions` (OpenAI-compatible)
Body: `{"model": "...", "messages": [{"role": "user", "content": "..."}], "max_tokens": 2048, "temperature": 0.3}`
Auth: `Authorization: Bearer $THAILLM_TOKEN`

---

## Limb Script Shortcuts

แทน curl ตรง สามารถใช้ scripts จาก Jit repo:

```bash
# MDES Ollama
bash ~/Jit/limbs/ollama.sh ask "prompt text"

# ThaiLLM (ระบุ model)
bash ~/Jit/limbs/thaillm.sh ask typhoon "prompt text"
bash ~/Jit/limbs/thaillm.sh ask openthaigpt "prompt text"
bash ~/Jit/limbs/thaillm.sh ask pathumma "prompt text"
bash ~/Jit/limbs/thaillm.sh ask thalle "prompt text"
```

หมายเหตุ: `ollama.sh ask` ใช้ `gemma4:26b` เสมอ ถ้าต้องการโมเดลอื่นต้องใช้ curl โดยตรง

---

## Error Handling

- ถ้าโมเดลหนึ่ง timeout → แสดง `🔴 Timeout (>60s)` ในตาราง แต่ยังแสดงผลโมเดลอื่น
- ถ้า token ไม่มี → แจ้ง "THAILLM_TOKEN หรือ OLLAMA_TOKEN ไม่พบ" แล้วข้ามโมเดลนั้น
- ถ้า response เป็น error JSON → parse error message แล้วแสดงใน table ว่า `ERROR: [message]`
- ถ้าไม่มีโมเดลใดตอบ → แจ้ง user ให้ตรวจ network และ tokens

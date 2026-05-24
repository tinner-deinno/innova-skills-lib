<!-- skill-id: model-list-status -->
<!-- source-path: model-list-status -->
<!-- source-file: C:/Users/MDES-DEV-NB/.claude/skills/model-list-status/SKILL.md -->
<!-- runtime: claude -->

# /model-list-status — สถานะทรัพยากรสมอง

ตรวจสอบ AI model endpoints ทั้งหมดและแสดงตาราง status + latency

**Trigger**: `/model-list-status` หรือเมื่อ user ถามว่า "โมเดลไหนใช้ได้บ้าง", "check models", "model status", "ทรัพยากรพร้อมไหม"

---

## วิธีปฏิบัติ (Step-by-Step)

### Step 1 — อ่าน Token จาก Environment

```bash
# อ่าน token จาก .env ในโปรเจกต์ Jit (ถ้ามี)
JIT_ROOT="$HOME/Jit"
if [ -f "$JIT_ROOT/.env" ]; then
  source "$JIT_ROOT/.env"
fi
# OLLAMA_TOKEN และ THAILLM_TOKEN ควรถูก export แล้ว
```

ถ้า env ไม่มี ให้แจ้ง user ว่า token ไม่ครบ แต่ยังทำ check ต่อเท่าที่ทำได้

### Step 2 — รัน Parallel Checks

รัน bash commands ต่อไปนี้พร้อมกัน (ใช้ Bash tool หลายตัวในเวลาเดียวกัน) แต่ละ check ต้องวัดเวลา:

#### Check A: MDES Ollama (gemma4:26b + list)
```bash
START=$(date +%s%3N)
RESPONSE=$(curl -s --max-time 5 \
  "https://ollama.mdes-innova.online/api/tags" \
  -H "Authorization: Bearer $OLLAMA_TOKEN" 2>/dev/null)
END=$(date +%s%3N)
LATENCY=$((END - START))
if [ -n "$RESPONSE" ]; then
  echo "STATUS=online"
  echo "LATENCY=${LATENCY}ms"
  echo "$RESPONSE" | python3 -c "
import sys, json
data = json.load(sys.stdin)
models = data.get('models', [])
for m in models:
    print('MODEL:', m.get('name', ''))
" 2>/dev/null
else
  echo "STATUS=offline"
  echo "LATENCY=timeout"
fi
```

#### Check B: ThaiLLM API
```bash
START=$(date +%s%3N)
RESPONSE=$(curl -s --max-time 5 \
  "http://thaillm.or.th/api/v1/models" \
  -H "Authorization: Bearer $THAILLM_TOKEN" 2>/dev/null)
END=$(date +%s%3N)
LATENCY=$((END - START))
if [ -n "$RESPONSE" ]; then
  echo "STATUS=online"
  echo "LATENCY=${LATENCY}ms"
  echo "$RESPONSE" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    models = data.get('data', data if isinstance(data, list) else [])
    for m in models:
        name = m.get('id', m.get('name', ''))
        print('MODEL:', name)
except:
    print('MODEL: (parse error)')
" 2>/dev/null
else
  echo "STATUS=offline"
  echo "LATENCY=timeout"
fi
```

#### Check C: Local Ollama
```bash
START=$(date +%s%3N)
RESPONSE=$(curl -s --max-time 3 "http://localhost:11434/api/tags" 2>/dev/null)
END=$(date +%s%3N)
LATENCY=$((END - START))
if [ -n "$RESPONSE" ]; then
  echo "STATUS=online"
  echo "LATENCY=${LATENCY}ms"
  echo "$RESPONSE" | python3 -c "
import sys, json
data = json.load(sys.stdin)
models = data.get('models', [])
for m in models:
    print('MODEL:', m.get('name', ''))
" 2>/dev/null
else
  echo "STATUS=offline"
  echo "LATENCY=timeout"
fi
```

#### Check D: OpenAI API
```bash
START=$(date +%s%3N)
RESPONSE=$(curl -s --max-time 5 \
  "https://api.openai.com/v1/models" \
  -H "Authorization: Bearer $OPENAI_API_KEY" 2>/dev/null)
END=$(date +%s%3N)
LATENCY=$((END - START))
if echo "$RESPONSE" | python3 -c "import sys,json; d=json.load(sys.stdin); print('ok')" 2>/dev/null | grep -q ok; then
  echo "STATUS=online"
  echo "LATENCY=${LATENCY}ms"
  echo "$RESPONSE" | python3 -c "
import sys, json
data = json.load(sys.stdin)
models = [m['id'] for m in data.get('data', []) if m.get('id','').startswith('gpt') or m.get('id','').startswith('o')]
for m in sorted(set(models))[:8]:
    print('MODEL:', m)
" 2>/dev/null
else
  echo "STATUS=offline"
  echo "LATENCY=timeout"
fi
```

#### Check E: GitHub Models
```bash
START=$(date +%s%3N)
RESPONSE=$(curl -s --max-time 5 \
  "https://models.inference.ai.azure.com/models" \
  -H "Authorization: Bearer $GITHUB_COPILOT_TOKEN" 2>/dev/null)
END=$(date +%s%3N)
LATENCY=$((END - START))
if echo "$RESPONSE" | python3 -c "import sys,json; json.load(sys.stdin); print('ok')" 2>/dev/null | grep -q ok; then
  echo "STATUS=online"
  echo "LATENCY=${LATENCY}ms"
  echo "$RESPONSE" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    items = data if isinstance(data, list) else data.get('data', [])
    for m in items[:8]:
        print('MODEL:', m.get('id', m.get('name', '')))
except:
    print('MODEL: (parse error)')
" 2>/dev/null
else
  echo "STATUS=offline"
  echo "LATENCY=timeout"
fi
```

### Step 3 — รวบรวมผลและสร้างตาราง

รวมผลจากทั้ง 3 checks แล้วแสดงในรูปแบบนี้:

```
## สถานะทรัพยากรสมอง (Brain Resource Status)
วันที่: YYYY-MM-DD HH:MM

### MDES Ollama (https://ollama.mdes-innova.online)
Status: 🟢 Online / 🔴 Offline / 🟡 Slow (>3s)
Latency: Xms

| # | โมเดล | ขนาด | เหมาะสำหรับ |
|---|-------|------|-------------|
| 1 | gemma4:26b | ~26B | งานทั่วไป, ภาษาไทย |
| 2 | qwen2.5:72b | ~72B | Deep reasoning, ซับซ้อน |
| 3 | qwen2.5-coder | ~7B | งาน code |
| 4 | gemma2:9b | ~9B | งานเบา, เร็ว |

### ThaiLLM (http://thaillm.or.th/api/v1)
Status: 🟢 Online / 🔴 Offline / 🟡 Slow (>3s)
Latency: Xms

| # | โมเดล | ID | เหมาะสำหรับ |
|---|----|------|-------------|
| 1 | OpenThaiGPT | OpenThaiGPT-ThaiLLM-8B-Instruct-v7.2 | ภาษาไทยทั่วไป |
| 2 | Pathumma | Pathumma-ThaiLLM-qwen3-8b-think-3.0.0 | คิดลึก, ภาษาไทย |
| 3 | Typhoon-S | Typhoon-S-ThaiLLM-8B-Instruct | สนทนาภาษาไทย |
| 4 | THaLLE | THaLLE-0.2-ThaiLLM-8B-fa | ภาษาไทย academic |

### Local Ollama (http://localhost:11434)
Status: 🟢 Online / 🔴 Offline (ปกติไม่รัน)
[แสดงโมเดลที่ติดตั้งถ้า online]

### OpenAI (https://api.openai.com/v1)
Status: 🟢 Online / 🔴 Offline / 🟡 Auth Error
Latency: Xms

| โมเดล | เหมาะสำหรับ |
|-------|-------------|
| gpt-4o | flagship, งานทั่วไป |
| gpt-4o-mini | ประหยัด cost |
| o1 / o3-mini / o4-mini | reasoning ลึก |

### GitHub Models (https://models.inference.ai.azure.com)
Status: 🟢 Online / 🔴 Offline / 🟡 Auth Error
Latency: Xms

| โมเดล | เหมาะสำหรับ |
|-------|-------------|
| gpt-4o | OpenAI ผ่าน GitHub |
| claude-3-5-sonnet-20241022 | Anthropic ผ่าน GitHub |
| meta-llama-3.3-70b-instruct | Meta ผ่าน GitHub |
| o1 / o3-mini | reasoning ผ่าน GitHub |

### Claude Models (Always Available)
| โมเดล | ID | เหมาะสำหรับ |
|-------|-----|-------------|
| claude-sonnet-4-6 | claude-sonnet-4-6 | งานหลัก, orchestration |
| claude-opus-4-7 | claude-opus-4-7 | reasoning ลึก |
| claude-haiku-4-5 | claude-haiku-4-5 | งานเบา, เร็ว, ประหยัด |

---

## สรุปแนะนำสำหรับงานต่างๆ

| งาน | โมเดลที่แนะนำ | เหตุผล |
|-----|--------------|--------|
| งานซับซ้อน / reasoning | qwen2.5:72b (MDES) | ใหญ่ที่สุด, ลึกที่สุด |
| ภาษาไทย (ทั่วไป) | typhoon / openthaigpt (ThaiLLM) | เชี่ยวชาญภาษาไทย |
| ภาษาไทย (คิดลึก) | pathumma (ThaiLLM) | มี thinking mode |
| งาน code | qwen2.5-coder (MDES) | เชี่ยวชาญ code |
| openclaude TUI (ไทย) | gemma4:26b MDES | default openclaude + ภาษาไทย |
| openclaude TUI (OpenAI) | gpt-4o (openai/github) | frontier, ผ่าน openclaude |
| orchestration / multi-agent | claude-sonnet-4-6 | มี tool use, agents |
| งานด่วน / ประหยัด cost | gemma2:9b (MDES) หรือ claude-haiku | เร็ว, ถูก |
| reasoning สูงสุด | claude-opus-4-7 หรือ o1/o3-mini | deepest reasoning |
```

### Step 4 — สรุปสถานะ

หลังจากแสดงตาราง ให้สรุปสั้นๆ:
- กี่ provider online (จาก 3: MDES Ollama, ThaiLLM, Local)
- provider ที่ latency ต่ำสุด
- คำแนะนำงานที่จะทำต่อไป (ถ้าทราบ context)

---

## หมายเหตุการ Parse

**MDES Ollama `/api/tags`** ตอบกลับเป็น:
```json
{"models": [{"name": "gemma4:26b", "size": 123456789, ...}]}
```

**ThaiLLM `/api/v1/models`** ตอบกลับแบบ OpenAI-compatible:
```json
{"data": [{"id": "OpenThaiGPT-ThaiLLM-8B-Instruct-v7.2", "object": "model"}]}
```

**Local Ollama `/api/tags`** format เดียวกับ MDES Ollama

---

## Status Indicator

- 🟢 Online — latency < 2000ms
- 🟡 Slow — latency 2000–5000ms  
- 🔴 Offline — timeout หรือ error

---

## ตัวอย่าง Output สั้น (ถ้า user ต้องการ quick view)

```
MDES Ollama    🟢 ~850ms  — gemma4:26b, qwen2.5:72b, qwen2.5-coder, gemma2:9b
ThaiLLM        🟢 ~1200ms — openthaigpt, pathumma, typhoon, thalle
Local Ollama   🔴 offline
OpenAI         🟢 ~600ms  — gpt-4o, gpt-4o-mini, o1, o3-mini, o4-mini
GitHub Models  🟢 ~700ms  — gpt-4o, claude-3-5-sonnet, llama-3.3-70b, o1
Claude         🟢 always  — sonnet-4-6, opus-4-7, haiku-4-5

แนะนำตอนนี้: MDES Ollama (latency ดีที่สุด)
```

### Step 4 — แสดง openclaude shortcuts (ถ้า user ต้องการเปิด TUI)

ถ้า providers พร้อมแล้ว ให้แสดงคำแนะนำ shortcut เพิ่มเติม:

```
ต้องการเปิด openclaude TUI?
  oc-mdes    → gemma4:26b  (MDES Ollama — ภาษาไทย)
  oc-github  → gpt-4o      (GitHub Models)
  oc-openai  → gpt-4o      (OpenAI direct)
  oc-thai    → typhoon-s   (ThaiLLM)
  oc-local   → (local models)

หรือใช้ /model-openclaude สำหรับรายละเอียดเพิ่มเติม
```

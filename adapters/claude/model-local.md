<!-- skill-id: model-local -->
<!-- source-path: model-local -->
<!-- source-file: C:/Users/MDES-DEV-NB/.claude/skills/model-local/SKILL.md -->
<!-- runtime: claude -->

# Skill: /model-local — ส่งงานไปยัง Local Ollama

> "ไม่ใช้ token cloud — ประมวลผลบนเครื่อง BigBoss เอง"

## ภาพรวม

`/model-local` ส่งงานไปยัง Ollama ที่รันบนเครื่อง `localhost:11434`
ไม่มีค่าใช้จ่าย ไม่มีข้อมูลส่งออกนอกเครื่อง เหมาะสำหรับงานที่มีข้อมูลสำคัญ/ลับ

## การใช้งาน

```
/model-local [prompt]
/model-local --list
/model-local --status
/model-local --model [ชื่อโมเดล] [prompt]
```

## ขั้นตอนการรัน

**1. ตรวจสอบว่า Local Ollama ทำงานอยู่หรือไม่:**

```bash
curl -s --max-time 2 http://localhost:11434/api/tags
```

ถ้าไม่มีผลลัพธ์ (error/timeout) → แสดงข้อความ:

```
Local Ollama ไม่ทำงาน

วิธีเริ่ม Ollama:
  1. เปิด Ollama app (ถ้าติดตั้งแล้ว)
  2. หรือรัน: ollama serve
  3. รอ 5-10 วินาทีแล้วลองใหม่

ติดตั้ง Ollama:
  https://ollama.com/download
  
ดาวน์โหลดโมเดลแนะนำ:
  ollama pull llama3.2:3b       # เบา เร็ว
  ollama pull qwen2.5:7b        # ดีสำหรับภาษาไทย
  ollama pull codellama:7b      # สำหรับโค้ด
  ollama pull gemma2:9b         # ดี round-trip
```

**2. แสดงโมเดลที่มีใน Local:**

```bash
curl -s http://localhost:11434/api/tags | python3 -c "
import sys, json
data = json.load(sys.stdin)
models = data.get('models', [])
if not models:
    print('ไม่มีโมเดล — ดาวน์โหลดด้วย: ollama pull <model>')
else:
    print('โมเดลที่มีในเครื่อง:')
    for m in models:
        size_gb = m.get('size', 0) / 1e9
        print(f'  {m[\"name\"]:30s} {size_gb:.1f}GB')
"
```

**3. Auto-select โมเดล หรือให้ผู้ใช้เลือก:**

เลือกโมเดลอัตโนมัติตามลำดับความสำคัญ:
1. ถ้ามี `qwen2.5:7b` → ใช้เลย (ดีสำหรับภาษาไทย)
2. ถ้ามี `llama3.2` → ใช้ (เร็ว ดีทั่วไป)
3. ถ้ามี `gemma2` → ใช้
4. อื่นๆ → ใช้โมเดลแรกในรายการ

**4. ส่งงาน:**

```bash
MODEL="qwen2.5:7b"
PROMPT="[งานจากผู้ใช้]"

curl -s http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d "$(python3 -c "import json,sys; print(json.dumps({'model':'$MODEL','prompt':sys.argv[1],'stream':False}))" "$PROMPT")" \
| python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('response',''))"
```

**5. แสดงผลพร้อม attribution:**

```
[ผลลัพธ์]

— ตอบโดย qwen2.5:7b (Local Ollama — ไม่ใช้ token cloud)
```

## ตัวอย่างการใช้งาน

```
/model-local
→ ตรวจสอบ Ollama...
→ พบโมเดล: qwen2.5:7b, llama3.2:3b, codellama:7b
→ เลือก: qwen2.5:7b (ดีที่สุดสำหรับภาษาไทย)
→ รอ prompt...

/model-local อธิบาย recursion ภาษาไทย
→ ใช้ qwen2.5:7b (auto-selected)

/model-local --model codellama:7b เขียน function sort linked list
→ ใช้ codellama:7b ตามที่ระบุ

/model-local --list
→ แสดงโมเดลทั้งหมดในเครื่อง

/model-local --status
→ ตรวจสอบ Ollama พร้อมทำงานหรือไม่
```

## คำสั่งที่รันจริง

```bash
# ตรวจสอบสถานะ
curl -s --max-time 2 http://localhost:11434/api/tags | python3 -m json.tool

# ดูโมเดลทั้งหมด
curl -s http://localhost:11434/api/tags | python3 -c "
import sys, json
for m in json.load(sys.stdin).get('models', []):
    print(m['name'], f\"{m.get('size',0)/1e9:.1f}GB\")
"

# ถามโมเดลใน Local
curl -s http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen2.5:7b","prompt":"สวัสดี","stream":false}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin).get('response',''))"

# ดึงโมเดลใหม่
ollama pull llama3.2:3b
ollama pull qwen2.5:7b
ollama pull codellama:7b
```

## ข้อดีของ Local Ollama

- ไม่มีค่าใช้จ่าย (ไม่มี API token)
- ข้อมูลไม่ออกนอกเครื่อง (ปลอดภัยสำหรับข้อมูลลับ)
- ทำงานได้แม้ไม่มี internet
- Latency ต่ำมากสำหรับโมเดลเล็ก

## ข้อจำกัด

- โมเดลเล็กกว่า cloud models (7B-13B vs 26B-72B)
- ต้องการ RAM/VRAM เพียงพอ
- ต้องดาวน์โหลดโมเดลก่อน (ครั้งแรก)

## ข้อมูลเพิ่มเติม

- **Author**: Jit Oracle
- **Created**: 2026-05-23
- **Endpoint**: `http://localhost:11434`
- **Download**: `https://ollama.com/download`
- **Models**: `https://ollama.com/library`
- **Related**: `/model-thaiLLM`, `/model-MDES`, `/model-claude`

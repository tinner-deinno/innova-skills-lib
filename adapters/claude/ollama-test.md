<!-- skill-id: ollama-test -->
<!-- source-path: ollama-test -->
<!-- source-file: C:/Users/MDES-DEV-NB/.claude/skills/ollama-test/SKILL.md -->
<!-- runtime: claude -->

# /ollama-test — ทักษะทดสอบ Ollama Cloud Models

> "ช่างฝีมือทดสอบเครื่องมือ — ทดสอบให้เห็นจริง ไม่ใช่แค่คิดว่าใช้ได้"

## ภาพรวม

ทักษะนี้ใช้ทดสอบ Ollama cloud models ว่า model ใดทำงานได้จริงกับ endpoint `mdes.ollama` พร้อมทั้งตรวจสอบ token limit และ usage percentage

## Endpoint หลัก

**mdes.ollama** — endpoint หลักสำหรับทดสอบโมเดล

```bash
$env:OLLAMA_HOST = "https://mdes.ollama"
ollama.exe list
```

## การใช้งาน

```
/ollama-test                    # ทดสอบ models ทั้งหมด
/ollama-test <model>           # ทดสอบ model เฉพาะ
/ollama-test --list            # แสดงรายการ models ที่มี
/ollama-test --status          # แสดง models ที่ใช้งานได้
/ollama-test --fallback       # ทดสอบ fallback providers
/ollama-test --tokens         # แสดง token usage ของแต่ละ model
```

## Token Limit Awareness

ทุกโมเดลมี token limit ต่างกัน ต้องตรวจสอบก่อนใช้งาน:

| Model | Context | Output | Usage % |
|-------|---------|--------|---------|
| nemotron-3-super | 128K | 8K | ตรวจสอบอัตโนมัติ |
| minimax-m2.5 | 1M | 32K | ตรวจสอบอัตโนมัติ |
| minimax-m2.7 | 1M | 32K | ตรวจสอบอัตโนมัติ |
| deepseek-v4-flash | 200K | 8K | ตรวจสอบอัตโนมัติ |
| deepseek-v4-pro | 200K | 8K | ตรวจสอบอัตโนมัติ |
| kimi-k2.6 | 200K | 8K | ตรวจสอบอัตโนมัติ |
| gemma4 | 128K | 8K | ตรวจสอบอัตโนมัติ |
| glm-5.1 | 1M | 8K | ตรวจสอบอัตโนมัติ |
| qwen3.5 | 32K | 8K | ตรวจสอบอัตโนมัติ |

### วิธีตรวจสอบ Token Usage

```powershell
# ตรวจสอบ token usage หลังจาก run model
ollama.exe run <model> "ทดสอบ" --verbose
```

### การคำนวณ Usage Percentage

- **Input tokens**: นับจาก prompt ที่ส่ง
- **Output tokens**: นับจาก response ที่ได้รับ
- **Usage %**: (input + output) / max_context * 100

## Cloud Models ที่ต้องทดสอบ

| # | Model | Provider | Context | Status |
|---|-------|----------|---------|--------|
| 1 | nemotron-3-super | NVIDIA | 128K | ทดสอบ |
| 2 | minimax-m2.5 | MiniMax | 1M | ทดสอบ |
| 3 | minimax-m2.7 | MiniMax | 1M | ทดสอบ |
| 4 | deepseek-v4-flash | DeepSeek | 200K | ทดสอบ |
| 5 | deepseek-v4-pro | DeepSeek | 200K | ทดสอบ |
| 6 | deepseek-v3.2 | DeepSeek | 64K | ทดสอบ |
| 7 | kimi-k2.6 | Kimi | 200K | ทดสอบ |
| 8 | kimi-k2.5 | Kimi | 128K | ทดสอบ |
| 9 | gemma4 | Google | 128K | ทดสอบ |
| 10 | glm-5.1 | Z.ai | 1M | ทดสอบ |
| 11 | glm-5 | Z.ai | 128K | ทดสอบ |
| 12 | glm-4.7 | Z.ai | 128K | ทดสอบ |
| 13 | qwen3.5 | Qwen | 32K | ทดสอบ |
| 14 | qwen3-coder-next | Qwen | 32K | ทดสอบ |
| 15 | qwen3-next | Qwen | 32K | ทดสอบ |
| 16 | devstral-small-2 | Devstral | 4K | ทดสอบ |
| 17 | rnj-1 | Essential AI | 32K | ทดสอบ |
| 18 | nemotron-3-nano | NVIDIA | 4K | ทดสอบ |
| 19 | ministral-3 | Ministral | 8K | ทดสอบ |
| 20 | gemini-3-flash-preview | Google | 1M | ทดสอบ |

## วิธีทดสอบแต่ละ Model

### 1. ตรวจสอบ Model ที่มีอยู่

```powershell
$env:OLLAMA_HOST = "https://mdes.ollama"
ollama.exe list
```

### 2. ทดสอบ Model เฉพาะ

```powershell
$env:OLLAMA_HOST = "https://mdes.ollama"
ollama.exe run <model> "Hello, ทดสอบ"
```

### 3. ตรวจสอบ Token Usage

```powershell
$env:OLLAMA_HOST = "https://mdes.ollama"
# ใช้ --verbose เพื่อดู token usage
ollama.exe run <model> "ทดสอบ 1-2-3" --verbose
```

## พฤติกรรมที่คาดหวัง

### สำเร็จ
- Model รันได้และตอบกลับ
- ไม่มี error เกี่ยวกับ API key หรือ authentication
- แสดง token usage percentage

### ล้มเหลว
- `Error: model not found` — model ไม่มีในระบบ
- `Error: invalid credentials` — API key ไม่ถูกต้อง
- `Error: connection failed` — endpoint ไม่ accessible
- `Error: rate limit exceeded` — เกิน quota
- `Error: token limit exceeded` — เกิน context window

## Fallback Providers

หาก Ollama ทั้งหมดไม่ได้ ให้ใช้:

### 1. OpenAI Codex (codex)
```powershell
# ต้องมี API key
$env:OPENAI_API_KEY = "your-key"
```

### 2. GPT Pro
```powershell
# ใช้ GPT-4o หรือ GPT-4.5
```

### 3. GitHub Copilot (with URL copy auth)
```
URL: https://github.com/features/copilot
Auth: Copy URL และให้ human ทำการ authenticate เอง
```

## ขั้นตอนการทดสอบ

### ทดสอบทั้งหมด

1. ตั้งค่า `OLLAMA_HOST=https://mdes.ollama`
2. เรียก `ollama.exe list` เพื่อดู models ที่มี
3. สำหรับแต่ละ model ในรายการ ให้ run ด้วย prompt ทดสอบ
4. ตรวจสอบ token usage percentage
5. บันทึกผลลัพธ์ (สำเร็จ/ล้มเหลว + error message + usage %)
6. รวบรวมเป็นรายงาน

### ทดสอบเฉพาะ model

```powershell
ollama.exe run <model> --verbose "ทดสอบ 1-2-3"
```

## การบันทึกผลลัพธ์

บันทึกผลการทดสอบที่:
- `~/.claude/skills/ollama-test/results/` — ไฟล์ผลลัพธ์
- ตั้งชื่อตาม timestamp: `test-YYYYMMDD-HHMMSS.json`
- รวม token usage data ในผลลัพธ์

## หมายเหตุ

- บาง model อาจต้องใช้เวลาโหลด (pull) ก่อน
- MiniMax models (minimax-m2.5, minimax-m2.7) อาจต้องใช้ API key เฉพาะ
- ทดสอบซ้ำหลายครั้งเพื่อยืนยันความเสถียร
- **ตรวจสอบ token usage ก่อนส่ง prompt ยาว**
- ใช้ `/auto-model` เพื่อค้นหาโมเดลที่ทำงานได้อัตโนมัติ
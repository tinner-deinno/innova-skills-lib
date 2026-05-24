<!-- skill-id: auto-model -->
<!-- source-path: auto-model -->
<!-- source-file: C:/Users/MDES-DEV-NB/.claude/skills/auto-model/SKILL.md -->
<!-- runtime: claude -->

# /auto-model — ระบบตรวจสอบและสำรองโมเดลอัตโนมัติ

> "ช่างฝีมือตรวจสอบเครื่องมือ — ทดสอบทุกโมเดล ให้มั่นใจว่ามีเครื่องมือพร้อมใช้งาน"

## วัตถุประสงค์

ระบบตรวจสอบและสำรองโมเดลอัตโนมัติ สำหรับ mdes.ollama endpoint

- ทดสอบโมเดลบน mdes.ollama
- ค้นหาโมเดลที่ทำงานได้อัตโนมัติ
- ตรวจสอบ token limit และ usage percentage
- สำรองไปยัง provider อื่นหากทุกอย่างล้มเหลว

## Endpoint หลัก

**mdes.ollama** — endpoint หลักสำหรับทดสอบโมเดล

## การใช้งาน

```
/auto-model                    # รันการตรวจสอบอัตโนมัติและค้นหาโมเดลที่ทำงานได้
/auto-model --current         # แสดงโมเดลที่กำลังทำงานอยู่
/auto-model --check <model>  # ตรวจสอบโมเดลเฉพาะ
/auto-model --set <model>     # ตั้งค่าโมเดลเป็นค่าเริ่มต้น
/auto-model --fallback       # ทดสอบ fallback providers
/auto-model --providers      # แสดงรายชื่อ providers ทั้งหมด
/auto-model --tokens         # แสดง token usage ของแต่ละ model
/auto-model --stats          # แสดง usage statistics
```

## Token Limit Awareness

### แต่ละ Model มี Token Limit ต่างกัน

| Model | Context | Output | ความเหมาะสม |
|-------|---------|--------|-------------|
| nemotron-3-super:cloud | 128K | 8K | งานใหญ่ |
| minimax-m2.5:cloud | 1M | 32K | งานใหญ่มาก |
| minimax-m2.7:cloud | 1M | 32K | งานใหญ่มาก |
| deepseek-v4-flash:cloud | 200K | 8K | งานกลาง |
| deepseek-v4-pro:cloud | 200K | 8K | งานกลาง |
| kimi-k2.6:cloud | 200K | 8K | งานกลาง |
| gemma4:cloud | 128K | 8K | งานใหญ่ |
| glm-5.1:cloud | 1M | 8K | งานใหญ่มาก |
| qwen3.5:cloud | 32K | 8K | งานเล็ก |

### การคำนวณ Usage Percentage

```bash
# ตัวอย่างการคำนวณ
Input tokens: 1,500
Output tokens: 3,200
Context limit: 128,000
Usage % = (1500 + 3200) / 128000 * 100 = 3.67%
```

### การตรวจสอบ Token

- ใช้ `--tokens` เพื่อดู token usage ของแต่ละ model
- ใช้ `--stats` เพื่อดู usage statistics โดยรวม
- หากใกล้ limit (90%+) ให้แจ้งเตือน

## Usage Statistics

แสดงสถิติการใช้งานโมเดล:

```
┌─────────────────────────────────────────────┐
│  Usage Statistics — mdes.ollama            │
├─────────────────────────────────────────────┤
│  nemotron-3-super:                         │
│    Total requests: 45                       │
│    Success rate: 93%                        │
│    Avg response: 1.2s                        │
│    Token usage: 12,450,000 / 128,000,000    │
│    Usage %: 9.7%                            │
├─────────────────────────────────────────────┤
│  minimax-m2.5:                              │
│    Total requests: 12                       │
│    Success rate: 75%                        │
│    Avg response: 2.3s                       │
│    Token usage: 8,200,000 / 1,000,000,000  │
│    Usage %: 0.8%                            │
└─────────────────────────────────────────────┘
```

## โมเดลที่ต้องทดสอบ (เรียงตามลำดับความสำคัญ)

1. `nemotron-3-super:cloud` — Super model จาก NVIDIA
2. `minimax-m2.5:cloud` — MiniMax M2.5
3. `deepseek-v4-flash:cloud` — DeepSeek V4 Flash
4. `kimi-k2.6:cloud` — Kimi K2.6
5. `gemma4:cloud` — Google Gemma 4
6. `glm-5.1:cloud` — GLM 5.1
7. `qwen3.5:cloud` — Qwen 3.5

## Fallback Providers

หาก Ollama ล้มเหลวทั้งหมด จะสำรองไปยัง:

- **codex** — OpenAI Codex
- **gpt pro** — GPT Pro
- **github copilot** — GitHub Copilot (URL copy auth)

## วิธีใช้งานแต่ละคำสั่ง

### /auto-model

รันการตรวจสอบอัตโนมัติ:

```
1. ขอรายชื่อโมเดลจาก ollama list
2. ทดสอบแต่ละโมเดลตามลำดับความสำคัญ
3. ตรวจสอบ token usage
4. บันทึกผลลัพธ์
5. แจ้งโมเดลที่ทำงานได้
```

### /auto-model --current

แสดงโมเดลปัจจุบันที่ถูกตั้งค่า:

```
- อ่านจาก config หรือ environment
- แสดงชื่อโมเดล, สถานะ, token usage
```

### /auto-model --check <model>

ตรวจสอบโมเดลเฉพาะ:

```
1. รับชื่อโมเดลเป้าหมาย
2. ทดสอบด้วย prompt ง่ายๆ
3. ตรวจสอบ token usage
4. คืนค่า: success/fail + response time + usage %
```

### /auto-model --set <model>

ตั้งค่าโมเดลเป็นค่าเริ่มต้น:

```
1. ตรวจสอบว่าโมเดลทำงานได้
2. บันทึกลง settings.json หรือ config
3. ยืนยันการตั้งค่า
```

### /auto-model --fallback

ทดสอบ fallback providers:

```
1. ทดสอบ codex
2. ทดสอบ gpt pro
3. ทดสอบ github copilot
4. แจ้ง provider ที่ทำงานได้
```

### /auto-model --providers

แสดงรายชื่อ providers ทั้งหมด:

```
- mdes.ollama (หลัก)
- codex (fallback)
- gpt pro (fallback)
- github copilot (fallback)
```

### /auto-model --tokens

แสดง token usage ของแต่ละ model:

```
- แสดง input/output tokens
- แสดง usage percentage
- แสดง context limit
```

### /auto-model --stats

แสดง usage statistics โดยรวม:

```
- Total requests
- Success rate
- Average response time
- Token usage by model
```

## GSD Skills Integration

### ทำงานร่วมกับ GSD workflow skills:

- **/gsd-execute-phase** — ใช้ auto-model เพื่อเลือกโมเดลที่เหมาะสม
- **/gsd-code-review** — ใช้ auto-model สำหรับ code review
- **/gsd-debug** — ใช้ auto-model สำหรับ debugging
- **/nemotron** — ใช้ auto-model เป็น fallback
- **/gang** — ใช้ auto-model สำหรับ gang operations
- **/mdes-ollama** — ใช้ auto-model ร่วมกับ orchestration

### ตัวอย่างการใช้งานใน GSD workflow:

```bash
# ก่อนเริ่ม GSD execute phase
/auto-model --current

# ตรวจสอบ token usage ก่อนงานใหญ่
/auto-model --tokens

# ดู statistics โดยรวม
/auto-model --stats
```

## ตัวอย่างการใช้งาน

```
user: /auto-model
→ ทดสอบ nemotron-3-super:cloud... สำเร็จ!
→ Token usage: 3.2%
→ โมเดลที่แนะนำ: nemotron-3-super:cloud

user: /auto-model --check minimax-m2.5:cloud
→ ทดสอบ minimax-m2.5:cloud... สำเร็จ! (2.3s)
→ Token usage: 1.8%

user: /auto-model --set deepseek-v4-flash:cloud
→ ตั้งค่า deepseek-v4-flash:cloud เป็นค่าเริ่มต้น ✓

user: /auto-model --providers
→ Available providers:
   - mdes.ollama (หลัก)
   - codex (fallback)
   - gpt pro (fallback)
   - github copilot (fallback)

user: /auto-model --tokens
→ Token Usage:
   - nemotron-3-super: 12,450,000 / 128,000,000 (9.7%)
   - minimax-m2.5: 8,200,000 / 1,000,000,000 (0.8%)
```

## การแจ้งเตือนข้อผิดพลาด

- `model not found` — โมเดลไม่มีในรายการ
- `connection failed` — เชื่อมต่อ endpoint ไม่ได้
- `timeout` — ใช้เวลานานเกินไป
- `token limit exceeded` — เกิน context window (90%+)
- `all failed` — ทุกโมเดลและ provider ล้มเหลว

## หมายเหตุ

- ควรทดสอบก่อนเริ่มงานสำคัญ
- เก็บผลลัพธ์ไว้อ้างอิง
- ตรวจสอบ token usage เป็นระยะ
- ใช้งานได้กับ agents ทุกตัว
- **ใช้งานร่วมกับ GSD skills สำหรับ end-to-end workflow**
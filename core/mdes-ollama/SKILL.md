---
name: mdes-ollama
description: "Skill workflow for mdes-ollama."
---

# Skill: /mdes-ollama — ระบบประสานงานโมเดลหลัก

> "ช่างฝีมือประสานโมเดล — ทดสอบทุกโมเดล ให้ได้เครื่องมือที่พร้อมทำงาน"

## ภาพรวม

`/mdes-ollama` คือ skill หลักสำหรับระบบทดสอบและสำรองโมเดล AI อัตโนมัติ — ทำหน้าที่เป็นตัวประสานงาน (orchestrator) ให้กับทุก skill ที่ต้องการใช้ AI models

## ตำแหน่งสำคัญ

**Endpoint หลัก**: mdes.ollama

**Config**: ~/.claude/skills/mdes-ollama/config.json

**Logs**: ~/.claude/skills/mdes-ollama/logs/

**Stats**: ~/.claude/skills/mdes-ollama/stats/

## วัตถุประสงค์

- เป็นตัวประสานงานหลัก (Central Orchestrator) ให้กับทุก skill
- ทดสอบโมเดลบน mdes.ollama endpoint
- ค้นหาโมเดลที่ทำงานได้โดยอัตโนมัติ
- ติดตาม token usage และ usage statistics
- สำรองไปยัง providers อื่นหาก Ollama ล้มเหลวทั้งหมด
- รองรับ auto-dev loop สำหรับ development workflow
- ให้บริการ `/nemotron`, `/gang`, `/auto-model` และ skills อื่นๆ

## การใช้งาน

```
/mdes-ollama                  # รันการตรวจสอบเต็มรูปแบบ + fallback chain
/mdes-ollama --test          # ทดสอบเฉพาะโมเดลที่มี
/mdes-ollama --force         # บังคับทดสอบใหม่ทุกโมเดล
/mdes-ollama --status        # แสดงโมเดลที่กำลังทำงานอยู่
/mdes-ollama --report        # รายงานผลการทดสอบ
/mdes-ollama --tokens        # แสดง token usage
/mdes-ollama --stats         # แสดง usage statistics
/mdes-ollama --dev-loop      # เริ่ม auto-dev loop
/mdes-ollama --integrate     # รวมกับ GSD skills
```

## Token Limit Tracking

### Token Tracking สำหรับทุก Model

| Model | Context | Output | สถานะ | Usage % |
|-------|---------|--------|-------|---------|
| nemotron-3-super:cloud | 128K | 8K | พร้อม | 9.7% |
| minimax-m2.5:cloud | 1M | 32K | พร้อม | 0.8% |
| minimax-m2.7:cloud | 1M | 32K | พร้อม | 0.5% |
| deepseek-v4-flash:cloud | 200K | 8K | พร้อม | 2.1% |
| deepseek-v4-pro:cloud | 200K | 8K | พร้อม | 1.2% |
| kimi-k2.6:cloud | 200K | 8K | พร้อม | 0.9% |
| gemma4:cloud | 128K | 8K | พร้อม | 3.4% |
| glm-5.1:cloud | 1M | 8K | พร้อม | 0.3% |
| qwen3.5:cloud | 32K | 8K | พร้อม | 5.6% |

### การติดตาม Token Usage

```bash
# ดู token usage โดยรวม
/mdes-ollama --tokens

# ดู statistics โดยละเอียด
/mdes-ollama --stats
```

### การคำนวณ Usage

- **Input**: tokens จาก prompt
- **Output**: tokens จาก response
- **Total**: input + output
- **Usage %**: total / context_limit * 100

### การแจ้งเตือน

- **Warning**: usage > 70% — แนะนำให้ใช้โมเดลอื่น
- **Critical**: usage > 90% — ห้ามใช้ ต้อง fallback

## Usage Statistics

### Dashboard

```
┌─────────────────────────────────────────────────────────────────┐
│  mdes.ollama — Central Orchestrator Statistics                  │
├─────────────────────────────────────────────────────────────────┤
│  Endpoint: mdes.ollama                                          │
│  Last Check: 2026-05-08 14:30                                   │
├─────────────────────────────────────────────────────────────────┤
│  Model Status:                                                   │
│    nemotron-3-super:cloud ✓ (93% success, 1.2s avg)            │
│    minimax-m2.5:cloud ✓ (75% success, 2.3s avg)                │
│    deepseek-v4-flash:cloud ✓ (88% success, 0.8s avg)            │
├─────────────────────────────────────────────────────────────────┤
│  Token Usage (Today):                                            │
│    Input: 4,250,000 tokens                                      │
│    Output: 1,820,000 tokens                                     │
│    Total: 6,070,000 tokens                                      │
│    Most used: nemotron-3-super (52%)                            │
├─────────────────────────────────────────────────────────────────┤
│  Requests Today: 57                                             │
│  Success Rate: 89%                                              │
│  Average Response: 1.5s                                          │
└─────────────────────────────────────────────────────────────────┘
```

## Auto-Dev Loop Capability

### วิธีเริ่ม Auto-Dev Loop

```bash
/mdes-ollama --dev-loop
```

### Auto-Dev Loop Features

1. **Automated Testing** — ทดสอบโมเดลอัตโนมัติเมื่อมีการเปลี่ยนแปลง
2. **Health Check** — ตรวจสอบสุขภาพโมเดลเป็นระยะ
3. **Fallback Trigger** — สลับไปยังโมเดลอื่นอัตโนมัติเมื่อล้มเหลว
4. **Notification** — แจ้งเตือนเมื่อมีปัญหา
5. **Logging** — บันทึกทุกการตัดสินใจ

### Dev Loop Configuration

```json
{
  "dev_loop": {
    "enabled": true,
    "interval": "5m",
    "models_to_check": ["nemotron-3-super", "minimax-m2.5", "deepseek-v4-flash"],
    "fallback_threshold": 3,
    "notification": true
  }
}
```

## Fallback Chain — ลำดับการสำรอง

### Priority 1: mdes.ollama models

ทดสอบโมเดลตามลำดับความสำคัญ (เรียงจากดีที่สุดไปหา):

1. `nemotron-3-super:cloud` — Super model จาก NVIDIA (แนะนำ)
2. `minimax-m2.5:cloud` — MiniMax M2.5
3. `deepseek-v4-flash:cloud` — DeepSeek V4 Flash
4. `kimi-k2.6:cloud` — Kimi K2.6
5. `gemma4:cloud` — Google Gemma 4
6. `glm-5.1:cloud` — GLM 5.1
7. `qwen3.5:cloud` — Qwen 3.5

### Priority 2: codex (OpenAI Codex)

หาก Ollama ล้มเหลวทั้งหมด → ลองใช้ OpenAI Codex

### Priority 3: GPT Pro

หาก codex ล้มเหลว → ลองใช้ GPT Pro

### Priority 4: GitHub Copilot

หาก GPT Pro ล้มเหลว → ใช้ GitHub Copilot (URL copy auth)

## GSD Skills Integration

### เป็น Central Orchestrator ให้กับ GSD Skills

- **/gsd-execute-phase** — เรียก mdes-ollama เพื่อเลือกโมเดล
- **/gsd-code-review** — ใช้ mdes-ollama สำหรับ review
- **/gsd-debug** — ใช้ mdes-ollama สำหรับ debugging
- **/gsd-spike** — ใช้ mdes-ollama สำหรับ investigation
- **/gsd-manager** — ใช้ mdes-ollama สำหรับ management

### การรวมกับ GSD

```bash
# รวมกับ GSD skills
/mdes-ollama --integrate

# ผลลัพธ์:
# ✓ รวมกับ gsd-execute-phase
# ✓ รวมกับ gsd-code-review
# ✓ รวมกับ gsd-debug
# ✓ รวมกับ gsd-manager
# พร้อมใช้งาน!
```

## วิธีใช้งานแต่ละคำสั่ง

### /mdes-ollama (ไม่มี flags)

รันการตรวจสอบเต็มรูปแบบพร้อม fallback chain:

```
1. ทดสอบโมเดล nemotron-3-super:cloud ก่อน
2. ตรวจสอบ token usage
3. หากสำเร็จ → คืนค่าโมเดลนี้
4. หากล้มเหลว → ลองโมเดลถัดไปในลำดับ
5. หากทุกโมเดลล้มเหลว → ลอง codex
6. หาก codex ล้มเหลว → ลอง GPT Pro
7. หาก GPT Pro ล้มเหลว → ลอง GitHub Copilot
8. คืนค่า provider/model ที่ทำงานได้
```

**ตัวอย่างผลลัพธ์:**
```
→ ทดสอบ nemotron-3-super:cloud... สำเร็จ! ✓
→ Token usage: 3.2%
→ โมเดลที่พร้อมใช้งาน: nemotron-3-super:cloud
```

### /mdes-ollama --test

ทดสอบเฉพาะโมเดลที่มีอยู่บนระบบ:

```
1. ขอรายชื่อโมเดลจาก `ollama list`
2. ทดสอบแต่ละโมเดลด้วย prompt ทดสอบ
3. แสดงผลลัพธ์แบบรวดเร็ว
4. ไม่มีการ fallback ไป providers อื่น
```

### /mdes-ollama --force

บังคับทดสอบใหม่ทุกโมเดล (ละทิ้ง cache):

```
1. ล้างผลการทดสอบก่อนหน้า
2. ทดสอบทุกโมเดลในลำดับความสำคัญ
3. บันทึกผลลัพธ์ใหม่ทั้งหมด
4. แสดงสถานะล่าสุด
```

### /mdes-ollama --status

แสดงโมเดลที่กำลังทำงานอยู่:

```
1. อ่านจาก config หรือ environment
2. แสดงชื่อโมเดล, provider, และสถานะ
3. แสดง token usage
4. แสดงเวลาที่ทดสอบล่าสุด
```

### /mdes-ollama --report

รายงานผลการทดสอบแบบละเอียด:

```
1. แสดงผลการทดสอบทุกโมเดล
2. แสดงเวลาตอบสนองของแต่ละโมเดล
3. แสดง token usage
4. แสดงประวัติการทดสอบ
5. แนะนำโมเดลที่เหมาะสมที่สุด
```

### /mdes-ollama --tokens

แสดง token usage ของแต่ละ model:

```
1. อ่านจาก stats database
2. แสดง input/output tokens
3. แสดง usage percentage
4. แสดง context limit
```

### /mdes-ollama --stats

แสดง usage statistics โดยรวม:

```
1. Total requests
2. Success rate
3. Average response time
4. Token usage by model
5. Most used model
6. Uptime
```

### /mdes-ollama --dev-loop

เริ่ม auto-dev loop:

```
1. ตั้งค่า dev loop configuration
2. เริ่ม health check loop
3. ตั้ง notification
4. บันทึก logs
```

### /mdes-ollama --integrate

รวมกับ GSD skills:

```
1. สแกน GSD skills ที่มีอยู่
2. เพิ่ม integration hooks
3. ทดสอบ connection
4. ยืนยันการรวม
```

## การทำงานภายใน

### Flowchart การทำงาน

```
START
  │
  ├─→ ตรวจสอบ Token Usage
  │     │
  │     ├─→ > 90% → Fallback ไปโมเดลอื่น
  │     └─→ < 90% → ดำเนินการต่อ
  │
  ├─→ ทดสอบ nemotron-3-super:cloud
  │     │
  │     ├─→ สำเร็จ → return "nemotron-3-super:cloud"
  │     └─→ ล้มเหลว → ทดสอบ minimax-m2.5:cloud
  │           │
  │           ├─→ สำเร็จ → return "minimax-m2.5:cloud"
  │           └─→ ล้มเหลว → ... (ทำซ้ำจนหมดทุกโมเดล)
  │
  └─→ ทุก Ollama ล้มเหลว → ทดสอบ codex
        │
        ├─→ สำเร็จ → return "codex"
        └─→ ล้มเหลว → ทดสอบ GPT Pro
              │
              ├─→ สำเร็จ → return "gpt-pro"
              └─→ ล้มเหลว → ทดสอบ GitHub Copilot
                    │
                    ├─→ สำเร็จ → return "github-copilot"
                    └─→ ล้มเหลว → return "NO_WORKING_MODEL"
```

### การตรวจจับข้อผิดพลาด

| ข้อผิดพลาด | ความหมาย | การแก้ไข |
|------------|----------|----------|
| `model not found` | โมเดลไม่มีในรายการ | ลองโมเดลถัดไป |
| `connection failed` | เชื่อมต่อ endpoint ไม่ได้ | ลอง fallback provider |
| `timeout` | ใช้เวลานานเกินไป (>30s) | ลองโมเดลถัดไป |
| `authentication failed` | ตรวจสอบ API key ไม่ผ่าน | ข้ามไป provider ถัดไป |
| `token limit exceeded` | เกิน context window | Fallback ไปโมเดลที่มี context ใหญ่กว่า |
| `all failed` | ทุกโมเดลและ provider ล้มเหลว | แจ้งเตือน BigBoss |

## การบูรณาการกับ Skills อื่น

### สำหรับ /nemotron

`/nemotron` ใช้ `/mdes-ollama` เพื่อ:
- ตรวจสอบว่า nemotron-3-super:cloud ทำงานได้หรือไม่
- ตรวจสอบ token usage ก่อนส่ง prompt
- หากไม่ได้ สำรองไปยังโมเดลอื่นที่ทำงานได้
- spawn sub-agent ด้วยโมเดลที่พร้อมใช้งาน

### สำหรับ /gang

`/gang` ใช้ `/mdes-ollama` เพื่อ:
- เลือกโมเดลที่เหมาะสมสำหรับแต่ละ agent
- ตรวจสอบ token usage ก่อนรัน
- fallback เมื่อโมเดลหลักไม่ทำงาน
- รักษาความต่อเนื่องของ multi-agent operations

### สำหรับ /auto-model

`/auto-model` ใช้ `/mdes-ollama` เพื่อ:
- ขอโมเดลที่พร้อมใช้งาน
- ตรวจสอบสถานะโมเดลปัจจุบัน
- รับ fallback provider หากจำเป็น
- ดู token usage statistics

### สำหรับ GSD Skills

ทุก skill ที่ต้องการ AI model สามารถเรียก `/mdes-ollama` เพื่อ:
- ขอโมเดลที่พร้อมใช้งาน
- ตรวจสอบสถานะโมเดลปัจจุบัน
- รับ fallback provider หากจำเป็น
- ดู token usage
- เริ่ม auto-dev loop

## ตัวอย่างการใช้งานจริง

### ตัวอย่างที่ 1: เริ่มงานใหม่

```
user: /mdes-ollama
→ ตรวจสอบโมเดลอัตโนมัติ...
→ ตรวจสอบ token usage...
→ ทดสอบ nemotron-3-super:cloud... สำเร็จ! ✓
→ Token usage: 3.2%
→ โมเดลพร้อม: nemotron-3-super:cloud
→ พร้อมเริ่มงาน!
```

### ตัวอย่างที่ 2: โมเดลหลักไม่ทำงาน

```
user: /mdes-ollama
→ ตรวจสอบโมเดลอัตโนมัติ...
→ nemotron-3-super:cloud... ล้มเหลว ✗
→ minimax-m2.5:cloud... ล้มเหลว ✗
→ deepseek-v4-flash:cloud... ล้มเหลว ✗
→ ... (ทุก Ollama ล้มเหลว)
→ ทดสอบ Fallback: codex... สำเร็จ! ✓
→ ใช้งาน: codex (OpenAI Codex)
```

### ตัวอย่างที่ 3: ตรวจสอบ token usage

```
user: /mdes-ollama --tokens
→ Token Usage:
   nemotron-3-super: 12,450,000 / 128,000,000 (9.7%)
   minimax-m2.5: 8,200,000 / 1,000,000,000 (0.8%)
   deepseek-v4-flash: 4,100,000 / 200,000,000 (2.1%)
```

### ตัวอย่างที่ 4: ดูรายงาน

```
user: /mdes-ollama --report
→ [แสดงรายงานผลการทดสอบแบบละเอียดพร้อม token usage]
```

### ตัวอย่างที่ 5: เริ่ม auto-dev loop

```
user: /mdes-ollama --dev-loop
→ เริ่ม auto-dev loop...
→ Health check ทุก 5 นาที
→ Fallback threshold: 3 failures
→ แจ้งเตือน: เปิด
→ Dev loop เริ่มทำงาน!
```

### ตัวอย่างที่ 6: รวมกับ GSD

```
user: /mdes-ollama --integrate
→ สแกน GSD skills...
→ รวมกับ gsd-execute-phase ✓
→ รวมกับ gsd-code-review ✓
→ รวมกับ gsd-debug ✓
→ รวมกับ gsd-manager ✓
→ พร้อมใช้งาน!
```

## ความปลอดภัยและข้อควรระวัง

- ตรวจสอบ API keys ก่อนใช้งาน fallback providers
- เก็บ log การทดสอบไว้สำหรับการวิเคราะห์
- แจ้งเตือนเมื่อทุก provider ล้มเหลว
- ทดสอบเป็นระยะเพื่อให้มั่นใจว่ามีโมเดลพร้อมใช้งาน
- **ตรวจสอบ token usage ก่อนทุก operation**

## หมายเหตุทางเทคนิค

- **Endpoint**: mdes.ollama (cloud)
- **Timeout**: 30 วินาทีต่อโมเดล
- **Retry**: ไม่มี retry ในตัว — ข้ามไปโมเดลถัดไป
- **Cache**: ผลการทดสอบมีอายุ 1 ชั่วโมง ยกเว้นใช้ `--force`
- **Config**: บันทึกที่ `~/.claude/skills/mdes-ollama/config.json`
- **Stats**: บันทึกที่ `~/.claude/skills/mdes-ollama/stats/`

## ข้อมูลเพิ่มเติม

- **Author**: Jit Oracle (ช่างฝีมือด้าน multi-agent)
- **Created**: 2026-05-08
- **Purpose**: ระบบประสานงานโมเดลหลักสำหรับทุก AI operations
- **Integration**: ใช้โดย `/nemotron`, `/gang`, `/auto-model` และ GSD skills
- **Central Orchestrator**: ใช่ — เป็นตัวกลางประสานงานหลัก
# Skill: /model-thaiLLM — ส่งงานไปยัง ThaiLLM Gang

> "ปัญญาไทย — เลือกโมเดลให้ถูกกับงาน สร้างผลลัพธ์ที่มีความหมาย"

## ภาพรวม

`/model-thaiLLM` ส่งงานปัจจุบันไปยัง ThaiLLM API และเลือกโมเดลที่เหมาะสมที่สุดโดยอัตโนมัติ
มี 4 โมเดลในกลุ่ม ThaiLLM แต่ละตัวเชี่ยวชาญต่างประเภทงาน

## การใช้งาน

```
/model-thaiLLM [คำอธิบายงาน]
/model-thaiLLM --model [openthaigpt|pathumma|typhoon|thalle] [prompt]
/model-thaiLLM --list
```

## โมเดลที่มี

| ชื่อย่อ | Model ID | เชี่ยวชาญ | เมื่อใช้ |
|---------|----------|-----------|----------|
| `openthaigpt` | OpenThaiGPT-ThaiLLM-8B-Instruct-v7.2 | เทคนิค/โค้ด/ลอจิก | โปรแกรมมิ่ง, debugging, การวิเคราะห์เชิงตรรกะ |
| `pathumma` | Pathumma-ThaiLLM-qwen3-8b-think-3.0.0 | ราชการ/กฎหมาย/ทางการ | เอกสารทางการ, ภาษากฎหมาย, นโยบายรัฐ |
| `typhoon` | Typhoon-S-ThaiLLM-8B-Instruct | ธุรกิจ/สรุป/ทั่วไป | งานธุรกิจ, สรุปเอกสาร, เขียนรายงาน |
| `thalle` | THaLLE-0.2-ThaiLLM-8B-fa | การศึกษา/วิชาการ | วิเคราะห์วิชาการ, อธิบายแนวคิด, บทความ |

## Routing Matrix (Auto-select)

เมื่อไม่ระบุ `--model` ระบบวิเคราะห์งานและเลือกโมเดลตามตาราง:

```
งานมีคำว่า:  code, โค้ด, debug, ฟังก์ชัน, algorithm, script, bash, python
→ openthaigpt

งานมีคำว่า:  กฎหมาย, พ.ร.บ., ราชการ, ระเบียบ, ข้อกำหนด, กรมกอง, กฎระเบียบ
→ pathumma

งานมีคำว่า:  รายงาน, สรุป, ธุรกิจ, ประชุม, นำเสนอ, เสนอขาย, แผน
→ typhoon

งานมีคำว่า:  วิจัย, วิทยานิพนธ์, บทความ, วิชาการ, อธิบาย, ทฤษฎี, ศึกษา
→ thalle

ไม่ตรงกับข้างบน → typhoon (default)
```

## ขั้นตอนการรัน

**1. ระบุโมเดลอัตโนมัติ:**

```bash
# วิเคราะห์งานแล้วเลือกโมเดล
TASK="[งานจากผู้ใช้]"

# ตรวจสอบ routing matrix
if [[ "$TASK" =~ (code|โค้ด|debug|script|python|bash|ฟังก์ชัน|algorithm) ]]; then
  MODEL="openthaigpt"
elif [[ "$TASK" =~ (กฎหมาย|พ.ร.บ.|ราชการ|ระเบียบ|ข้อกำหนด|กรม) ]]; then
  MODEL="pathumma"
elif [[ "$TASK" =~ (วิจัย|วิทยานิพนธ์|บทความ|วิชาการ|ทฤษฎี) ]]; then
  MODEL="thalle"
else
  MODEL="typhoon"
fi

echo "→ เลือก: $MODEL"
```

**2. เรียก ThaiLLM:**

```bash
# ส่งงานพร้อม attribution env
CURRENT_AGENT="$MODEL" CURRENT_SKILL="model-thaiLLM" \
  bash ~/Jit/limbs/thaillm.sh ask "$MODEL" "$TASK"
```

**3. แสดงผลพร้อม attribution:**

```
[ผลลัพธ์จาก ThaiLLM]

— ตอบโดย openthaigpt (ThaiLLM)
```

## ตัวอย่างการใช้งาน

```
/model-thaiLLM เขียน bash script สำหรับ backup ไฟล์
→ เลือก: openthaigpt (พบคำว่า "bash script")
→ เรียก: bash ~/Jit/limbs/thaillm.sh ask openthaigpt "เขียน bash script..."
→ แสดงผลพร้อม attribution

/model-thaiLLM --model pathumma แปล พ.ร.บ.คุ้มครองข้อมูล
→ เรียก: bash ~/Jit/limbs/thaillm.sh ask pathumma "แปล พ.ร.บ.คุ้มครองข้อมูล"

/model-thaiLLM --list
→ แสดงตาราง 4 โมเดลพร้อมคำอธิบาย
```

## คำสั่งที่รันจริง

```bash
# Auto-route (ไม่ระบุ model)
CURRENT_AGENT="typhoon" CURRENT_SKILL="model-thaiLLM" \
  bash ~/Jit/limbs/thaillm.sh ask typhoon "สรุปรายงานประจำเดือน..."

# ระบุ model ตรงๆ
CURRENT_AGENT="openthaigpt" CURRENT_SKILL="model-thaiLLM" \
  bash ~/Jit/limbs/thaillm.sh ask openthaigpt "เขียน Python function..."

# ดูรายชื่อโมเดลจาก API
bash ~/Jit/limbs/thaillm.sh list

# ดู token log
cat ~/Jit/ψ/telemetry/token_log.jsonl | python3 -m json.tool | grep thaillm
```

## Telemetry

ทุกการเรียกจะบันทึกไปที่ `~/Jit/ψ/telemetry/token_log.jsonl`:
```json
{
  "timestamp": "2026-05-23T10:00:00",
  "source": "thaillm",
  "model": "OpenThaiGPT-ThaiLLM-8B-Instruct-v7.2",
  "agent": "openthaigpt",
  "skill": "model-thaiLLM",
  "prompt_tokens": 120,
  "completion_tokens": 350,
  "total_tokens": 470,
  "elapsed_ms": 2340
}
```

## ข้อกำหนด

- ต้องมี `THAILLM_TOKEN` ใน `~/Jit/.env`
- ต้องเข้าถึง `http://thaillm.or.th/api/v1/` ได้
- `~/Jit/limbs/thaillm.sh` ต้องพร้อมใช้งาน

## ข้อมูลเพิ่มเติม

- **Author**: Jit Oracle
- **Created**: 2026-05-23
- **Source**: `~/Jit/limbs/thaillm.sh`
- **Log**: `~/Jit/ψ/telemetry/token_log.jsonl`
- **Related**: `/model-MDES`, `/model-local`, `/model-claude`

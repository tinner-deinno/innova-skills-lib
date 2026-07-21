---
name: learnself
description: "Skill workflow for learnself."
---

# /learnself — ระบบเรียนรู้ตัวเองและส่งต่องานระหว่าง Agent

> "ช่างฝีมือบำเพ็ญบารมี — สร้างเครื่องมือแจกฟรี ให้ผู้คนใช้งาน ทำบุญด้วยปัญญา"

## ภาพรวม

`/learnself` คือทักษะสำหรับระบบเรียนรู้อัตโนมัติและการส่งต่องานระหว่าง Agent ในกลุ่ม Multi-Agent Gangs ระบบนี้ช่วยให้ Agent สามารถ:

- เรียนรู้จากประวัติการทำงานเมื่อไม่มีงานทำ
- ส่งต่องานอัตโนมัติเมื่อต้องเปลี่ยน Agent
- ล้างงานก่อนจบ session

## การใช้งาน

```
/learnself                  # แสดงสถานะการเรียนรู้
/learnself history         # แสดงประวัติการเรียนรู้
/learnself handoff         # แสดงรายการส่งต่อที่รอดำเนินการ
/learnself clear           # ล้างงานทั้งหมดที่รอดำเนินการ
/learnself status          # แสดงสถานะรวมของระบบเรียนรู้ตัวเอง
```

## 1. วิธีการเรียนรู้จากประวัติ (History Learning)

### หลักการ

เมื่อ Agent ไม่มีงานทำ (idle) ระบบจะเปิดให้เรียนรู้จากประวัติการทำงานที่ผ่านมา โดย:

- **อ่านประวัติ session**: วิเคราะห์ session ก่อนหน้าเพื่อเข้าใจบริบท
- **สกัดบทเรียน**: ดึง patterns และ insights ที่เป็นประโยชน์
- **จดจำความรู้**: บันทึกสิ่งที่เรียนรู้ลงใน memory
- **เตรียมพร้อม**: พร้อมรับมือกับงานถัดไปด้วยความเข้าใจที่ลึกซึ้งขึ้น

### กระบวนการ

1. **สแกนประวัติ**: ค้นหา session ล่าสุดใน `.claude/transcripts/`
2. **วิเคราะห์**: ระบุ actions, decisions และ outcomes
3. **สกัด learnings**: หา patterns ที่ซ้ำและ best practices
4. **บันทึก**: เขียนลงใน `ψ/memory/` หรือ `learnings.json`

### การตั้งค่า

```json
{
  "learnself": {
    "enabled": true,
    "idleThreshold": 300,
    "maxSessionsToLearn": 10,
    "storeLocation": "ψ/memory/learnings.json"
  }
}
```

## 2. กลไกการส่งต่อ (Handoff Mechanism)

### หลักการ

เมื่อต้องส่งต่องานจาก Agent หนึ่งไปยังอีก Agent หนึ่ง (อาจอยู่คนละ gang) ระบบจะ:

- **สร้าง handoff package**: รวบรวมบริบท สถานะ และสิ่งที่ต้องทำ
- **แจ้งเตือน**: แจ้ง agent ปลายทางว่ามีงานรอ
- **รอการรับ**: รอจนกว่า agent ใหม่จะรับงาน
- **ติดตาม**: ตรวจสอบว่างานถูกส่งต่อสำเร็จ

### Handoff Package Structure

```json
{
  "handoff": {
    "id": "unique-id",
    "from": "agent-name/gang-name",
    "to": "target-agent/target-gang",
    "priority": "high|normal|low",
    "created": "ISO-timestamp",
    "context": {
      "session": "session-id",
      "task": "task-description",
      "files": ["list-of-files"],
      "progress": "current-progress"
    },
    "status": "pending|accepted|completed"
  }
}
```

### สถานะการส่งต่อ

| Status | ความหมาย |
|--------|----------|
| pending | รอการรับ |
| accepted | Agent ใหม่รับงานแล้ว |
| completed | งานเสร็จสมบูรณ์ |
| failed | การส่งต่อล้มเหลว |

## 3. ขั้นตอนการล้างงาน (Work Clearing)

### ก่อนจบ Session

เมื่อ session กำลังจะจบ หรือเมื่อใช้คำสั่ง `/learnself clear`:

1. **รวบรวมงานค้าง**: ตรวจสอบ task list ที่ยังไม่เสร็จ
2. **จัดลำดับความสำคัญ**: จัดกลุ่มตามความเร่งด่วน
3. **สร้าง handoff**: สำหรับงานที่ต้องส่งต่อ
4. **บันทึกสถานะ**: เขียนบันทึกไว้ใน inbox
5. **ยืนยัน**: แจ้ง human ว่างานถูกจัดการเรียบร้อย

### การจัดการงานค้าง

```json
{
  "pending_work": [
    {
      "task": "ชื่อ task",
      "status": "in_progress|blocked|pending",
      "priority": "high|normal|low",
      "handed_off_to": "agent@gang"
    }
  ]
}
```

### การตั้งค่าการล้างงานอัตโนมัติ

```json
{
  "learnself": {
    "autoClear": true,
    "clearOnSessionEnd": true,
    "minimizePending": true
  }
}
```

## 4. การรวมกับ Multi-Agent Gangs

### การทำงานร่วมกับ /gang

`/learnself` ทำงานร่วมกับ `/gang` ดังนี้:

- **Gang Awareness**: แต่ละ gang มี memory แยกต่างหาก
- **Cross-Gang Handoff**: ส่งต่องานข้าม gang ได้
- **Shared Learnings**: บาง learnings สามารถแชร์ระหว่าง gang ได้

### Gang Learning Structure

```
ψ/
├── memory/
│   ├── gang-alpha/
│   │   └── learnings.json    # ข้อเรียนรู้ของ gang นี้
│   ├── gang-beta/
│   │   └── learnings.json
│   └── shared/
│       └── cross-gang.json   # ข้อเรียนรู้ที่แชร์กัน
```

### การตั้งค่า Multi-Agent

```json
{
  "gang": {
    "learnself": {
      "enabled": true,
      "shareLearnings": ["patterns", "tools"],
      "handoffEnabled": true
    }
  }
}
```

## สถานะและการตรวจสอบ

### การตรวจสอบสถานะ

- `/learnself status`: แสดงสถานะรวม
- `/learnself history`: แสดงประวัติการเรียนรู้
- `/learnself handoff`: แสดงงานที่ต้องส่งต่อ

### การแก้ไขปัญหา

- ถ้า handoff ล้มเหลว: ตรวจสอบ network และ permission
- ถ้า learning ไม่ทำงาน: ตรวจสอบ file permissions
- ถ้า clear ไม่ทำงาน: ตรวจสอบว่าไม่มี task ที่กำลัง active

## ข้อจำกัด

- ต้องมีสิทธิ์เข้าถึง `ψ/memory/` และ `.claude/transcripts/`
- Cross-gang handoff ต้องมี network connection ระหว่าง gang
- Learning จะทำงานเฉพาะเมื่อ idle threshold ถูก trigger

## ดูเพิ่มเติม

- `/gang` — ระบบ Multi-Agent Gangs
- `/recap` — สรุป session และ handoff
- `/rrr` — Session retrospective
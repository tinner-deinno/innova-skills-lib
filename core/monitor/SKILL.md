---
name: monitor
description: "Skill workflow for monitor."
---

# /monitor — ระบบ TUI Monitoring สำหรับ Sub-Agents

## ภาพรวม

`/monitor` เป็นทักษะสำหรับติดตามและ наблюдател (observe) สถานะของ sub-agents แบบเรียลไทม์ผ่าน Terminal User Interface (TUI)

ระบบนี้ทำงานร่วมกับ **multi-agent-gangs** ที่ `~/multi-agent-gangs/` เพื่อแสดง:
- สถานะการทำงานของ agent
- แถบความก้าวหน้า (progress bars)
- ข้อมูลเวลาและการจับเวลา
- สถานะของ gangs ทั้งหมด

## การใช้งาน

### /monitor
แสดงหน้าหลักของ monitoring dashboard

```
/monitor
```

แสดงภาพรวมของระบบทั้งหมด:
- จำนวน agents ที่กำลังทำงาน
- สถานะ gangs ทั้ง 4 กลุ่ม
- Logs ล่าสุด
- สรุปการทำงาน

### /monitor agents
แสดง agents ทั้งหมดที่กำลังทำงาน

```
/monitor agents
```

แสดงรายการ:
- ชื่อ agent และสถานะ
- เวลาที่เริ่มทำงาน
- ความก้าวหน้า (%)
- Task ปัจจุบัน
- Resource usage

### /monitor gangs
แสดงสถานะของ gangs ทั้ง 4 กลุ่ม

```
/monitor gangs
```

แสดงสำหรับแต่ละ gang:
- **Architects** — การออกแบบและวางแผน
- **Builders** — การพัฒนาและเขียนโค้ด
- **Auditors** — การตรวจสอบและทบทวน
- **Oracles** — การวิเคราะห์และให้คำปรึกษา

แต่ละ gang แสดง:
- จำนวน agents ใน gang
- สถานะโดยรวม (active/idle/error)
- Tasks ที่กำลังทำงาน

### /monitor logs
แสดง logs ล่าสุด

```
/monitor logs
```

Options:
- `/monitor logs --error` — แสดงเฉพาะ errors
- `/monitor logs --agent [name]` — logs เฉพาะ agent
- `/monitor logs --tail 50` — แสดง 50 บรรทัดล่าสุด

### /monitor watch
เริ่ม monitoring แบบต่อเนื่อง

```
/monitor watch
```

หรือกำหนด interval:
```
/monitor watch --interval 5s
/monitor watch --interval 30s
```

หยุดการ watch:
```
/monitor watch --stop
```

### /monitor clear
ล้างหน้าจอ monitor

```
/monitor clear
```

## ตัวอย่างการใช้งาน

### ตัวอย่างที่ 1: ตรวจสอบสถานะทั้งหมด
```
User: /monitor
```
ผลลัพธ์: แสดง dashboard หลักพร้อมภาพรวมของระบบ

### ตัวอย่างที่ 2: ติดตาม agents เฉพาะ
```
User: /monitor agents
```
ผลลัพธ์: แสดงรายการ agents ทั้งหมดพร้อมสถานะ

### ตัวอย่างที่ 3: ดู gangs ทั้ง 4 กลุ่ม
```
User: /monitor gangs
```
ผลลัพธ์: แสดงตารางสถานะของ Architects, Builders, Auditors, Oracles

### ตัวอย่างที่ 4: ดู errors ล่าสุด
```
User: /monitor logs --error
```
ผลลัพธ์: แสดง error logs ทั้งหมด

### ตัวอย่างที่ 5: monitoring ต่อเนื่อง
```
User: /monitor watch --interval 10s
```
ผลลัพธ์: อัพเดทสถานะทุก 10 วินาทีจนกว่าจะหยุด

## การรวมกับ multi-agent-gangs

ระบบ `/monitor` ทำงานร่วมกับ multi-agent-gangs โดย:

### โครงสร้าง Gang
- **Architects** — วางแผนและออกแบบ architecture
- **Builders** — เขียนและปรับปรุงโค้ด
- **Auditors** — ตรวจสอบคุณภาพและ security
- **Oracles** — ให้คำปรึกษาและวิเคราะห์

### การอ่านสถานะ
Monitor อ่านข้อมูลจาก:
- State files ใน `~/multi-agent-gangs/state/`
- Log files ใน `~/multi-agent-gangs/logs/`
- Agent status จาก running processes

### การตั้งค่า
สร้างไฟล์ config ที่ `~/.claude/skills/monitor/config.json`:

```json
{
  "gangsPath": "~/multi-agent-gangs",
  "refreshInterval": 5000,
  "showProgress": true,
  "theme": "default"
}
```

## Tips

- ใช้ `/monitor watch` สำหรับการติดตามระหว่างการพัฒนา
- `/monitor clear` ช่วยล้างหน้าจอเมื่อมีข้อมูลมาก
- รวม `/monitor` กับ `/gang status` เพื่อดูภาพรวม

## Troubleshooting

**ไม่แสดงข้อมูล:**
- ตรวจสอบว่า multi-agent-gangs กำลังทำงาน
- ตรวจสอบ path: `~/multi-agent-gangs/`

**ไม่อัพเดท:**
- ลอง `/monitor clear` แล้วเริ่มใหม่
- ตรวจสอบว่า agents ยังทำงานอยู่

## Related Commands

- `/gang` — จัดการ multi-agent gangs
- `/trace` — ค้นหา projects และ code
- `/recap` — สรุปสถานะ session
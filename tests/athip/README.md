# ชุดการทดสอบอัตโนมัติ: ผู้ทดสอบ อธิป (athip)

ชุดทดสอบนี้ครอบคลุมการทำงานของ **โมดูลโครงสร้างพื้นฐานและการสื่อสารแบบเรียลไทม์** รวมทั้งหมด **5 Test Cases**:
- **Module 7: ระบบโครงสร้างพื้นฐานและการสื่อสารแบบเรียลไทม์ (System Infrastructure & Real-Time - FR-SYS)**: TC-064 ถึง TC-068

---

## 📋 รายการ Test Cases

| รหัส TC | รหัส FR | ชื่อ Test Case | ไฟล์ทดสอบ |
|---|---|---|---|
| **TC-064** | FR-SYS-001 | การเชื่อมต่อ WebSocket สองทางอัปเดตข้อมูลโดยไม่ต้องรีเฟรช | `test_infrastructure.py` |
| **TC-065** | FR-SYS-002 | จัดเก็บข้อมูลลง SQLite อย่างถูกต้องและไม่สูญหาย (Persistence) | `test_infrastructure.py` |
| **TC-066** | FR-SYS-003 | กำหนด Port ผ่าน Environment Variable | `test_infrastructure.py` |
| **TC-067** | FR-SYS-003 | ใช้ Port เริ่มต้น 3000 เมื่อไม่ได้กำหนดค่า PORT | `test_infrastructure.py` |
| **TC-068** | FR-SYS-004 | สร้างและรันแอปพลิเคชันด้วย Docker Compose | `test_infrastructure.py` |

---

## 🚀 วิธีการรันชุดทดสอบของอธิป

```bash
# รันการทดสอบทั้งหมดของอธิป (5 Cases)
pytest tests/athip/ -v

# รันเฉพาะไฟล์ทดสอบโครงสร้างพื้นฐาน
pytest tests/athip/test_infrastructure.py -v
```

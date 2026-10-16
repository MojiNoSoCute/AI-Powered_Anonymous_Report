# ชุดการทดสอบอัตโนมัติ: ผู้ทดสอบ วุฒิชัย (suttichai)

ชุดทดสอบนี้ครอบคลุมการทำงานของ **2 โมดูลหลัก** รวมทั้งหมด **23 Test Cases**:
1. **Module 3: ระบบติดตามสถานะและการสนทนาลับ 2 ทาง (Status Tracking & 2-Way Encrypted Chat - FR-TRK)**: TC-031 ถึง TC-038
2. **Module 4: ระบบจัดการสำนวนคดีสำหรับเจ้าหน้าที่ (Case Management Dashboard - FR-CAS)**: TC-039 ถึง TC-053

---

## 📋 รายการ Test Cases

| รหัส TC | รหัส FR | ชื่อ Test Case | ไฟล์ทดสอบ |
|---|---|---|---|
| **TC-031** | FR-TRK-001 | ค้นหารายงานด้วย Report ID และ PIN ที่ถูกต้อง | `test_tracking_chat.py` |
| **TC-032** | FR-TRK-001 | ค้นหารายงานด้วย PIN ที่ไม่ถูกต้อง | `test_tracking_chat.py` |
| **TC-033** | FR-TRK-001 | ค้นหารายงานด้วย Report ID ที่ไม่มีอยู่ในระบบ | `test_tracking_chat.py` |
| **TC-034** | FR-TRK-002 | แสดงไทม์ไลน์สถานะคดี 4 ขั้นและไฮไลต์สถานะปัจจุบัน | `test_tracking_chat.py` |
| **TC-035** | FR-TRK-003 | ผู้แจ้งสนทนาลับ 2 ทางกับเจ้าหน้าที่แบบเรียลไทม์ | `test_tracking_chat.py` |
| **TC-036** | FR-TRK-004 | แสดงสถานะกำลังพิมพ์ (Typing Indicator) | `test_tracking_chat.py` |
| **TC-037** | FR-TRK-005 | ผู้แจ้งแนบหลักฐานเพิ่มเติมผ่านหน้าติดตามสถานะ | `test_tracking_chat.py` |
| **TC-038** | FR-TRK-006 | หน้าต่างแชทเลื่อนไปข้อความล่าสุดอัตโนมัติ | `test_tracking_chat.py` |
| **TC-039** | FR-CAS-001 | บุคคลที่ไม่ได้ล็อกอินเข้าแท็บจัดการรายงานไม่ได้ (Protected Route) | `test_case_management.py` |
| **TC-040** | FR-CAS-002 | ค้นหาและกรองตารางคดีแบบทันที (Live Filtering) | `test_case_management.py` |
| **TC-041** | FR-CAS-002 | ตารางคดีแบ่งหน้า (Pagination) เมื่อมีข้อมูลจำนวนมาก | `test_case_management.py` |
| **TC-042** | FR-CAS-003 | เปลี่ยนสถานะคดีด่วนในคลิกเดียวและแจ้งผู้แจ้งแบบเรียลไทม์ | `test_case_management.py` |
| **TC-043** | FR-CAS-004 | ปรับระดับความเร่งด่วนของคดีด่วน | `test_case_management.py` |
| **TC-044** | FR-CAS-005 | ปรับเปลี่ยนหมวดหมู่เรื่องร้องเรียนด่วนในคลิกเดียว | `test_case_management.py` |
| **TC-045** | FR-CAS-006 | แก้ไขข้อมูลสำนวนคดีแบบเต็ม (Full Edit Mode) | `test_case_management.py` |
| **TC-046** | FR-CAS-007 | บันทึกช่วยจำภายในของเจ้าหน้าที่ไม่แสดงต่อผู้แจ้ง (Privacy) | `test_case_management.py` |
| **TC-047** | FR-CAS-008 | ตรวจสอบสื่อหลักฐานด้วย Lightbox (Images & Videos) | `test_case_management.py` |
| **TC-048** | FR-CAS-009 | เจ้าหน้าที่อัปโหลดหลักฐานเพิ่มเติมในคดี | `test_case_management.py` |
| **TC-049** | FR-CAS-010 | ลบไฟล์หลักฐานที่ไม่เกี่ยวข้องออกจากสำนวนคดี | `test_case_management.py` |
| **TC-050** | FR-CAS-011 | ห้องแชทเจ้าหน้าที่กับผู้แจ้ง พร้อมตัวนับข้อความที่ยังไม่ได้อ่าน | `test_case_management.py` |
| **TC-051** | FR-CAS-012 | ลบสำนวนคดีพร้อมกล่องยืนยัน (Confirmation Dialog) | `test_case_management.py` |
| **TC-052** | FR-CAS-012 | ยกเลิกการลบสำนวนคดีใน Confirm Dialog | `test_case_management.py` |
| **TC-053** | FR-CAS-013 | ส่งออกข้อมูลรายงานเป็นไฟล์ CSV (UTF-8 with BOM) | `test_case_management.py` |

---

## 🚀 วิธีการรันชุดทดสอบของวุฒิชัย

```bash
# รันการทดสอบทั้งหมดของวุฒิชัย (23 Cases)
pytest tests/suttichai/ -v

# รันเฉพาะการทดสอบการติดตามสถานะและแชท
pytest tests/suttichai/test_tracking_chat.py -v

# รันเฉพาะการทดสอบการจัดการสำนวนคดี (Case Management)
pytest tests/suttichai/test_case_management.py -v
```

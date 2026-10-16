# ชุดการทดสอบอัตโนมัติ: ผู้ทดสอบ สหรัฐ (saharat)

ชุดทดสอบนี้ครอบคลุมการทำงานของ **2 โมดูลหลัก** รวมทั้งหมด **10 Test Cases**:
1. **Module 5: ระบบแดชบอร์ดสถิติและการวิเคราะห์ (Analytics Dashboard - FR-ANA)**: TC-054 ถึง TC-057
2. **Module 6: ระบบการยืนยันตัวตนและความปลอดภัย (Authentication & Security - FR-SEC)**: TC-058 ถึง TC-063

---

## 📋 รายการ Test Cases

| รหัส TC | รหัส FR | ชื่อ Test Case | ไฟล์ทดสอบ |
|---|---|---|---|
| **TC-054** | FR-ANA-001 | แสดงตัวชี้วัดสรุปผลภาพรวม (KPI Summary Cards) 5 การ์ด | `test_analytics_dashboard.py` |
| **TC-055** | FR-ANA-002 | กราฟสัดส่วนเรื่องร้องเรียนแยกตามหมวดหมู่ (7 หมวด) | `test_analytics_dashboard.py` |
| **TC-056** | FR-ANA-003 | กราฟสัดส่วนระดับความเร่งด่วน | `test_analytics_dashboard.py` |
| **TC-057** | FR-ANA-004 | แนวโน้มรายเดือนและการจัดอันดับพื้นที่เสี่ยง (Hotspots) | `test_analytics_dashboard.py` |
| **TC-058** | FR-SEC-001 | เจ้าหน้าที่เข้าสู่ระบบด้วยบัญชี admin (สิทธิ์เต็ม) | `test_auth_security.py` |
| **TC-059** | FR-SEC-001 | เจ้าหน้าที่สืบสวนเข้าสู่ระบบด้วยบัญชี officer1 | `test_auth_security.py` |
| **TC-060** | FR-SEC-001 | เข้าสู่ระบบด้วยรหัสผ่านหรือบัญชีที่ไม่ถูกต้อง (Error Alert) | `test_auth_security.py` |
| **TC-061** | FR-SEC-002 | เจ้าหน้าที่ออกจากระบบและเคลียร์ Session | `test_auth_security.py` |
| **TC-062** | FR-SEC-003 | ระบบไม่จัดเก็บข้อมูลส่วนบุคคลของผู้แจ้ง (Anonymity Enforcement) | `test_auth_security.py` |
| **TC-063** | FR-SEC-004 | บันทึกประวัติการแก้ไข (Audit Trail Logging) | `test_auth_security.py` |

---

## 🚀 วิธีการรันชุดทดสอบของสหรัฐ

```bash
# รันการทดสอบทั้งหมดของสหรัฐ (10 Cases)
pytest tests/saharat/ -v

# รันเฉพาะการทดสอบสถิติและแดชบอร์ด
pytest tests/saharat/test_analytics_dashboard.py -v

# รันเฉพาะการทดสอบความปลอดภัยและการยืนยันตัวตน
pytest tests/saharat/test_auth_security.py -v
```

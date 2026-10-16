# โครงสร้างชุดทดสอบอัตโนมัติ Selenium Python (TrustLine E2E Test Suite)
## มหาวิทยาลัยราชภัฏนครปฐม (Nakhon Pathom Rajabhat University)

ชุดทดสอบอัตโนมัตินี้พัฒนาด้วย **Python 3**, **Selenium WebDriver** (Chrome Headless) และ **pytest** โดยอ้างอิงข้อกำหนดและกรณีทดสอบทั้งหมดจากเอกสารในโฟลเดอร์ `docs/`:
1. `docs/FUNCTIONAL_REQUIREMENTS.md` (ข้อกำหนดความต้องการเชิงหน้าที่ FRS ทั้งหมด 7 โมดูล)
2. `docs/Annonymous-Test-Cases.docx` (กรณีทดสอบ E2E ทั้งหมด 68 กรณีทดสอบ)
3. `docs/Annonymous-Test-Plan-and-Report.docx` (แผนการทดสอบและผู้รับผิดชอบการทดสอบ)

---

## 👥 โครงสร้างโฟลเดอร์แยกตามผู้ทดสอบ (Test Directory Structure by Tester)

```
tests/
├── conftest.py                   # Pytest fixtures, Selenium WebDriver headless setup & shared helpers
├── requirements.txt              # รายการ Dependencies (selenium, pytest, requests, websockets)
├── run_tests.py                  # สคริปต์กลางสำหรับสั่งรัน Test Suite ทั้งหมดหรือเลือกตามรายบุคคล
├── README.md                     # เอกสารอธิบายโครงสร้างและการใช้งาน
│
├── watcharakorn/                 # [ผู้ทดสอบ: วัชรากร] รวม 30 Test Cases (TC-001 - TC-030)
│   ├── test_sub_module.py        # Module 1: Anonymous Report Submission (TC-001 ถึง TC-021)
│   ├── test_ai_module.py         # Module 2: AI Smart Assistant Analysis (TC-022 ถึง TC-030)
│   └── README.md
│
├── suttichai/                    # [ผู้ทดสอบ: วุฒิชัย / สุทธิชัย] รวม 23 Test Cases (TC-031 - TC-053)
│   ├── test_tracking_chat.py     # Module 3: Status Tracking & 2-Way Chat (TC-031 ถึง TC-038)
│   ├── test_case_management.py   # Module 4: Case Management Dashboard (TC-039 ถึง TC-053)
│   └── README.md
│
├── saharat/                      # [ผู้ทดสอบ: สหรัฐ] รวม 10 Test Cases (TC-054 - TC-063)
│   ├── test_analytics_dashboard.py # Module 5: Analytics Dashboard & Metrics (TC-054 ถึง TC-057)
│   ├── test_auth_security.py     # Module 6: Authentication & Security (TC-058 ถึง TC-063)
│   └── README.md
│
└── athip/                        # [ผู้ทดสอบ: อธิป] รวม 5 Test Cases (TC-064 - TC-068)
    ├── test_infrastructure.py    # Module 7: Infrastructure, WebSocket & SQLite (TC-064 ถึง TC-068)
    └── README.md
```

---

## 📊 สรุปความครอบคลุมการทดสอบ (Test Coverage Matrix)

| ผู้ทดสอบ | โฟลเดอร์ | โมดูลที่รับผิดชอบ | ขอบเขต Test Cases | จำนวนกรณีทดสอบ |
|---|---|---|---|---|
| **วัชรากร (watcharakorn)** | `tests/watcharakorn/` | Module 1: การส่งรายงานเบาะแสลับ<br>Module 2: AI Smart Assistant | TC-001 ถึง TC-030 | **30 Cases** |
| **วุฒิชัย (suttichai)** | `tests/suttichai/` | Module 3: ติดตามสถานะและแชทลับ 2 ทาง<br>Module 4: ระบบจัดการสำนวนคดี | TC-031 ถึง TC-053 | **23 Cases** |
| **สหรัฐ (saharat)** | `tests/saharat/` | Module 5: แดชบอร์ดสถิติและการวิเคราะห์<br>Module 6: การยืนยันตัวตนและความปลอดภัย | TC-054 ถึง TC-063 | **10 Cases** |
| **อธิป (athip)** | `tests/athip/` | Module 7: ระบบโครงสร้างพื้นฐาน, WebSocket & SQLite | TC-064 ถึง TC-068 | **5 Cases** |
| **รวมทั้งหมด** | `tests/` | **ครบถ้วนทั้ง 7 โมดูลตามเอกสาร docs** | **TC-001 ถึง TC-068** | **68 Cases** |

---

## 🛠️ การติดตั้งเครื่องมือที่จำเป็น (Prerequisites & Installation)

### 1.1 ตรวจสอบเวอร์ชัน Python
ต้องมี **Python 3.10+ / 3.11+ / 3.12+ / 3.14+** ติดตั้งในเครื่อง:
```bash
# Windows:
python --version

# macOS / Linux:
python3 --version
```

### 1.2 การใช้งาน Google Chrome & ChromeDriver
- **รองรับ ChromeDriver ทุกรูปแบบ (Auto / Custom / Zero-Config):**
  - **แบบที่ 1 (แนะนำที่สุด - ทำงานอัตโนมัติ):** เพียงแค่เครื่องของคุณมี **Google Chrome** ติดตั้งอยู่ตามปกติ ตัวโค้ดใน `conftest.py` จะจับคู่และจัดการ **ChromeDriver** ผ่าน Selenium Manager / `webdriver-manager` ให้อัตโนมัติทันที
  - **แบบที่ 2 (ระบุไฟล์เอง):** หากดาวน์โหลด `chromedriver.exe` (Windows) หรือ `chromedriver` (Mac/Linux) มาแล้ว สามารถวางไว้ที่โฟลเดอร์หลักของโปรเจกต์ หรือกำหนด Environment Variable `CHROMEDRIVER_PATH`
  - รองรับทั้งโหมด **Headless** (รันเบื้องหลังความเร็วสูง) และโหมด **Headed** (เปิดหน้าต่าง Google Chrome จริงขึ้นมาด้วย `--headed`)

### 1.3 ติดตั้ง Dependencies สำหรับ Python
⚠️ **หากยังไม่ได้ติดตั้ง Library สำหรับ Selenium & ChromeDriver** ให้รันคำสั่งติดตั้งเพียงครั้งเดียว:

- **บน Windows (Command Prompt หรือ PowerShell):**
  ```cmd
  python -m pip install -r tests/requirements.txt
  ```

- **บน macOS / Linux:**
  ```bash
  pip3 install -r tests/requirements.txt
  # หรือหากติดสิทธิ์ระดับระบบ:
  pip3 install -r tests/requirements.txt --break-system-packages
  ```
*(Dependencies: `selenium>=4.20.0`, `pytest>=8.0.0`, `requests>=2.31.0`, `websockets>=12.0`, `webdriver-manager>=4.0.0`)*

---

## 🌐 การทดสอบกับเว็บจริง (Live Website Testing)

ชุดทดสอบทั้งหมดถูกตั้งค่าเริ่มต้นให้เชื่อมต่อไปยัง **เว็บจริงบน Cloud ทันที**:
```
https://anonymous-report.ai.studio/
```
> 🚀 **ข้อดี:** ไม่จำเป็นต้องเปิดรัน Server ในเครื่อง สามารถสั่งรัน Selenium ChromeDriver ไปทดสอบกับเว็บจริงบน Cloud ได้ทันที!
> 
> หากต้องการสลับไปทดสอบกับ URL อื่น สามารถระบุ `--url` ได้:
> `python tests/run_tests.py --url https://anonymous-report.ai.studio/`

---

## 🚀 คำสั่งการรันการทดสอบ (Execution Commands)

### 1. สั่งรันผ่านตัวรันกลาง `run_tests.py` (แนะนำที่สุด - สรุปรายงานสถานะแบบตาราง)

#### 🟢 รันการทดสอบทั้งหมด (ครบ 68 Test Cases จากทั้ง 4 ท่าน)
```cmd
# Windows:
python tests/run_tests.py --tester all

# macOS / Linux:
python3 tests/run_tests.py --tester all
```

#### 🔵 รันแยกเฉพาะของแต่ละคน
```cmd
# 1. วัชรากร (watcharakorn) - Module 1 & 2 (30 Cases)
python tests/run_tests.py --tester watcharakorn

# 2. วุฒิชัย (suttichai) - Module 3 & 4 (23 Cases)
python tests/run_tests.py --tester suttichai

# 3. สหรัฐ (saharat) - Module 5 & 6 (10 Cases)
python tests/run_tests.py --tester saharat

# 4. อธิป (athip) - Module 7 (5 Cases)
python tests/run_tests.py --tester athip
```

#### 🖥️ โหมดเปิดหน้าต่างเบราว์เซอร์ Chrome ให้เห็นการทำงานจริง (Headed Mode)
หากต้องการเห็นหน้าต่างเบราว์เซอร์เปิดขึ้นมาคลิกและกรอกข้อมูลอัตโนมัติแบบเรียลไทม์:
```cmd
python tests/run_tests.py --tester watcharakorn --headed
```

---

### 2. สั่งรันผ่าน `pytest` โดยตรง (สำหรับ Windows ให้ใช้ `python -m pytest` เสมอ)
```cmd
# รันทั้งหมด:
python -m pytest tests/ -v

# รันแยกเฉพาะโฟลเดอร์แต่ละคน:
python -m pytest tests/watcharakorn/ -v    # วัชรากร (30 Cases)
python -m pytest tests/suttichai/ -v      # วุฒิชัย (23 Cases)
python -m pytest tests/saharat/ -v        # สหรัฐ (10 Cases)
python -m pytest tests/athip/ -v          # อธิป (5 Cases)
```

# 🟡 รันเฉพาะไฟล์ย่อยประจำโมดูล:
pytest tests/watcharakorn/test_sub_module.py -v         # Module 1 (Submission: TC-001 ถึง TC-021)
pytest tests/watcharakorn/test_ai_module.py -v          # Module 2 (AI Analysis: TC-022 ถึง TC-030)
pytest tests/suttichai/test_tracking_chat.py -v         # Module 3 (Tracking & Chat: TC-031 ถึง TC-038)
pytest tests/suttichai/test_case_management.py -v       # Module 4 (Case Manager: TC-039 ถึง TC-053)
pytest tests/saharat/test_analytics_dashboard.py -v     # Module 5 (Analytics: TC-054 ถึง TC-057)
pytest tests/saharat/test_auth_security.py -v           # Module 6 (Auth & Security: TC-058 ถึง TC-063)
pytest tests/athip/test_infrastructure.py -v            # Module 7 (Infrastructure: TC-064 ถึง TC-068)

# 🔍 รันเจาะจงเฉพาะชื่อ Test Case:
pytest tests/ -k "test_tc001" -v
pytest tests/ -k "test_tc035" -v
```

---

## 🏆 ผลการรันการทดสอบ (Verification Status)
- ✅ **วัชรากร (watcharakorn):** 30/30 Cases ผ่านทั้งหมด (100%)
- ✅ **วุฒิชัย (suttichai):** 23/23 Cases ผ่านทั้งหมด (100%)
- ✅ **สหรัฐ (saharat):** 10/10 Cases ผ่านทั้งหมด (100%)
- ✅ **อธิป (athip):** 5/5 Cases ผ่านทั้งหมด (100%)
- 🌟 **รวมทั้งหมด:** **68/68 Test Cases ผ่านทั้งหมด (100%)**

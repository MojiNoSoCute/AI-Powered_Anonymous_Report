# NPRU Sentinel - Anonymous Report Portal (TrustLine)
ระบบแจ้งเบาะแสและจัดการข้อมูลอย่างเป็นระบบ ปลอดภัย และเข้ารหัส (Nakhon Pathom Rajabhat University)

---

## 📌 บทนำ (Introduction)
**NPRU Sentinel (TrustLine)** เป็นระบบเว็บแอปพลิเคชันสำหรับรับแจ้งเรื่องร้องเรียน เบาะแส และปัญหาภายในมหาวิทยาลัยราชภัฏนครปฐม โดยให้ความสำคัญสูงสุดกับ **ความปลอดภัย ความเป็นนิรนาม (Anonymity) และการปกป้องตัวตนของผู้แจ้ง** พร้อมด้วยระบบ **AI Smart Assistant (Gemini 3.6 Flash)** ที่ช่วยคัดกรองหมวดหมู่ ประเมินความเร่งด่วน สรุปข้อมูลอัตโนมัติ และระบบจัดการเคสสำหรับผู้ดูแลระบบ (Admin) แบบครบวงจร

---

## ✨ ฟีเจอร์หลัก (Key Features)

1. **🔒 แจ้งเบาะแสนิรนาม 100% (100% Anonymous Reporting)**
   - ไม่ต้องลงชื่อเข้าใช้ ไม่เก็บ IP Address หรือข้อมูลระบุตัวตน
   - แนบไฟล์หลักฐาน (รูปภาพ, PDF, เอกสาร) พร้อมระบบเข้ารหัสข้อมูล
   - เข้ารหัส PIN ด้วย SHA-256 เพื่อใช้เข้าถึงรายงาน

2. **🤖 AI Smart Assistant (Gemini 3.6 Flash)**
   - วิเคราะห์ข้อความคำอธิบายภาษาไทยแบบเรียลไทม์
   - จัดหมวดหมู่เรื่องร้องเรียนอัตโนมัติ 7 หมวดหมู่ (Harassment, Fraud, Academic, Technical, Safety, Compliance, Teaching)
   - ประเมินระดับความเร่งด่วนเบื้องต้น พร้อมเหตุผลประกอบและคำสำคัญ (Keywords)

3. **🛠️ ระบบจัดการและแก้ไขข้อมูลสำหรับผู้ดูแลระบบ (Admin Full Management)**
   - **แก้ไขข้อมูลสำนวนคดีได้ครบทุกส่วน (Full Edit Mode):** แก้ไขหมวดหมู่, ความเร่งด่วน, สถานะ, ผู้รับผิดชอบ, วันที่/สถานที่, รหัส PIN, รายละเอียด และบันทึกข้อค้นพบภายใน (Internal Memo)
   - **เปลี่ยนสถานะและความเร่งด่วนได้ทันที (Direct In-Table Selectors):** เปลี่ยนค่าผ่านตารางหรือหน้าต่างรายละเอียดเคสได้ในคลิกเดียว
   - **ระบบคัดกรองและค้นหาขั้นสูง:** กรองตามหมวดหมู่ ความเร่งด่วน สถานะ หรือพิมพ์ค้นหาตามรหัสเคส/คีย์เวิร์ด
   - **ส่งออกข้อมูล (Export):** รองรับการส่งออกข้อมูลเป็น CSV และ JSON
   - **บันทึกประวัติการตรวจสอบ (Audit Trail / Logs):** ติดตามทุกการเปลี่ยนแปลงสถานะและการแก้ไขข้อมูล

4. **🔍 ติดตามสถานะและการสนทนาลับ 2 ทาง (Status Tracking & 2-Way Secure Chat)**
   - ผู้แจ้งใช้ **Report ID** (เช่น `TL-2024-X89K`) + **PIN** ในการติดตามสถานะ
   - สามารถแชทคุยกับเจ้าหน้าที่ผู้รับผิดชอบคดีได้แบบเรียลไทม์ (WebSocket) โดยยังคงสถานะนิรนาม 100%

5. **📊 แดชบอร์ดสถิติและการวิเคราะห์ (Analytics Dashboard)**
   - กราฟสรุปสถิติเรื่องร้องเรียนแยกตามหมวดหมู่ ความเร่งด่วน และแนวโน้มรายเดือน
   - แผนภูมิวิเคราะห์จุดเสี่ยงของพื้นที่ภายในมหาวิทยาลัย

6. **🐍 รองรับสถาปัตยกรรม 2 รูปแบบ (Dual Architecture Support)**
   - **Full-Stack Node.js (React + Vite + Express + Gemini AI SDK + WebSockets)** สำหรับการรันบน Cloud Run / AI Studio
   - **Python Flask + SQLite Backend (`app.py`, `schema.sql`)** สำหรับนำไป Deploy บน Python Server อิสระ

---

## 📖 คู่มือการใช้งาน (How to Use)

### 👤 1. สำหรับนักศึกษาและบุคคลทั่วไป (Whistleblower / General Public)

#### ขั้นตอนที่ 1: สร้างรายงานแจ้งเบาะแส (Submit a Report)
1. เข้าสู่หน้าหลักของระบบ เลือกแท็บ **"สร้างรายงานใหม่"**
2. เลือก **หมวดหมู่ปัญหา** (หรือให้ AI ช่วยเลือกให้อัตโนมัติ)
3. พิมพ์ **สถานที่เกิดเหตุ** และ **รายละเอียดเหตุการณ์** ให้ชัดเจน
4. เมื่อพิมพ์รายละเอียด ระบบ **AI Smart Assistant** จะประมวลผลคำอธิบาย และเลือกหมวดหมู่พร้อมประเมินระดับความเร่งด่วนให้ทันที
5. (ไม่บังคับ) แนบไฟล์รูปภาพ หรือเอกสารหลักฐาน
6. กดปุ่ม **"ส่งรายงานอย่างปลอดภัย (Encrypted Submit)"**
7. **⚠️ สำคัญมาก:** ระบบจะแสดง **รหัสรายงาน (Report ID)** และ **รหัส PIN ลับ** ให้ทำการบันทึกหรือคัดลอกเก็บไว้ทันที (รหัส PIN จะไม่ถูกจัดเก็บแบบ Plaintext)

#### ขั้นตอนที่ 2: ติดตามสถานะและแชทกับเจ้าหน้าที่ (Track Status & Chat)
1. เลือกแท็บ **"ติดตามสถานะ"**
2. กรอก **รหัสรายงาน (Report ID)** และ **รหัส PIN**
3. กดปุ่ม **"ตรวจสอบข้อมูลรายงาน"**
4. ระบบจะแสดงสถานะปัจจุบัน (เช่น รับเรื่องแล้ว, กำลังตรวจสอบ) พร้อมประวัติไทม์ไลน์
5. ผู้แจ้งสามารถพิมพ์ข้อความส่งหาเจ้าหน้าที่ หรือส่งหลักฐานเพิ่มเติมผ่านกล่องแชทลับได้ทันที

---

### 🛡️ 2. สำหรับเจ้าหน้าที่และผู้ดูแลระบบ (Admin / Staff)

#### ข้อมูลบัญชีผู้ใช้สำหรับทดสอบ (Default Test Accounts):
| บทบาท (Role) | Username | Password | สิทธิ์การเข้าถึง |
|---|---|---|---|
| **Admin (ผู้ดูแลระบบ/หัวหน้างาน)** | `admin` | `admin123` | แก้ไขข้อมูลทุกส่วน, จัดการทุกคดี, ปรับระดับความเร่งด่วน, ดูสถิติ, จัดการ Audit Logs, ลบรายงาน |
| **Officer (เจ้าหน้าที่สอบสวน)** | `officer1` | `officer123` | ตรวจสอบคดี, แชทตอบกลับผู้แจ้ง, อัปเดตสถานะคดี |

#### ขั้นตอนการทำงานของ Admin / เจ้าหน้าที่:
1. กดปุ่ม **"เจ้าหน้าที่เข้าสู่ระบบ"** ที่แถบเมนูด้านบนขวา
2. กรอก Username (`admin`) และ Password (`admin123`)
3. เมื่อเข้าสู่ระบบแล้ว สามารถใช้งานส่วนต่างๆ ได้ดังนี้:
   - **เปลี่ยนสถานะ/ความเร่งด่วนด่วน:** สามารถคลิกดรอปดาวน์ที่คอลัมน์ในตารางเพื่อเปลี่ยนสถานะหรือความเร่งด่วนได้ทันที
   - **แก้ไขข้อมูลสำนวนคดี:** กดปุ่ม **"✏️ แก้ไข"** ในตาราง หรือกดจากหน้าต่างรายละเอียดเคส เพื่อปรับแก้ข้อมูลทุกฟิลด์ (หมวดหมู่, ความเร่งด่วน, สถานะ, ผู้รับผิดชอบ, วันที่/สถานที่, รหัส PIN, รายละเอียด และบันทึกช่วยจำภายใน)
   - **แชทกับผู้แจ้ง:** กดปุ่ม **"สนทนาลับ"** เพื่อแชทโต้ตอบกับผู้แจ้งแบบ Real-time
   - **สถิติ & สรุปผล (Analytics):** ดูภาพรวมและแนวโน้มเรื่องร้องเรียนเพื่อวางแผนป้องกัน
   - **ส่งออกข้อมูล (Export):** กดปุ่ม Export ด้านบนขวาเพื่อดาวน์โหลดรายงานเป็น CSV หรือ JSON

---

## 🛠️ วิธีการติดตั้งและรันระบบ (Installation & How to Run)

### 🚀 วิธีที่ 1: รันในสภาพแวดล้อม Node.js Full-Stack (แนะนำ - รองรับทุกฟังก์ชัน + AI + WebSockets)

#### ความต้องการของระบบ (Prerequisites)
- **Node.js**: เวอร์ชัน 18.0.0 ขึ้นไป (ตรวจสอบด้วยคำสั่ง `node -v`)
- **npm**: เวอร์ชัน 9.0.0 ขึ้นไป (หรือใช้ `pnpm` / `bun` / `yarn`)

#### ขั้นตอนการติดตั้งและรัน:

```bash
# 1. โคลนโปรเจกต์ (หากนำไปรันที่เครื่องตัวเอง)
git clone <URL_REPO>
cd npru-sentinel

# 2. ติดตั้ง Dependencies ทั้งหมด
npm install

# 3. ตั้งค่าไฟล์ Environment Variables
# ทำการคัดลอกไฟล์ตัวอย่าง .env.example ไปเป็น .env
cp .env.example .env
```

#### การตั้งค่าคีย์ในไฟล์ `.env`:
เปิดไฟล์ `.env` และกรอกค่าตามต้องการ:
```env
# พอร์ตที่ใช้รัน (ค่าเริ่มต้นคือ 3000)
PORT=3000

# API Key สำหรับระบบ AI วิเคราะห์รายงานอัตโนมัติ (รับฟรีจาก https://aistudio.google.com)
GEMINI_API_KEY=your_gemini_api_key_here

# URL สำหรับระบบ
APP_URL=http://localhost:3000
```
> 💡 *หมายเหตุ:* หากยังไม่มี `GEMINI_API_KEY` ระบบจะมี **Local Rule-based AI Engine** ทำงานสำรองให้อัตโนมัติทันที

#### รันระบบในโหมดพัฒนา (Development Mode):
```bash
npm run dev
```
- ระบบจะเปิดเซิร์ฟเวอร์ Express + Vite พร้อมระบบ Real-time WebSockets บนพอร์ต **3000**
- เปิดเว็บเบราว์เซอร์แล้วเข้าใช้งานได้ทันทีที่: **`http://localhost:3000`**

#### บิลด์และรันในโหมด Production:
```bash
# 1. ทำการ Build ทั้งฝั่ง Frontend (Vite) และ Backend (esbuild)
npm run build

# 2. เริ่มต้นรัน Production Server
npm start
```

---

### 🐳 วิธีที่ 2: รันด้วย Docker & Docker Compose (สะดวก รวดเร็ว และเป็นระเบียบ)

ระบบมีไฟล์ `Dockerfile` และ `docker-compose.yml` สำหรับการ Deploy พร้อมใช้งาน:

#### คำสั่งรันผ่าน Docker Compose:
```bash
# 1. ตั้งค่าไฟล์ .env ก่อนรัน (ถ้ายังไม่มี)
cp .env.example .env

# 2. สั่ง Build และเริ่มต้น Container ในโหมด Background
docker compose up -d --build

# 3. ตรวจสอบสถานะการทำงานและ Logs
docker compose ps
docker compose logs -f

# 4. หยุดการทำงาน
docker compose down
```
- เข้าใช้งานได้ทันทีที่: **`http://localhost:3000`**

---

### 🐍 วิธีที่ 3: รันด้วย Python Backend (Flask + SQLite)

หากต้องการนำไปใช้งานร่วมกับ Server ภาษา Python มีไฟล์ `app.py` และ `schema.sql` ให้พร้อมใช้งาน:

```bash
# 1. สร้าง Virtual Environment
python -m venv venv

# 2. เปิดใช้งาน Virtual Environment
# บน Linux / macOS:
source venv/bin/activate
# บน Windows (Command Prompt / PowerShell):
venv\Scripts\activate

# 3. ติดตั้ง Dependencies ที่จำเป็น
pip install flask flask-cors

# 4. เริ่มต้นรัน Python Flask Server
python app.py
```
- เซิร์ฟเวอร์ Python จะทำงานที่: **`http://localhost:5000`**

---

### 🔑 บัญชีผู้ใช้สำหรับทดสอบระบบ (Default Login Credentials)

เมื่อเปิดหน้าเว็บแล้ว สามารถกดปุ่ม **"เจ้าหน้าที่เข้าสู่ระบบ"** ที่มุมขวาบนเพื่อทดสอบสิทธิ์:

| ระดับสิทธิ์ (Role) | Username | Password | ความสามารถในระบบ |
|---|---|---|---|
| **ผู้ดูแลระบบ (Admin)** | `admin` | `admin123` | **แก้ไขข้อมูลได้ทุกส่วน**, ปรับความเร่งด่วน/สถานะ, ลบรายงาน, ดูสถิติ, ตรวจสอบ Audit Log, แชทลับ |
| **เจ้าหน้าที่สอบสวน (Officer)** | `officer1` | `officer123` | ตรวจสอบข้อเท็จจริง, แชทตอบกลับผู้แจ้ง, ปรับสถานะการดำเนินการ |

---

## 🔐 สถาปัตยกรรมความปลอดภัย (Security Architecture)

1. **Zero-Knowledge PIN Verification:** รหัส PIN ถูก Hash ด้วยอัลกอริทึม SHA-256 ก่อนบันทึกลงฐานข้อมูล
2. **Strict Role-Based Access Control (RBAC):** แยกระดับสิทธิ์ระหว่างผู้แจ้งทั่วไป (Guest), เจ้าหน้าที่สอบสวน (Officer) และผู้ดูแลระบบ (Admin)
3. **Full Admin Governance:** ผู้ดูแลระบบมีสิทธิ์ทบทวน ตรวจสอบ แก้ไขข้อมูล และบันทึกข้อค้นพบภายใน (Internal Memo) พร้อมระบบ Audit Trail บันทึกเวลาและชื่อผู้แก้ไข
4. **Server-Side AI Proxy:** ซ่อน `GEMINI_API_KEY` ไว้ที่ฝั่ง Server-side (`server.ts`) ไม่เปิดเผยไปยัง Browser ของผู้ใช้งาน

---

## 📂 โครงสร้างไดเรกทอรี (Project Directory Structure)

```text
├── README.md               # คู่มือการใช้งานและเอกสารประกอบระบบ
├── server.ts               # Express Backend Server + Gemini AI API Proxy + WebSockets
├── app.py                  # Python Flask Alternative Backend
├── schema.sql              # โครงสร้างฐานข้อมูล SQLite
├── package.json            # รายการ Dependencies และ Scripts
├── .env.example            # ตัวอย่างการกำหนดค่า Environment Variables
├── public/                 # Static Assets และโลโก้ NPRU
│   └── npru_logo.png       # โลโก้ทางการของมหาวิทยาลัยราชภัฏนครปฐม
└── src/
    ├── App.tsx             # Main Component และระบบจัดการแท็บ/สิทธิ์
    ├── types.ts            # TypeScript Interface และ Data Types
    ├── index.css           # Tailwind CSS Styling
    ├── components/
    │   ├── Navbar.tsx              # เมนูนำทางด้านบน
    │   ├── SubmitReport.tsx        # แบบฟอร์มแจ้งเบาะแสนิรนาม + AI Assistant
    │   ├── TrackStatus.tsx         # หน้าติดตามสถานะและแชทลับ 2 ทาง
    │   ├── CaseManager.tsx         # ระบบจัดการและแก้ไขคดีสำหรับ Admin & Staff
    │   ├── AnalyticsDashboard.tsx  # กราฟและสถิติภาพรวม
    │   ├── LoginModal.tsx          # หน้าต่างเข้าสู่ระบบเจ้าหน้าที่
    │   └── PythonFlaskCodeView.tsx # ตัวอย่างโค้ดและวิธีรัน Python
    ├── db/
    │   └── sqlite.ts               # SQLite & Storage Engine พร้อมระบบ Audit Trail
    ├── services/
    │   └── realtime.ts             # ระบบซิงค์ข้อมูล Real-time (WebSocket / Broadcast)
    └── lib/
        └── aiAnalyzer.ts           # AI Helper & Fallback Engine
```

---

## 🧪 การทดสอบระบบอัตโนมัติด้วย Selenium Python (Automated E2E Testing)

ระบบ TrustLine ได้รับการพัฒนาชุดทดสอบอัตโนมัติแบบ **End-to-End (E2E)** ด้วย **Python 3**, **Selenium WebDriver** (Chrome Headless) และ **pytest** โดยครอบคลุมทั้ง 7 โมดูล รวม **68 Test Cases (TC-001 ถึง TC-068)** ตามเอกสารข้อกำหนดในโฟลเดอร์ `docs/`:
- `docs/FUNCTIONAL_REQUIREMENTS.md` (ข้อกำหนดความต้องการเชิงหน้าที่ FRS)
- `docs/Annonymous-Test-Cases.docx` (กรณีทดสอบ E2E ทั้งหมด 68 กรณี)
- `docs/Annonymous-Test-Plan-and-Report.docx` (แผนการทดสอบและผู้รับผิดชอบ)

---

### 📦 1. สิ่งที่ต้องติดตั้งล่วงหน้า (Prerequisites & Installation)

#### ขั้นตอนที่ 1.1: ติดตั้ง Python และ Pip
- ต้องใช้ **Python 3.10+ หรือ 3.11+**
- ตรวจสอบเวอร์ชัน: `python3 --version`

#### ขั้นตอนที่ 1.2: ติดตั้ง Chromium และ ChromeDriver
- **บน Ubuntu / Debian / Linux:**
  ```bash
  sudo apt-get update
  sudo apt-get install -y python3-pip chromium chromium-driver
  ```
- **บน macOS (Homebrew):**
  ```bash
  brew install python chromium chromedriver
  ```
- **บน Windows:**
  - ติดตั้ง Google Chrome และดาวน์โหลด ChromeDriver เวอร์ชันตรงกันจาก [Chrome for Testing](https://googlechromelabs.github.io/chrome-for-testing/)
  - นำไฟล์ `chromedriver.exe` ไปวางไว้ใน System PATH

#### ขั้นตอนที่ 1.3: ติดตั้ง Python Dependencies
```bash
# ติดตั้ง Packages ที่จำเป็นจาก tests/requirements.txt
pip install -r tests/requirements.txt

# หรือหากใช้ pip3 บน Linux:
pip3 install -r tests/requirements.txt
```
*(รายการ Packages ที่ติดตั้ง: `selenium>=4.20.0`, `pytest>=8.0.0`, `requests>=2.31.0`, `websockets>=12.0`)*

---

### 🔌 2. การเตรียมเซิร์ฟเวอร์ก่อนเริ่มทดสอบ (Server Pre-requisite)

ก่อนสั่งรันการทดสอบ ต้องเปิดเซิร์ฟเวอร์ระบบให้ทำงานอยู่ก่อน (พอร์ต 3000):
```bash
# ใน Terminal แรก: สั่งเริ่มรันแอปพลิเคชัน
npm run dev
```
*(ตรวจสอบว่าเข้าใช้งานที่ `http://localhost:3000` ได้ตามปกติ)*

> 💡 *หมายเหตุสำหรับการทดสอบบนเว็บจริง (Live Website / Production):*
> หากต้องการทดสอบกับเว็บไซต์จริง (เช่น `https://anonymous-report.ai.studio/`) สามารถทำได้ 2 วิธี:
> 1. ใส่ Flag `--url https://anonymous-report.ai.studio/` ต่อท้ายคำสั่ง `run_tests.py`
> 2. หรือตั้งค่า Environment Variable `TEST_BASE_URL` ก่อนรัน `pytest`:
>    - **บน Windows CMD:** `set TEST_BASE_URL=https://anonymous-report.ai.studio/`
>    - **บน Windows PowerShell:** `$env:TEST_BASE_URL="https://anonymous-report.ai.studio/"`
>    - **บน Linux / macOS:** `export TEST_BASE_URL="https://anonymous-report.ai.studio/"`

---

### 👥 3. โครงสร้างโฟลเดอร์แยกตามผู้ทดสอบ (Test Folders by Person)

ชุดทดสอบแบ่งออกเป็น 4 โฟลเดอร์ตามผู้รับผิดชอบการทดสอบทั้ง 4 ท่าน:

| ผู้ทดสอบ | โฟลเดอร์ | โมดูลที่รับผิดชอบ | ขอบเขต Test Cases | จำนวนกรณี | ผลการทดสอบจริง |
|---|---|---|---|:---:|:---:|
| **วัชรากร (watcharakorn)** | `tests/watcharakorn/` | **Module 1:** การส่งรายงานเบาะแสลับ (FR-SUB)<br>**Module 2:** ระบบวิเคราะห์อัจฉริยะด้วย AI (FR-AI) | TC-001 ถึง TC-030 | **30 Cases** | ✅ **30/30 ผ่าน 100%** |
| **วุฒิชัย (suttichai)** | `tests/suttichai/` | **Module 3:** ติดตามสถานะและแชทลับ 2 ทาง (FR-TRK)<br>**Module 4:** ระบบจัดการสำนวนคดีสำหรับเจ้าหน้าที่ (FR-CAS) | TC-031 ถึง TC-053 | **23 Cases** | ✅ **23/23 ผ่าน 100%** |
| **สหรัฐ (saharat)** | `tests/saharat/` | **Module 5:** แดชบอร์ดสถิติและการวิเคราะห์ (FR-ANA)<br>**Module 6:** การยืนยันตัวตนและความปลอดภัย (FR-SEC) | TC-054 ถึง TC-063 | **10 Cases** | ✅ **10/10 ผ่าน 100%** |
| **อธิป (athip)** | `tests/athip/` | **Module 7:** โครงสร้างพื้นฐาน, WebSocket & SQLite (FR-SYS) | TC-064 ถึง TC-068 | **5 Cases** | ✅ **5/5 ผ่าน 100%** |
| **รวมทั้งสิ้น** | `tests/` | **ครบทั้ง 7 โมดูลตามเอกสาร FRS** | **TC-001 ถึง TC-068** | **68 Cases** | ✅ **68/68 ผ่าน 100%** |

---

### 🚀 4. คำสั่งการรันการทดสอบ (Execution Commands)

> 🌐 **เว็บจริงที่ใช้ทดสอบ (Live Web Target):**  
> ระบบถูกตั้งค่าเริ่มต้นให้ยิงทดสอบไปยัง **`https://anonymous-report.ai.studio/`** โดยตรงทันที ไม่จำเป็นต้องรัน `npm run dev` ในเครื่อง  
> 
> 🚗 **ระบบจัดการ ChromeDriver อัตโนมัติ:**  
> มี `webdriver-manager` ตรวจจับเวอร์ชัน Google Chrome ในเครื่องของคุณและจัดเตรียมไดรเวอร์ให้โดยอัตโนมัติ ไม่ต้องโหลดไฟล์หรือตั้ง PATH เอง  
> 
> 💡 **สำหรับผู้ใช้งาน Windows:**  
> หากพิมพ์ `pytest` แล้วพบข้อความว่า `'pytest' is not recognized` หรือ `[WinError 2]`  
> ให้ติดตั้ง dependencies ก่อนด้วย:  
> `python -m pip install -r tests/requirements.txt`  
> และสั่งรันด้วย **`python tests/run_tests.py`** หรือ **`python -m pytest`**

#### 4.1 สั่งรันผ่านตัวจัดการกลาง `run_tests.py` (แนะนำ - แสดงตารางสรุปผลสวยงาม)

- **บน Windows (Command Prompt หรือ PowerShell):**
  ```cmd
  # 🟢 รันการทดสอบทั้งหมด (68 Cases) ยิงไปยัง https://anonymous-report.ai.studio/
  python tests/run_tests.py --tester all

  # 🔵 รันเฉพาะของ "วัชรากร" (30 Cases)
  python tests/run_tests.py --tester watcharakorn

  # 🔵 รันเฉพาะของ "วุฒิชัย" (23 Cases)
  python tests/run_tests.py --tester suttichai

  # 🔵 รันเฉพาะของ "สหรัฐ" (10 Cases)
  python tests/run_tests.py --tester saharat

  # 🔵 รันเฉพาะของ "อธิป" (5 Cases)
  python tests/run_tests.py --tester athip

  # 🖥️ โหมดเปิดหน้าต่าง Chrome ให้เห็นการทำงานสด (Headed Mode)
  python tests/run_tests.py --tester watcharakorn --headed
  ```

- **บน Linux / macOS:**
  ```bash
  python3 tests/run_tests.py --tester all
  python3 tests/run_tests.py --tester watcharakorn
  python3 tests/run_tests.py --tester suttichai
  python3 tests/run_tests.py --tester saharat
  python3 tests/run_tests.py --tester athip
  ```

#### 4.2 สั่งรันผ่าน `pytest` โดยตรง

- **บน Windows (ใช้ `python -m pytest`):**
  ```cmd
  # 🟢 รันการทดสอบทั้งหมด:
  python -m pytest tests/ -v

  # 🔵 รันแยกเฉพาะของแต่ละคน:
  python -m pytest tests/watcharakorn/ -v    # วัชรากร (30 Cases)
  python -m pytest tests/suttichai/ -v      # วุฒิชัย (23 Cases)
  python -m pytest tests/saharat/ -v        # สหรัฐ (10 Cases)
  python -m pytest tests/athip/ -v          # อธิป (5 Cases)

  # 🟡 รันเฉพาะไฟล์ย่อย:
  python -m pytest tests/watcharakorn/test_sub_module.py -v         # Module 1 (Submission)
  python -m pytest tests/watcharakorn/test_ai_module.py -v          # Module 2 (AI Analysis)
  python -m pytest tests/suttichai/test_tracking_chat.py -v         # Module 3 (Tracking & Chat)
  python -m pytest tests/suttichai/test_case_management.py -v       # Module 4 (Case Manager)
  python -m pytest tests/saharat/test_analytics_dashboard.py -v     # Module 5 (Analytics)
  python -m pytest tests/saharat/test_auth_security.py -v           # Module 6 (Auth & Security)
  python -m pytest tests/athip/test_infrastructure.py -v            # Module 7 (Infrastructure)
  ```

- **บน Linux / macOS (ใช้ `pytest` หรือ `python3 -m pytest`):**
  ```bash
  pytest tests/watcharakorn/ -v
  pytest tests/suttichai/ -v
  pytest tests/saharat/ -v
  pytest tests/athip/ -v
  ```

---

## 📑 เอกสารข้อกำหนดและการทดสอบ (Documentation & Testing)
- **[ข้อกำหนดความต้องการเชิงหน้าที่สำหรับทำ Test Cases (Functional Requirements Specification)](docs/FUNCTIONAL_REQUIREMENTS.md)**: ระบุ Requirement IDs (เช่น `FR-SUB-001`, `FR-AI-001`, `FR-CAS-001`), Inputs, Expected Results และ Acceptance Criteria ครบทุกโมดูล สำหรับทีม QA นำไปเขียน Test Scenarios
- **[ไฟล์กรณีทดสอบทั้งหมด 68 กรณี (Annonymous-Test-Cases.docx)](docs/Annonymous-Test-Cases.docx)**: รายละเอียด Pre-conditions, Steps, Test Data, Expected Results
- **[แผนการทดสอบและรายงานผล (Annonymous-Test-Plan-and-Report.docx)](docs/Annonymous-Test-Plan-and-Report.docx)**: การแบ่งบทบาทผู้ทดสอบ, รอบการทดสอบ และเกณฑ์การประเมิน

---

## ⚖️ ลิขสิทธิ์และการใช้งาน (License & Disclaimer)
พัฒนาขึ้นสำหรับ **มหาวิทยาลัยราชภัฏนครปฐม (Nakhon Pathom Rajabhat University - NPRU)** เพื่อเป็นระบบแจ้งเบาะแสและร้องเรียนที่โปร่งใส ตรวจสอบได้ และรักษาความลับของผู้ร้องเรียนตามมาตรฐานจริยธรรมและ พ.ร.บ. คุ้มครองข้อมูลส่วนบุคคล (PDPA)

-- =========================================================
-- TrustLine Whistleblower Systems - PostgreSQL Database Schema
-- สคริปต์สร้างตารางฐานข้อมูล PostgreSQL สำหรับระบบแจ้งเบาะแส
-- =========================================================

-- 1. ตารางรายงานเบาะแส (reports)
CREATE TABLE IF NOT EXISTS reports (
    id VARCHAR(50) PRIMARY KEY,
    pin_hash VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    urgency VARCHAR(20) NOT NULL,
    incident_date VARCHAR(50) NOT NULL,
    location TEXT NOT NULL,
    description TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'received',
    assigned_to VARCHAR(100) DEFAULT 'รอเจ้าหน้าที่รับเรื่อง',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. ตารางไฟล์หลักฐานแนบ (evidence)
CREATE TABLE IF NOT EXISTS evidence (
    id SERIAL PRIMARY KEY,
    report_id VARCHAR(50) NOT NULL REFERENCES reports(id) ON DELETE CASCADE,
    file_name VARCHAR(255) NOT NULL,
    file_path TEXT NOT NULL,
    file_type VARCHAR(100) NOT NULL,
    file_size BIGINT NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. ตารางข้อความแชทลับ (messages)
CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    report_id VARCHAR(50) NOT NULL REFERENCES reports(id) ON DELETE CASCADE,
    sender_role VARCHAR(50) NOT NULL,
    sender_name VARCHAR(100) NOT NULL,
    message_text TEXT NOT NULL,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. ตารางบันทึกประวัติการใช้งาน (audit_logs)
CREATE TABLE IF NOT EXISTS audit_logs (
    id SERIAL PRIMARY KEY,
    user_name VARCHAR(100) NOT NULL,
    action_text TEXT NOT NULL,
    ip_address VARCHAR(50) DEFAULT '127.0.0.1',
    status VARCHAR(20) DEFAULT 'Success',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. ตารางผู้ดูแลระบบ / เจ้าหน้าที่สอบสวน (users)
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(150) NOT NULL,
    role VARCHAR(50) DEFAULT 'investigator',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ข้อมูลตัวอย่างเริ่มต้นสำหรับการทดสอบ (Initial Seed Data)
INSERT INTO reports (id, pin_hash, category, urgency, incident_date, location, description, status, assigned_to)
VALUES 
('TL-8942-XCVB', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'fraud', 'high', '2024-10-10', 'สำนักงานใหญ่ ชั้น 14', 'พบความผิดปกติในการอนุมัติงบประมาณการจัดซื้อซอฟต์แวร์ของแผนก IT', 'investigating', 'เจ้าหน้าที่สืบสวน สมชาย'),
('TL-1092-AABB', '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', 'harassment', 'high', '2024-10-16', 'อาคารเฉลิมพระเกียรติ ชั้น 4', 'มีพฤติกรรมการใช้วาจาคุกคามและข่มขู่ทางวาจาจากบุคคลในภาควิชา', 'investigating', 'นิติกร ประวิทย์ (ฝ่ายวินัย)'),
('TL-2024-089A', 'ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb', 'fraud', 'critical', '2024-10-24', 'อาคารเรียนรวม 2', 'ตรวจพบใบเสร็จรับเงินเท็จสำหรับการจัดซื้ออุปกรณ์ห้องปฏิบัติการคอมพิวเตอร์', 'investigating', 'เจ้าหน้าที่ HR นารี')
ON CONFLICT (id) DO NOTHING;

INSERT INTO audit_logs (user_name, action_text, ip_address, status)
VALUES
('Admin_HR_01', 'Status updated to In-Progress (Case #TL-8942-XCVB)', '192.168.1.105', 'Success'),
('System_Automated', 'Escalation triggered for Critical Case #TL-2024-089A', '10.0.0.1', 'Success'),
('Investigator_04', 'Failed login attempt (3rd try with invalid credentials)', '203.114.10.44', 'Failure');

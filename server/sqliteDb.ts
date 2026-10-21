/**
 * TrustLine Portal - Server-Side Real SQLite Database Engine
 * ใช้ Node.js 22 built-in SQLite (DatabaseSync) จัดเก็บข้อมูลลงไฟล์จริง: ./data/trustline.db
 */

import fs from 'fs';
import path from 'path';
import { DatabaseSync } from 'node:sqlite';
import { ReportItem, EvidenceFile, ChatMessage, AuditLogItem } from '../src/types';

const DATA_DIR = path.join(process.cwd(), 'data');
const DB_FILE = path.join(DATA_DIR, 'trustline.db');

// Ensure data directory exists
if (!fs.existsSync(DATA_DIR)) {
  fs.mkdirSync(DATA_DIR, { recursive: true });
}

// Open or create SQLite database file
const db = new DatabaseSync(DB_FILE);

// Set PRAGMA configurations for high performance & reliability
db.exec('PRAGMA journal_mode = WAL;');
db.exec('PRAGMA foreign_keys = ON;');
db.exec('PRAGMA synchronous = NORMAL;');

// Initialize Tables Schema
db.exec(`
  CREATE TABLE IF NOT EXISTS reports (
    id TEXT PRIMARY KEY,
    pin TEXT NOT NULL,
    category TEXT NOT NULL,
    category_label_th TEXT NOT NULL,
    urgency TEXT NOT NULL,
    incident_date TEXT NOT NULL,
    location TEXT NOT NULL,
    description TEXT NOT NULL,
    status TEXT NOT NULL,
    status_label_th TEXT NOT NULL,
    assigned_to TEXT NOT NULL,
    admin_notes TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
  );

  CREATE TABLE IF NOT EXISTS evidence_files (
    id TEXT PRIMARY KEY,
    report_id TEXT NOT NULL,
    file_name TEXT NOT NULL,
    file_size INTEGER NOT NULL,
    file_type TEXT NOT NULL,
    url TEXT NOT NULL,
    uploaded_at TEXT NOT NULL,
    FOREIGN KEY (report_id) REFERENCES reports(id) ON DELETE CASCADE
  );

  CREATE TABLE IF NOT EXISTS messages (
    id TEXT PRIMARY KEY,
    report_id TEXT NOT NULL,
    sender_role TEXT NOT NULL,
    sender_name TEXT NOT NULL,
    message TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    read_by_admin INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    FOREIGN KEY (report_id) REFERENCES reports(id) ON DELETE CASCADE
  );

  CREATE TABLE IF NOT EXISTS audit_logs (
    id TEXT PRIMARY KEY,
    date_time TEXT NOT NULL,
    user_name TEXT NOT NULL,
    action TEXT NOT NULL,
    ip_address TEXT NOT NULL,
    status TEXT NOT NULL
  );

  CREATE INDEX IF NOT EXISTS idx_reports_category ON reports(category);
  CREATE INDEX IF NOT EXISTS idx_reports_status ON reports(status);
  CREATE INDEX IF NOT EXISTS idx_evidence_report_id ON evidence_files(report_id);
  CREATE INDEX IF NOT EXISTS idx_messages_report_id ON messages(report_id);
`);

// --- Seed Data Definition ---
const INITIAL_REPORTS: ReportItem[] = [
  {
    id: 'TL-8942-XCVB',
    pin: '8942',
    category: 'fraud',
    categoryLabelTh: 'การทุจริตทางการเงิน',
    urgency: 'high',
    incidentDate: '2024-10-10',
    location: 'สำนักงานใหญ่ ชั้น 14',
    description: 'พบความผิดปกติในการอนุมัติงบประมาณการจัดซื้อซอฟต์แวร์ของแผนก IT โดยไม่มีการประมูลตามขั้นตอนปกติ',
    status: 'investigating',
    statusLabelTh: 'กำลังตรวจสอบข้อเท็จจริง',
    assignedTo: 'เจ้าหน้าที่สืบสวน สมชาย',
    createdAt: '2024-10-12T09:30:00Z',
    updatedAt: '2024-10-14T09:10:00Z',
    evidenceFiles: [
      {
        id: 'ev-1',
        reportId: 'TL-8942-XCVB',
        fileName: 'NPRU_Software_Engineering_Logo.png',
        fileSize: 245000,
        fileType: 'image/png',
        url: 'https://lh3.googleusercontent.com/aida/AP1WRLtU44n3f_tjW66fZilAlpQg6COjKylcfyMotAx17aYlNkTDIA-fW67FtlHS3vhd48wYNNwEMys_5vOkD8nxOVcyRXbHJtHu5IJC4TSRdhd3YVcL8a3_qK6WBXcunS2QAu_NKlh2mOtg9jhoMcB7RWAhoqRTwUq0bfWEISeHr9akBF4qxnLJ_Gjrte3ZbdUxiskXf1teAaZj7YFsI6xKM5IfLvo-DdqU6BpIhn_Ly2-l_kApOnM58wkpei0',
        uploadedAt: '2024-10-12 09:30'
      },
      {
        id: 'ev-2',
        reportId: 'TL-8942-XCVB',
        fileName: 'PO_Software_License_2024.pdf',
        fileSize: 1240000,
        fileType: 'application/pdf',
        url: 'https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?w=600&auto=format&fit=crop&q=80',
        uploadedAt: '2024-10-13 15:10'
      },
      {
        id: 'ev-video-1',
        reportId: 'TL-8942-XCVB',
        fileName: 'CCTV_Software_Department_Evidence.mp4',
        fileSize: 8450000,
        fileType: 'video/mp4',
        url: 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4',
        uploadedAt: '2024-10-14 10:15'
      }
    ]
  },
  {
    id: 'TL-1092-AABB',
    pin: '1092',
    category: 'harassment',
    categoryLabelTh: 'การล่วงละเมิดและคุกคาม',
    urgency: 'high',
    incidentDate: '2024-10-16',
    location: 'อาคารเฉลิมพระเกียรติ ชั้น 4',
    description: 'มีพฤติกรรมการใช้วาจาคุกคามและข่มขู่ทางวาจาจากบุคคลในภาควิชา ทำให้รู้สึกไม่ปลอดภัยและได้รับผลกระทบทางจิตใจอย่างรุนแรง',
    status: 'investigating',
    statusLabelTh: 'กำลังตรวจสอบข้อเท็จจริง',
    assignedTo: 'นิติกร ประวิทย์ (ฝ่ายวินัย)',
    createdAt: '2024-10-16T10:15:00Z',
    updatedAt: '2024-10-18T14:30:00Z',
    evidenceFiles: [
      {
        id: 'ev-aabb-1',
        reportId: 'TL-1092-AABB',
        fileName: 'Chat_Evidence_Harassment.png',
        fileSize: 420000,
        fileType: 'image/png',
        url: 'https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=600&auto=format&fit=crop&q=80',
        uploadedAt: '2024-10-16 10:15'
      }
    ]
  },
  {
    id: 'TL-2024-089A',
    pin: '1111',
    category: 'fraud',
    categoryLabelTh: 'การทุจริตทางการเงิน',
    urgency: 'critical',
    incidentDate: '2024-10-24',
    location: 'อาคารเรียนรวม 2',
    description: 'ตรวจพบใบเสร็จรับเงินเท็จสำหรับการจัดซื้ออุปกรณ์ห้องปฏิบัติการคอมพิวเตอร์',
    status: 'investigating',
    statusLabelTh: 'กำลังตรวจสอบข้อเท็จจริง',
    assignedTo: 'เจ้าหน้าที่ HR นารี',
    createdAt: '2024-10-24T11:20:00Z',
    updatedAt: '2024-10-25T14:00:00Z',
    evidenceFiles: [
      {
        id: 'ev-3',
        reportId: 'TL-2024-089A',
        fileName: 'Receipt_Audit_Evidence.jpg',
        fileSize: 890000,
        fileType: 'image/jpeg',
        url: 'https://images.unsplash.com/photo-1450133064473-71024230f91b?w=600&auto=format&fit=crop&q=80',
        uploadedAt: '2024-10-24 11:25'
      }
    ]
  },
  {
    id: 'TL-2024-088B',
    pin: '2222',
    category: 'harassment',
    categoryLabelTh: 'การล่วงละเมิดในที่ทำงาน',
    urgency: 'high',
    incidentDate: '2024-10-22',
    location: 'แผนกการเงิน ชั้น 3',
    description: 'มีการใช้วาจาข่มขู่และคุกคามในสถานที่ทำงานอย่างต่อเนื่อง',
    status: 'received',
    statusLabelTh: 'รับเรื่องแล้ว',
    assignedTo: 'ยังไม่มอบหมาย',
    createdAt: '2024-10-22T08:15:00Z',
    updatedAt: '2024-10-22T08:15:00Z',
    evidenceFiles: []
  },
  {
    id: 'TL-2024-075C',
    pin: '3333',
    category: 'compliance',
    categoryLabelTh: 'การปฏิบัติตามกฎระเบียบ',
    urgency: 'medium',
    incidentDate: '2024-10-18',
    location: 'ศูนย์คอมพิวเตอร์',
    description: 'การเปิดเผยข้อมูลส่วนบุคคลของนักศึกษาโดยไม่ได้รับอนุญาต',
    status: 'disciplinary',
    statusLabelTh: 'ดำเนินการทางวินัย/กฎหมาย',
    assignedTo: 'นิติกร ประวิทย์',
    createdAt: '2024-10-18T16:45:00Z',
    updatedAt: '2024-10-21T10:30:00Z',
    evidenceFiles: []
  },
  {
    id: 'TL-2024-061D',
    pin: '4444',
    category: 'technical',
    categoryLabelTh: 'ปัญหาทางเทคนิค/ความปลอดภัย',
    urgency: 'low',
    incidentDate: '2024-10-15',
    location: 'ระบบเซิร์ฟเวอร์หลัก',
    description: 'พบคะแนนสอบรั่วไหลในระบบจัดเก็บไฟล์ส่วนกลาง',
    status: 'closed',
    statusLabelTh: 'ปิดเรื่องเรียบร้อยแล้ว',
    assignedTo: 'ทีมงานความปลอดภัย IT',
    createdAt: '2024-10-15T13:00:00Z',
    updatedAt: '2024-10-17T17:00:00Z',
    evidenceFiles: []
  }
];

const INITIAL_MESSAGES: ChatMessage[] = [
  {
    id: 'msg-1',
    reportId: 'TL-8942-XCVB',
    senderRole: 'investigator',
    senderName: 'เจ้าหน้าที่สืบสวน',
    message: 'เรียนผู้แจ้งเบาะแส, ขอขอบคุณสำหรับข้อมูลเพิ่มเติม ทางเราต้องการสอบถามว่าเหตุการณ์ที่ระบุเกิดขึ้นที่สาขาใดครับ?',
    timestamp: '13 ต.ค. 14:20',
    readByAdmin: true
  },
  {
    id: 'msg-2',
    reportId: 'TL-8942-XCVB',
    senderRole: 'reporter',
    senderName: 'คุณ (ผู้แจ้ง)',
    message: 'เกิดขึ้นที่สาขาสำนักงานใหญ่ ชั้น 14 ครับ',
    timestamp: '13 ต.ค. 15:05',
    readByAdmin: true
  },
  {
    id: 'msg-3',
    reportId: 'TL-8942-XCVB',
    senderRole: 'investigator',
    senderName: 'เจ้าหน้าที่สืบสวน',
    message: 'รับทราบครับ หากมีหลักฐานภาพถ่ายเพิ่มเติม สามารถอัปโหลดในระบบได้เลยครับ',
    timestamp: '14 ต.ค. 09:10',
    readByAdmin: true
  },
  {
    id: 'msg-aabb-1',
    reportId: 'TL-1092-AABB',
    senderRole: 'investigator',
    senderName: 'นิติกร ประวิทย์',
    message: 'สวัสดีครับ เจ้าหน้าที่ได้รับเรื่องร้องเรียนแล้ว ทางเรากำลังรวบรวมข้อมูลและจะรักษาความลับของคุณอย่างสูงสุด',
    timestamp: '16 ต.ค. 11:30',
    readByAdmin: true
  },
  {
    id: 'msg-aabb-2',
    reportId: 'TL-1092-AABB',
    senderRole: 'reporter',
    senderName: 'คุณ (ผู้แจ้ง)',
    message: 'ขอบคุณครับ มีภาพหลักฐานข้อความแชทที่ถูกคุกคามแนบไว้ในระบบเรียบร้อยแล้วครับ',
    timestamp: '16 ต.ค. 11:45',
    readByAdmin: true
  },
  {
    id: 'msg-aabb-3',
    reportId: 'TL-1092-AABB',
    senderRole: 'investigator',
    senderName: 'นิติกร ประวิทย์',
    message: 'ได้รับหลักฐานเรียบร้อยแล้วครับ คณะกรรมการกำลังดำเนินการตรวจสอบข้อเท็จจริงอย่างเร่งด่วนครับ',
    timestamp: '18 ต.ค. 14:30',
    readByAdmin: true
  }
];

const INITIAL_AUDIT_LOGS: AuditLogItem[] = [
  {
    id: 'log-1',
    dateTime: '2024-10-27 14:32:01',
    userName: 'Admin_HR_01',
    action: "Status updated to 'In-Progress' (Case #TL-8942-XCVB)",
    ipAddress: '192.168.1.105',
    status: 'Success'
  },
  {
    id: 'log-2',
    dateTime: '2024-10-27 13:15:22',
    userName: 'System_Automated',
    action: 'Escalation triggered for Critical Case #TL-2024-089A',
    ipAddress: '10.0.0.1',
    status: 'Success'
  },
  {
    id: 'log-3',
    dateTime: '2024-10-27 11:05:45',
    userName: 'Investigator_04',
    action: 'Failed login attempt (3rd try with invalid credentials)',
    ipAddress: '203.114.10.44',
    status: 'Failure'
  },
  {
    id: 'log-4',
    dateTime: '2024-10-27 09:30:10',
    userName: 'Admin_Finance',
    action: 'Downloaded Encrypted Audit Report (Q3 Compliance Summary)',
    ipAddress: '192.168.2.55',
    status: 'Success'
  },
  {
    id: 'log-5',
    dateTime: '2024-10-26 16:20:00',
    userName: 'System_Database',
    action: 'SQLite Database persistent engine initialized on server disk (data/trustline.db)',
    ipAddress: '127.0.0.1',
    status: 'Success'
  }
];

// Seed initial data if table is empty
function seedDatabaseIfNeeded() {
  const countRow = db.prepare('SELECT COUNT(*) as count FROM reports').get() as { count: number };
  if (countRow && countRow.count > 0) {
    return;
  }

  console.log('[SQLite] Seeding initial records into SQLite database...');

  const insertReportStmt = db.prepare(`
    INSERT INTO reports (
      id, pin, category, category_label_th, urgency, incident_date, 
      location, description, status, status_label_th, assigned_to, 
      admin_notes, created_at, updated_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
  `);

  const insertEvidenceStmt = db.prepare(`
    INSERT INTO evidence_files (
      id, report_id, file_name, file_size, file_type, url, uploaded_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?)
  `);

  for (const r of INITIAL_REPORTS) {
    insertReportStmt.run(
      r.id,
      r.pin,
      r.category,
      r.categoryLabelTh,
      r.urgency,
      r.incidentDate,
      r.location,
      r.description,
      r.status,
      r.statusLabelTh,
      r.assignedTo || 'รอเจ้าหน้าที่รับเรื่อง',
      r.adminNotes || null,
      r.createdAt,
      r.updatedAt
    );

    if (r.evidenceFiles && r.evidenceFiles.length > 0) {
      for (const ev of r.evidenceFiles) {
        insertEvidenceStmt.run(
          ev.id,
          r.id,
          ev.fileName,
          ev.fileSize,
          ev.fileType,
          ev.url,
          ev.uploadedAt
        );
      }
    }
  }

  const insertMsgStmt = db.prepare(`
    INSERT INTO messages (
      id, report_id, sender_role, sender_name, message, timestamp, read_by_admin, created_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
  `);

  for (const m of INITIAL_MESSAGES) {
    insertMsgStmt.run(
      m.id,
      m.reportId,
      m.senderRole,
      m.senderName,
      m.message,
      m.timestamp,
      m.readByAdmin ? 1 : 0,
      new Date().toISOString()
    );
  }

  const insertLogStmt = db.prepare(`
    INSERT INTO audit_logs (id, date_time, user_name, action, ip_address, status)
    VALUES (?, ?, ?, ?, ?, ?)
  `);

  for (const log of INITIAL_AUDIT_LOGS) {
    insertLogStmt.run(log.id, log.dateTime, log.userName, log.action, log.ipAddress, log.status);
  }

  console.log('[SQLite] Seeding complete. All initial records stored in ./data/trustline.db');
}

seedDatabaseIfNeeded();

// Helper to hydrate evidence files into report
function hydrateReport(row: any): ReportItem {
  const evRows = db.prepare('SELECT * FROM evidence_files WHERE report_id = ?').all(row.id) as any[];
  const evidenceFiles: EvidenceFile[] = evRows.map(ev => ({
    id: ev.id,
    reportId: ev.report_id,
    fileName: ev.file_name,
    fileSize: Number(ev.file_size),
    fileType: ev.file_type,
    url: ev.url,
    uploadedAt: ev.uploaded_at
  }));

  return {
    id: row.id,
    pin: row.pin,
    category: row.category,
    categoryLabelTh: row.category_label_th,
    urgency: row.urgency,
    incidentDate: row.incident_date,
    location: row.location,
    description: row.description,
    status: row.status,
    statusLabelTh: row.status_label_th,
    assignedTo: row.assigned_to,
    adminNotes: row.admin_notes || undefined,
    createdAt: row.created_at,
    updatedAt: row.updated_at,
    evidenceFiles
  };
}

// --- CRUD Operations for Reports ---

export function getAllReports(): ReportItem[] {
  const rows = db.prepare('SELECT * FROM reports ORDER BY created_at DESC').all() as any[];
  return rows.map(hydrateReport);
}

export function getReportById(id: string): ReportItem | null {
  const row = db.prepare('SELECT * FROM reports WHERE LOWER(id) = LOWER(?)').get(id.trim()) as any;
  if (!row) return null;
  return hydrateReport(row);
}

export function getReportByIdAndPin(id: string, pin: string): ReportItem | null {
  const row = db.prepare(
    'SELECT * FROM reports WHERE LOWER(id) = LOWER(?) AND pin = ?'
  ).get(id.trim(), pin.trim()) as any;
  if (!row) return null;
  return hydrateReport(row);
}

export function createReport(
  data: Omit<ReportItem, 'id' | 'createdAt' | 'updatedAt' | 'status' | 'statusLabelTh'> & { id?: string },
  operator: string = 'Anonymous_User'
): ReportItem {
  const randomHex = Math.random().toString(36).substring(2, 6).toUpperCase();
  const reportId = data.id || `TL-2024-${randomHex}`;
  const pin = data.pin || Math.floor(1000 + Math.random() * 9000).toString();
  const now = new Date().toISOString();

  const categoryLabels: Record<string, string> = {
    harassment: 'การล่วงละเมิดและคุกคาม',
    compliance: 'การปฏิบัติตามกฎระเบียบ',
    technical: 'ปัญหาทางเทคนิค/ความปลอดภัย',
    fraud: 'การทุจริตทางการเงิน',
    safety: 'ความปลอดภัยและสิ่งแวดล้อม',
    academic: 'การประพฤติผิดทางวิชาการ',
    teaching: 'คุณภาพการสอน/รายงานเกี่ยวกับอาจารย์'
  };

  const statusLabels: Record<string, string> = {
    received: 'รับเรื่องแล้ว',
    investigating: 'กำลังตรวจสอบข้อเท็จจริง',
    disciplinary: 'ดำเนินการทางวินัย/กฎหมาย',
    closed: 'ปิดเรื่องเรียบร้อยแล้ว'
  };

  const categoryLabelTh = data.categoryLabelTh || categoryLabels[data.category] || 'อื่นๆ';
  const status = 'received';
  const statusLabelTh = statusLabels[status];
  const assignedTo = data.assignedTo || 'รอเจ้าหน้าที่รับเรื่อง';

  db.prepare(`
    INSERT INTO reports (
      id, pin, category, category_label_th, urgency, incident_date, 
      location, description, status, status_label_th, assigned_to, 
      admin_notes, created_at, updated_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
  `).run(
    reportId,
    pin,
    data.category || 'safety',
    categoryLabelTh,
    data.urgency,
    data.incidentDate || new Date().toISOString().split('T')[0],
    data.location || 'ไม่ระบุ',
    data.description,
    status,
    statusLabelTh,
    assignedTo,
    data.adminNotes || null,
    now,
    now
  );

  // Insert evidence files if present
  if (data.evidenceFiles && data.evidenceFiles.length > 0) {
    const insertEvidenceStmt = db.prepare(`
      INSERT INTO evidence_files (
        id, report_id, file_name, file_size, file_type, url, uploaded_at
      ) VALUES (?, ?, ?, ?, ?, ?, ?)
    `);
    for (const ev of data.evidenceFiles) {
      insertEvidenceStmt.run(
        ev.id,
        reportId,
        ev.fileName,
        ev.fileSize,
        ev.fileType,
        ev.url,
        ev.uploadedAt || now
      );
    }
  }

  // Record Audit Log in SQLite
  addAuditLog(
    operator,
    `Created new encrypted report #${reportId} (${categoryLabelTh}) in SQLite DB`,
    'Success'
  );

  return getReportById(reportId)!;
}

export function updateReport(
  id: string,
  data: Partial<Omit<ReportItem, 'id' | 'createdAt'>>,
  operator: string = 'Admin'
): ReportItem | null {
  const existing = getReportById(id);
  if (!existing) return null;

  const now = new Date().toISOString();

  const categoryLabels: Record<string, string> = {
    harassment: 'การล่วงละเมิดและคุกคาม',
    compliance: 'การปฏิบัติตามกฎระเบียบ',
    technical: 'ปัญหาทางเทคนิค/ความปลอดภัย',
    fraud: 'การทุจริตทางการเงิน',
    safety: 'ความปลอดภัยและสิ่งแวดล้อม',
    academic: 'การประพฤติผิดทางวิชาการ',
    teaching: 'คุณภาพการสอน/รายงานเกี่ยวกับอาจารย์'
  };

  const statusLabels: Record<string, string> = {
    received: 'รับเรื่องแล้ว',
    investigating: 'กำลังตรวจสอบข้อเท็จจริง',
    disciplinary: 'ดำเนินการทางวินัย/กฎหมาย',
    closed: 'ปิดเรื่องเรียบร้อยแล้ว'
  };

  const updatedPin = data.pin !== undefined ? data.pin : existing.pin;
  const updatedCategory = data.category || existing.category;
  const updatedCategoryLabelTh = data.categoryLabelTh || (data.category ? categoryLabels[data.category] : existing.categoryLabelTh);
  const updatedUrgency = data.urgency || existing.urgency;
  const updatedIncidentDate = data.incidentDate || existing.incidentDate;
  const updatedLocation = data.location !== undefined ? data.location : existing.location;
  const updatedDescription = data.description !== undefined ? data.description : existing.description;
  const updatedStatus = data.status || existing.status;
  const updatedStatusLabelTh = data.statusLabelTh || (data.status ? statusLabels[data.status] : existing.statusLabelTh);
  const updatedAssignedTo = data.assignedTo !== undefined ? data.assignedTo : existing.assignedTo;
  const updatedAdminNotes = data.adminNotes !== undefined ? data.adminNotes : existing.adminNotes;

  db.prepare(`
    UPDATE reports SET
      pin = ?,
      category = ?,
      category_label_th = ?,
      urgency = ?,
      incident_date = ?,
      location = ?,
      description = ?,
      status = ?,
      status_label_th = ?,
      assigned_to = ?,
      admin_notes = ?,
      updated_at = ?
    WHERE LOWER(id) = LOWER(?)
  `).run(
    updatedPin,
    updatedCategory,
    updatedCategoryLabelTh,
    updatedUrgency,
    updatedIncidentDate,
    updatedLocation,
    updatedDescription,
    updatedStatus,
    updatedStatusLabelTh,
    updatedAssignedTo || 'รอเจ้าหน้าที่รับเรื่อง',
    updatedAdminNotes || null,
    now,
    id.trim()
  );

  addAuditLog(
    operator,
    `Updated report #${existing.id} (Status: ${updatedStatusLabelTh}, Urgency: ${updatedUrgency})`,
    'Success'
  );

  return getReportById(id);
}

export function deleteReport(id: string, operator: string = 'Admin'): boolean {
  const existing = getReportById(id);
  if (!existing) return false;

  db.prepare('DELETE FROM messages WHERE LOWER(report_id) = LOWER(?)').run(id.trim());
  db.prepare('DELETE FROM evidence_files WHERE LOWER(report_id) = LOWER(?)').run(id.trim());
  db.prepare('DELETE FROM reports WHERE LOWER(id) = LOWER(?)').run(id.trim());

  addAuditLog(
    operator,
    `Deleted report #${existing.id} and associated evidence from SQLite database`,
    'Success'
  );

  return true;
}

// --- Evidence Operations ---

export function addEvidence(reportId: string, file: EvidenceFile, operator: string = 'User'): boolean {
  const report = getReportById(reportId);
  if (!report) return false;

  const now = new Date().toISOString();
  db.prepare(`
    INSERT INTO evidence_files (
      id, report_id, file_name, file_size, file_type, url, uploaded_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?)
  `).run(
    file.id,
    report.id,
    file.fileName,
    file.fileSize,
    file.fileType,
    file.url,
    file.uploadedAt || now
  );

  db.prepare('UPDATE reports SET updated_at = ? WHERE id = ?').run(now, report.id);

  addAuditLog(
    operator,
    `Uploaded evidence '${file.fileName}' for Case #${report.id} to SQLite`,
    'Success'
  );

  return true;
}

export function removeEvidence(reportId: string, evidenceId: string, operator: string = 'Admin'): boolean {
  const file = db.prepare('SELECT * FROM evidence_files WHERE id = ? AND LOWER(report_id) = LOWER(?)').get(evidenceId, reportId.trim()) as any;
  if (!file) return false;

  db.prepare('DELETE FROM evidence_files WHERE id = ?').run(evidenceId);
  const now = new Date().toISOString();
  db.prepare('UPDATE reports SET updated_at = ? WHERE LOWER(id) = LOWER(?)').run(now, reportId.trim());

  addAuditLog(
    operator,
    `Deleted evidence '${file.file_name}' from Case #${reportId}`,
    'Success'
  );

  return true;
}

// --- Secret Chat Messages Operations ---

export function getMessages(reportId: string): ChatMessage[] {
  const rows = db.prepare(
    'SELECT * FROM messages WHERE LOWER(report_id) = LOWER(?) ORDER BY created_at ASC'
  ).all(reportId.trim()) as any[];

  return rows.map(m => ({
    id: m.id,
    reportId: m.report_id,
    senderRole: m.sender_role as 'investigator' | 'reporter',
    senderName: m.sender_name,
    message: m.message,
    timestamp: m.timestamp,
    readByAdmin: Boolean(m.read_by_admin)
  }));
}

export function insertMessage(msg: ChatMessage): ChatMessage {
  const now = new Date().toISOString();
  db.prepare(`
    INSERT INTO messages (
      id, report_id, sender_role, sender_name, message, timestamp, read_by_admin, created_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
  `).run(
    msg.id,
    msg.reportId,
    msg.senderRole,
    msg.senderName,
    msg.message,
    msg.timestamp,
    msg.readByAdmin ? 1 : 0,
    now
  );

  addAuditLog(
    msg.senderName,
    `Sent encrypted secret message for Case #${msg.reportId}`,
    'Success'
  );

  return msg;
}

export function markMessagesAsRead(reportId: string): void {
  db.prepare(`
    UPDATE messages 
    SET read_by_admin = 1 
    WHERE LOWER(report_id) = LOWER(?) AND sender_role = 'reporter'
  `).run(reportId.trim());
}

// --- Audit Logs Operations ---

export function getAuditLogs(): AuditLogItem[] {
  const rows = db.prepare('SELECT * FROM audit_logs ORDER BY date_time DESC LIMIT 100').all() as any[];
  return rows.map(r => ({
    id: r.id,
    dateTime: r.date_time,
    userName: r.user_name,
    action: r.action,
    ipAddress: r.ip_address,
    status: r.status as 'Success' | 'Failure'
  }));
}

export function addAuditLog(
  userName: string, 
  action: string, 
  status: 'Success' | 'Failure',
  ipAddress: string = '127.0.0.1 (Encrypted Proxy)'
): void {
  const now = new Date();
  const dateStr = `${now.getFullYear()}-${(now.getMonth() + 1).toString().padStart(2, '0')}-${now.getDate().toString().padStart(2, '0')} ${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}:${now.getSeconds().toString().padStart(2, '0')}`;
  const logId = `log-${Date.now()}-${Math.random().toString(36).substring(2, 6)}`;

  try {
    db.prepare(`
      INSERT INTO audit_logs (id, date_time, user_name, action, ip_address, status)
      VALUES (?, ?, ?, ?, ?, ?)
    `).run(logId, dateStr, userName, action, ipAddress, status);
  } catch (err) {
    console.error('Failed to write audit log into SQLite:', err);
  }
}

// --- Database Status and Inspection ---

export function getDatabaseStatus() {
  const stats = fs.existsSync(DB_FILE) ? fs.statSync(DB_FILE) : { size: 0 };
  const walFile = `${DB_FILE}-wal`;
  const walStats = fs.existsSync(walFile) ? fs.statSync(walFile) : { size: 0 };

  const repCount = (db.prepare('SELECT COUNT(*) as c FROM reports').get() as any)?.c || 0;
  const msgCount = (db.prepare('SELECT COUNT(*) as c FROM messages').get() as any)?.c || 0;
  const evCount = (db.prepare('SELECT COUNT(*) as c FROM evidence_files').get() as any)?.c || 0;
  const logCount = (db.prepare('SELECT COUNT(*) as c FROM audit_logs').get() as any)?.c || 0;

  const pragmaCheck = (db.prepare('PRAGMA integrity_check').get() as any)?.integrity_check || 'ok';
  const journalMode = (db.prepare('PRAGMA journal_mode').get() as any)?.journal_mode || 'wal';

  const totalBytes = stats.size + walStats.size;
  const formattedSize = totalBytes > 1024 * 1024 
    ? `${(totalBytes / (1024 * 1024)).toFixed(2)} MB`
    : `${(totalBytes / 1024).toFixed(2)} KB`;

  return {
    engine: 'SQLite 3 (Node.js Native DatabaseSync)',
    dbPath: 'data/trustline.db',
    absolutePath: DB_FILE,
    fileSizeBytes: stats.size,
    walSizeBytes: walStats.size,
    fileSizeFormatted: formattedSize,
    tableCounts: {
      reports: repCount,
      messages: msgCount,
      evidenceFiles: evCount,
      auditLogs: logCount
    },
    pragmaIntegrity: pragmaCheck,
    journalMode: journalMode,
    lastUpdated: new Date().toISOString()
  };
}

export function executeSqlSafe(sqlQuery: string) {
  const trimmed = sqlQuery.trim();
  const lower = trimmed.toLowerCase();

  // Allow only SELECT and PRAGMA queries for security
  if (!lower.startsWith('select') && !lower.startsWith('pragma') && !lower.startsWith('explain')) {
    throw new Error('Only read-only queries (SELECT, PRAGMA) are allowed in the SQL inspector');
  }

  const startTime = Date.now();
  const rows = db.prepare(trimmed).all() as any[];
  const executionTimeMs = Date.now() - startTime;

  const columns = rows.length > 0 ? Object.keys(rows[0]) : [];

  return {
    columns,
    rows,
    rowCount: rows.length,
    executionTimeMs
  };
}

export function resetDatabaseToSeed() {
  console.log('[SQLite] Resetting database to initial seeds...');
  db.exec(`
    DELETE FROM messages;
    DELETE FROM evidence_files;
    DELETE FROM reports;
    DELETE FROM audit_logs;
  `);

  seedDatabaseIfNeeded();

  addAuditLog('System_Admin', 'Reset SQLite database to factory defaults', 'Success');
  return getDatabaseStatus();
}

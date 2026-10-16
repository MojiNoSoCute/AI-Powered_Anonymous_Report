/**
 * TrustLine Portal - Real SQLite Database Client Engine
 * ซิงค์ข้อมูลกับฐานข้อมูล SQLite จริงบนเซิร์ฟเวอร์ (data/trustline.db)
 * รองรับ Full CRUD (Create, Read, Update, Delete) ผ่าน REST API และ WebSocket
 */

import { 
  ReportItem, 
  ChatMessage, 
  AuditLogItem, 
  CategoryType, 
  UrgencyLevel, 
  ReportStatus, 
  EvidenceFile,
  DatabaseStatusInfo,
  SqlQueryResult
} from '../types';

// Key for LocalStorage persistence of optimistic state
const STORAGE_KEY = 'trustline_sqlite_db_cache_v2';

// Initial Fallback Mock Seed Data in case network is offline
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

const INITIAL_MESSAGES: Record<string, ChatMessage[]> = {
  'TL-8942-XCVB': [
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
    }
  ],
  'TL-1092-AABB': [
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
  ]
};

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
    action: 'SQLite Database persistent engine connected (data/trustline.db)',
    ipAddress: '127.0.0.1',
    status: 'Success'
  }
];

class SQLiteDatabase {
  private reports: ReportItem[] = [];
  private messages: Record<string, ChatMessage[]> = {};
  private auditLogs: AuditLogItem[] = [];
  private isServerSynced: boolean = false;

  constructor() {
    // 1. Load optimistic cache from localStorage
    if (typeof window !== 'undefined') {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved) {
        try {
          const parsed = JSON.parse(saved);
          this.reports = Array.isArray(parsed.reports) ? parsed.reports : INITIAL_REPORTS;
          this.messages = parsed.messages || INITIAL_MESSAGES;
          this.auditLogs = Array.isArray(parsed.auditLogs) ? parsed.auditLogs : INITIAL_AUDIT_LOGS;
        } catch {
          this.reports = INITIAL_REPORTS;
          this.messages = INITIAL_MESSAGES;
          this.auditLogs = INITIAL_AUDIT_LOGS;
        }
      } else {
        this.reports = INITIAL_REPORTS;
        this.messages = INITIAL_MESSAGES;
        this.auditLogs = INITIAL_AUDIT_LOGS;
      }
    } else {
      this.reports = INITIAL_REPORTS;
      this.messages = INITIAL_MESSAGES;
      this.auditLogs = INITIAL_AUDIT_LOGS;
    }

    // 2. Fetch fresh real data from SQLite backend
    if (typeof window !== 'undefined') {
      this.fetchFromServer();
    }
  }

  public async fetchFromServer(): Promise<void> {
    try {
      const [resReports, resLogs] = await Promise.all([
        fetch('/api/reports').then(r => r.ok ? r.json() : null),
        fetch('/api/audit-logs').then(r => r.ok ? r.json() : null)
      ]);

      if (Array.isArray(resReports) && resReports.length > 0) {
        this.reports = resReports;
      }
      if (Array.isArray(resLogs) && resLogs.length > 0) {
        this.auditLogs = resLogs;
      }

      this.isServerSynced = true;
      this.persist();
    } catch (err) {
      console.warn('[SQLite Client] Background sync error, using cached state:', err);
    }
  }

  private persist() {
    if (typeof window === 'undefined') return;
    try {
      localStorage.setItem(
        STORAGE_KEY,
        JSON.stringify({
          reports: this.reports,
          messages: this.messages,
          auditLogs: this.auditLogs
        })
      );
    } catch {}
  }

  // --- Reports CRUD Operations ---

  public getReports(): ReportItem[] {
    return this.reports.map(r => ({ ...r, evidenceFiles: [...(r.evidenceFiles || [])] }));
  }

  public getReportById(id: string): ReportItem | undefined {
    const found = this.reports.find(r => r.id.toLowerCase() === id.trim().toLowerCase());
    return found ? { ...found, evidenceFiles: [...(found.evidenceFiles || [])] } : undefined;
  }

  public getReportByIdAndPin(id: string, pin: string): ReportItem | undefined {
    const found = this.reports.find(
      r => r.id.toLowerCase() === id.trim().toLowerCase() && r.pin === pin.trim()
    );
    return found ? { ...found, evidenceFiles: [...(found.evidenceFiles || [])] } : undefined;
  }

  public createReport(
    data: Omit<ReportItem, 'id' | 'createdAt' | 'updatedAt' | 'status' | 'statusLabelTh'>,
    operator: string = 'Anonymous_User'
  ): ReportItem {
    const randomHex = Math.random().toString(36).substring(2, 6).toUpperCase();
    const newId = `TL-2024-${randomHex}`;
    const now = new Date().toISOString();

    const categoryLabels: Record<CategoryType, string> = {
      harassment: 'การล่วงละเมิดและคุกคาม',
      compliance: 'การปฏิบัติตามกฎระเบียบ',
      technical: 'ปัญหาทางเทคนิค/ความปลอดภัย',
      fraud: 'การทุจริตทางการเงิน',
      safety: 'ความปลอดภัยและสิ่งแวดล้อม',
      academic: 'การประพฤติผิดทางวิชาการ',
      teaching: 'คุณภาพการสอน/รายงานเกี่ยวกับอาจารย์'
    };

    const newReport: ReportItem = {
      ...data,
      id: newId,
      categoryLabelTh: categoryLabels[data.category] || 'อื่นๆ',
      status: 'received',
      statusLabelTh: 'รับเรื่องแล้ว',
      assignedTo: 'รอเจ้าหน้าที่รับเรื่อง',
      createdAt: now,
      updatedAt: now,
      evidenceFiles: data.evidenceFiles || []
    };

    // 1. Optimistic local update
    this.reports.unshift(newReport);
    this.addAuditLog(
      operator,
      `Created new encrypted report #${newId} (${newReport.categoryLabelTh}) in SQLite DB`,
      'Success'
    );
    this.persist();

    // 2. Real SQLite backend POST
    if (typeof window !== 'undefined') {
      fetch('/api/reports', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'x-user-name': operator 
        },
        body: JSON.stringify(newReport)
      })
      .then(r => r.json())
      .then(res => {
        if (res.report) {
          this.syncReportFromServer(res.report);
        }
      })
      .catch(err => console.error('[SQLite Client] POST /api/reports failed:', err));
    }

    return newReport;
  }

  public updateReportStatus(reportId: string, newStatus: ReportStatus, userName: string = 'Admin'): boolean {
    const report = this.reports.find(r => r.id.toLowerCase() === reportId.trim().toLowerCase());
    if (!report) return false;

    const statusLabels: Record<ReportStatus, string> = {
      received: 'รับเรื่องแล้ว',
      investigating: 'กำลังตรวจสอบข้อเท็จจริง',
      disciplinary: 'ดำเนินการทางวินัย/กฎหมาย',
      closed: 'ปิดเรื่องเรียบร้อยแล้ว'
    };

    report.status = newStatus;
    report.statusLabelTh = statusLabels[newStatus];
    report.updatedAt = new Date().toISOString();

    this.addAuditLog(
      userName,
      `Updated Case #${reportId} status to '${statusLabels[newStatus]}'`,
      'Success'
    );
    this.persist();

    // Sync to Real SQLite backend
    if (typeof window !== 'undefined') {
      fetch(`/api/reports/${report.id}`, {
        method: 'PUT',
        headers: { 
          'Content-Type': 'application/json',
          'x-user-name': userName 
        },
        body: JSON.stringify(report)
      }).catch(err => console.error('[SQLite Client] PUT /api/reports failed:', err));
    }

    return true;
  }

  public updateReport(
    reportId: string, 
    data: Partial<Omit<ReportItem, 'id' | 'createdAt'>>, 
    userName: string = 'Admin'
  ): boolean {
    const report = this.reports.find(r => r.id.toLowerCase() === reportId.trim().toLowerCase());
    if (!report) return false;

    const categoryLabels: Record<CategoryType, string> = {
      fraud: 'การทุจริตทางการเงิน',
      harassment: 'การล่วงละเมิดในที่ทำงาน',
      teaching: 'รายงานเกี่ยวกับอาจารย์/การสอน',
      compliance: 'การปฏิบัติตามกฎระเบียบ',
      technical: 'ปัญหาทางเทคนิค/ความปลอดภัย',
      safety: 'ความปลอดภัย/สิ่งแวดล้อม',
      academic: 'การประพฤติผิดทางวิชาการ'
    };

    const statusLabels: Record<ReportStatus, string> = {
      received: 'รับเรื่องแล้ว',
      investigating: 'กำลังตรวจสอบข้อเท็จจริง',
      disciplinary: 'ดำเนินการทางวินัย/กฎหมาย',
      closed: 'ปิดเรื่องเรียบร้อยแล้ว'
    };

    if (data.category) {
      report.category = data.category;
      report.categoryLabelTh = categoryLabels[data.category] || report.categoryLabelTh;
    }
    if (data.status) {
      report.status = data.status;
      report.statusLabelTh = statusLabels[data.status] || report.statusLabelTh;
    }
    if (data.urgency) report.urgency = data.urgency;
    if (data.incidentDate) report.incidentDate = data.incidentDate;
    if (data.location) report.location = data.location;
    if (data.description) report.description = data.description;
    if (data.assignedTo !== undefined) report.assignedTo = data.assignedTo;
    if (data.pin) report.pin = data.pin;
    if (data.adminNotes !== undefined) report.adminNotes = data.adminNotes;
    
    report.updatedAt = new Date().toISOString();

    this.addAuditLog(userName, `Edited details for Case #${reportId}`, 'Success');
    this.persist();

    // Sync to Real SQLite backend
    if (typeof window !== 'undefined') {
      fetch(`/api/reports/${report.id}`, {
        method: 'PUT',
        headers: { 
          'Content-Type': 'application/json',
          'x-user-name': userName 
        },
        body: JSON.stringify(report)
      }).catch(err => console.error('[SQLite Client] PUT /api/reports failed:', err));
    }

    return true;
  }

  public deleteReport(reportId: string, userName: string = 'Admin'): boolean {
    const idx = this.reports.findIndex(r => r.id.toLowerCase() === reportId.toLowerCase());
    if (idx === -1) return false;

    this.reports.splice(idx, 1);
    delete this.messages[reportId];

    this.addAuditLog(userName, `Withdrew/Deleted Report #${reportId}`, 'Success');
    this.persist();

    // Sync to Real SQLite backend
    if (typeof window !== 'undefined') {
      fetch(`/api/reports/${reportId}`, {
        method: 'DELETE',
        headers: { 'x-user-name': userName }
      }).catch(err => console.error('[SQLite Client] DELETE /api/reports failed:', err));
    }

    return true;
  }

  public syncReportFromServer(serverReport: ReportItem): void {
    const idx = this.reports.findIndex(r => r.id.toLowerCase() === serverReport.id.toLowerCase());
    if (idx !== -1) {
      this.reports[idx] = { ...serverReport };
    } else {
      this.reports.unshift({ ...serverReport });
    }
    this.persist();
  }

  public removeReportFromServer(reportId: string): void {
    const idx = this.reports.findIndex(r => r.id.toLowerCase() === reportId.toLowerCase());
    if (idx !== -1) {
      this.reports.splice(idx, 1);
      delete this.messages[reportId];
      this.persist();
    }
  }

  // --- Evidence Files Operations ---

  public addEvidence(reportId: string, file: EvidenceFile, userName: string = 'User'): boolean {
    const report = this.reports.find(r => r.id.toLowerCase() === reportId.trim().toLowerCase());
    if (!report) return false;

    report.evidenceFiles.push(file);
    report.updatedAt = new Date().toISOString();

    this.addAuditLog(userName, `Uploaded evidence '${file.fileName}' for Case #${reportId}`, 'Success');
    this.persist();

    if (typeof window !== 'undefined') {
      fetch(`/api/reports/${reportId}/evidence`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'x-user-name': userName 
        },
        body: JSON.stringify(file)
      }).catch(err => console.error('[SQLite Client] POST evidence failed:', err));
    }

    return true;
  }

  public removeEvidence(reportId: string, evidenceId: string, userName: string = 'Admin'): boolean {
    const report = this.reports.find(r => r.id.toLowerCase() === reportId.trim().toLowerCase());
    if (!report) return false;

    const fileIdx = report.evidenceFiles.findIndex(f => f.id === evidenceId);
    if (fileIdx === -1) return false;

    const fileName = report.evidenceFiles[fileIdx].fileName;
    report.evidenceFiles.splice(fileIdx, 1);
    report.updatedAt = new Date().toISOString();

    this.addAuditLog(userName, `Deleted evidence '${fileName}' from Case #${reportId}`, 'Success');
    this.persist();

    if (typeof window !== 'undefined') {
      fetch(`/api/reports/${reportId}/evidence/${evidenceId}`, {
        method: 'DELETE',
        headers: { 'x-user-name': userName }
      }).catch(err => console.error('[SQLite Client] DELETE evidence failed:', err));
    }

    return true;
  }

  // --- Secret Chat Messages Operations ---

  public getMessages(reportId: string): ChatMessage[] {
    // If not cached, trigger fetch
    if (!this.messages[reportId] && typeof window !== 'undefined') {
      fetch(`/api/reports/${reportId}/messages`)
        .then(r => r.ok ? r.json() : [])
        .then(list => {
          if (Array.isArray(list)) {
            this.messages[reportId] = list;
            this.persist();
          }
        })
        .catch(() => {});
    }
    return this.messages[reportId] ? [...this.messages[reportId]] : [];
  }

  public getUnreadMessagesCount(reportId: string): number {
    const list = this.messages[reportId];
    if (!list || list.length === 0) return 0;
    return list.filter(m => m.senderRole === 'reporter' && m.readByAdmin !== true).length;
  }

  public getTotalUnreadCountForAdmin(): number {
    let total = 0;
    for (const key in this.messages) {
      total += this.getUnreadMessagesCount(key);
    }
    return total;
  }

  public markMessagesAsReadByAdmin(reportId: string): boolean {
    const list = this.messages[reportId];
    if (!list || list.length === 0) return false;

    let modified = false;
    for (const msg of list) {
      if (msg.senderRole === 'reporter' && msg.readByAdmin !== true) {
        msg.readByAdmin = true;
        modified = true;
      }
    }

    if (modified) {
      this.persist();
      if (typeof window !== 'undefined') {
        fetch(`/api/reports/${reportId}/mark-read`, { method: 'POST' }).catch(() => {});
      }
    }
    return modified;
  }

  public sendMessage(reportId: string, senderRole: 'investigator' | 'reporter', senderName: string, text: string): ChatMessage {
    if (!this.messages[reportId]) {
      this.messages[reportId] = [];
    }

    const now = new Date();
    const timeStr = `${now.getDate()} ต.ค. ${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`;

    const newMsg: ChatMessage = {
      id: `msg-${Date.now()}-${Math.random().toString(36).substring(2, 6)}`,
      reportId,
      senderRole,
      senderName,
      message: text,
      timestamp: timeStr,
      readByAdmin: senderRole === 'investigator'
    };

    this.messages[reportId].push(newMsg);
    this.addAuditLog(
      senderName,
      `Sent encrypted message in secret channel for Case #${reportId}`,
      'Success'
    );
    this.persist();

    // Real SQLite backend POST
    if (typeof window !== 'undefined') {
      fetch(`/api/reports/${reportId}/messages`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ senderRole, senderName, message: text })
      }).catch(err => console.error('[SQLite Client] POST message failed:', err));
    }

    return newMsg;
  }

  // --- Audit Logs Operations ---

  public getAuditLogs(): AuditLogItem[] {
    return [...this.auditLogs];
  }

  public addAuditLog(userName: string, action: string, status: 'Success' | 'Failure'): void {
    const now = new Date();
    const dateStr = `${now.getFullYear()}-${(now.getMonth() + 1).toString().padStart(2, '0')}-${now.getDate().toString().padStart(2, '0')} ${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}:${now.getSeconds().toString().padStart(2, '0')}`;

    const newLog: AuditLogItem = {
      id: `log-${Date.now()}`,
      dateTime: dateStr,
      userName,
      action,
      ipAddress: '127.0.0.1 (Encrypted Proxy)',
      status
    };

    this.auditLogs.unshift(newLog);
    this.persist();

    if (typeof window !== 'undefined') {
      fetch('/api/audit-logs', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newLog)
      }).catch(() => {});
    }
  }

  // --- Real SQLite Database Server Inspections ---

  public async getDatabaseStatus(): Promise<DatabaseStatusInfo | null> {
    try {
      const res = await fetch('/api/db/status');
      if (!res.ok) throw new Error('Failed to query SQLite server status');
      return await res.json();
    } catch (err) {
      console.error('[SQLite Client] getDatabaseStatus error:', err);
      return null;
    }
  }

  public async executeSqlQuery(query: string): Promise<SqlQueryResult> {
    const res = await fetch('/api/db/query', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query })
    });
    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData.error || 'SQL query failed');
    }
    return await res.json();
  }

  public async resetToDefaultSeed(): Promise<void> {
    try {
      const res = await fetch('/api/db/reset', { method: 'POST' });
      if (res.ok) {
        await this.fetchFromServer();
      }
    } catch {
      this.reports = INITIAL_REPORTS;
      this.messages = INITIAL_MESSAGES;
      this.auditLogs = INITIAL_AUDIT_LOGS;
      this.persist();
    }
  }
}

export const db = new SQLiteDatabase();

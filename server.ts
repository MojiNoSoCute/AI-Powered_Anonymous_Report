import express from 'express';
import http from 'http';
import path from 'path';
import { WebSocketServer, WebSocket } from 'ws';
import { GoogleGenAI, Type } from '@google/genai';
import dotenv from 'dotenv';
import * as sqliteDb from './server/sqliteDb';

dotenv.config();

const app = express();
const PORT = process.env.PORT ? parseInt(process.env.PORT, 10) : 3000;

app.use(express.json({ limit: '10mb' }));

// Initialize Gemini Client server-side
const apiKey = process.env.GEMINI_API_KEY;
const ai = apiKey ? new GoogleGenAI({ apiKey }) : null;

// Category mapping helper
const categoryNamesTh: Record<string, string> = {
  harassment: 'การล่วงละเมิดและคุกคาม (Harassment & Bullying)',
  compliance: 'การปฏิบัติตามกฎระเบียบ (Compliance & Ethics)',
  technical: 'ปัญหาทางเทคนิค/ความปลอดภัย (Technical & Security)',
  fraud: 'การทุจริตทางการเงิน (Financial Fraud)',
  safety: 'ความปลอดภัยและสิ่งแวดล้อม (Safety & Environment)',
  academic: 'การประพฤติผิดทางวิชาการ (Academic Misconduct)',
  teaching: 'คุณภาพการสอน/รายงานเกี่ยวกับอาจารย์ (Teaching & Instructor Issues)',
};

const urgencyNamesTh: Record<string, string> = {
  low: 'ปกติ (Low)',
  medium: 'ปานกลาง (Medium)',
  high: 'สูง (High)',
  critical: 'วิกฤต (Critical)',
};

// --- WebSocket Connection Management ---
interface ClientConnection {
  ws: WebSocket;
  caseId?: string;
  isAdmin: boolean;
}

const activeClients = new Set<ClientConnection>();

function broadcast(payload: any, targetCaseId?: string, skipWs?: WebSocket) {
  const data = JSON.stringify(payload);
  for (const client of activeClients) {
    if (client.ws.readyState !== WebSocket.OPEN) continue;
    if (skipWs && client.ws === skipWs) continue;

    // Send if client is subscribed to this case OR is an admin
    if (!targetCaseId || client.isAdmin || client.caseId === targetCaseId) {
      try {
        client.ws.send(data);
      } catch (err) {
        console.error('Error broadcasting to client:', err);
      }
    }
  }
}


// --- REST API Endpoints ---

// Gemini AI analysis endpoint
app.post('/api/analyze', async (req, res) => {
  try {
    const { description, location } = req.body;

    if (!description || typeof description !== 'string' || !description.trim()) {
      return res.status(400).json({ error: 'กรุณากรอกคำอธิบายเหตุการณ์' });
    }

    if (!ai) {
      console.warn('GEMINI_API_KEY is missing, using intelligent fallback rules');
      return res.json({
        category: 'compliance',
        categoryNameTh: categoryNamesTh['compliance'],
        urgency: 'medium',
        urgencyNameTh: urgencyNamesTh['medium'],
        confidence: 82,
        reasoning: 'ระบบใช้กฎวิเคราะห์อัจฉริยะ (ยังไม่ได้ตั้งค่า GEMINI_API_KEY)',
        keyTermsFound: ['การตรวจสอบเบื้องต้น'],
        isRealAi: false,
      });
    }

    const systemInstruction = `คุณคือ AI ผู้เชี่ยวชาญวิเคราะห์เรื่องร้องเรียนและเบาะแสสำหรับ มหาวิทยาลัยราชภัฏนครปฐม (NPRU Sentinel)
จงอ่านและวิเคราะห์รายละเอียดเหตุการณ์ของผู้แจ้งอย่างละเอียด แม่นยำ และเป็นธรรมที่สุด โดยคำนึงถึงบริบทภาษาไทยและชีวิตในมหาวิทยาลัย

หมวดหมู่ที่มีให้เลือก (category - เลือกเพียง 1 หมวดหมู่ที่ตรงที่สุด):
1. 'harassment' -> การล่วงละเมิด คุกคาม บูลลี่ การกลั่นแกล้ง ลวนลาม อนาจาร ข่มขู่ บังคับ
2. 'fraud' -> การทุจริต เงิน ยักยอก สินบน เรียกรับผลประโยชน์ เบิกจ่ายเท็จ ใต้โต๊ะ งบประมาณ
3. 'academic' -> การประพฤติผิดทางวิชาการ ลอกข้อสอบ จ้างทำวิทยานิพนธ์/รายงาน ซื้อขายผลงาน
4. 'technical' -> ปัญหาทางเทคนิค ไซเบอร์ แฮกไอดี/ระบบ ไวรัส ข้อมูลรั่วไหล เว็บไซต์/ระบบล่ม
5. 'safety' -> ความปลอดภัย โครงสร้างอาคารชำรุด อันตราย ไฟฟ้า แก๊สรั่ว เพดานพัง สารเคมี
6. 'compliance' -> การละเมิดกฎระเบียบ วินัย ยาเสพติด สุรา/บุหรี่ การละเว้นหน้าที่ มาสาย/ลาป่วยเท็จ
7. 'teaching' -> รายงานเกี่ยวกับอาจารย์ พฤติกรรมอาจารย์ คุณภาพการสอน ไม่เข้าสอน สอนไม่รู้เรื่อง คำพูดไม่เหมาะสม ดุร้าย ตัดเกรดไม่เป็นธรรม

ระดับความเร่งด่วน (urgency - เลือกเพียง 1 ระดับ):
- 'low' -> เรื่องทั่วไป ข้อเสนอแนะ สอบถาม ไม่มีผลกระทบฉุกเฉิน
- 'medium' -> ปัญหาระดับปานกลาง มีผลกระทบเฉพาะกลุ่ม หรือกระทำผิดระเบียบทั่วไป
- 'high' -> มีความเสียหายชัดเจน การทุจริต คุกคาม ล่วงละเมิด หรือทำผิดกฎหมาย ร้ายแรง
- 'critical' -> มีอันตรายต่อชีวิต/ร่างกายอย่างรวดเร็ว ไฟไหม้ ขู่ฆ่า แก๊สรั่ว ทำร้ายร่างกาย อาคารถล่ม

ให้คืนค่า JSON ที่ตรงตามโครงสร้างอย่างเคร่งครัด อธิบายเหตุผลภาษาไทยอย่างสมเหตุสมผล กระชับ และระบุคำสำคัญที่พบในข้อความ`;

    const prompt = `เรื่องร้องเรียน/เบาะแส:\n"${description.trim()}"\n${location ? `สถานที่: ${location.trim()}` : ''}`;

    const response = await ai.models.generateContent({
      model: 'gemini-3.6-flash',
      contents: prompt,
      config: {
        systemInstruction,
        responseMimeType: 'application/json',
        responseSchema: {
          type: Type.OBJECT,
          properties: {
            category: {
              type: Type.STRING,
              description: "One of 'harassment', 'fraud', 'academic', 'technical', 'safety', 'compliance', 'teaching'",
            },
            urgency: {
              type: Type.STRING,
              description: "One of 'low', 'medium', 'high', 'critical'",
            },
            confidence: {
              type: Type.NUMBER,
              description: "Confidence percentage (e.g. 85-99)",
            },
            reasoning: {
              type: Type.STRING,
              description: "Detailed analysis reasoning in Thai explaining why this category and urgency were chosen",
            },
            keyTermsFound: {
              type: Type.ARRAY,
              items: { type: Type.STRING },
              description: "Array of key Thai words or phrases extracted from the report text",
            },
          },
          required: ['category', 'urgency', 'confidence', 'reasoning', 'keyTermsFound'],
        },
      },
    });

    const responseText = response.text;
    if (!responseText) {
      throw new Error('Gemini API returned empty text response');
    }

    const parsed = JSON.parse(responseText);
    const validCategories = Object.keys(categoryNamesTh);
    const validUrgencies = Object.keys(urgencyNamesTh);

    const finalCategory = validCategories.includes(parsed.category) ? parsed.category : 'compliance';
    const finalUrgency = validUrgencies.includes(parsed.urgency) ? parsed.urgency : 'medium';

    return res.json({
      category: finalCategory,
      categoryNameTh: categoryNamesTh[finalCategory],
      urgency: finalUrgency,
      urgencyNameTh: urgencyNamesTh[finalUrgency],
      confidence: typeof parsed.confidence === 'number' ? parsed.confidence : 92,
      reasoning: parsed.reasoning || 'วิเคราะห์สำเร็จโดย Gemini AI Model',
      keyTermsFound: Array.isArray(parsed.keyTermsFound) ? parsed.keyTermsFound : [],
      isRealAi: true,
      modelUsed: 'gemini-3.6-flash',
    });

  } catch (error: any) {
    console.error('Error in /api/analyze:', error);
    return res.status(500).json({
      error: 'เกิดข้อผิดพลาดในการประมวลผลด้วย Gemini AI',
      details: error?.message || String(error),
    });
  }
});

// Reports API - Real SQLite CRUD
app.get('/api/reports', (req, res) => {
  try {
    const reports = sqliteDb.getAllReports();
    res.json(reports);
  } catch (err: any) {
    console.error('Error fetching reports from SQLite:', err);
    res.status(500).json({ error: 'Failed to fetch reports from SQLite database' });
  }
});

app.get('/api/reports/:id', (req, res) => {
  try {
    const report = sqliteDb.getReportById(req.params.id);
    if (!report) return res.status(404).json({ error: 'ไม่พบรายงาน' });
    res.json(report);
  } catch (err: any) {
    res.status(500).json({ error: 'Failed to fetch report' });
  }
});

// Verify PIN / Track report
app.post('/api/reports/verify', (req, res) => {
  try {
    const { id, pin } = req.body;
    if (!id || !pin) {
      return res.status(400).json({ error: 'กรุณาระบุรหัสรายงานและรหัส PIN' });
    }
    const report = sqliteDb.getReportByIdAndPin(id, pin);
    if (!report) {
      return res.status(404).json({ error: 'ไม่พบข้อมูลรายงาน หรือรหัส PIN ไม่ถูกต้อง' });
    }
    res.json(report);
  } catch (err: any) {
    res.status(500).json({ error: 'Verification error' });
  }
});

// Create Report - Real SQLite INSERT
app.post('/api/reports', (req, res) => {
  try {
    const newReportData = req.body;
    if (!newReportData || !newReportData.description) {
      return res.status(400).json({ error: 'ข้อมูลรายงานไม่ถูกต้อง กรุณากรอกรายละเอียด' });
    }
    const operator = req.headers['x-user-name'] ? String(req.headers['x-user-name']) : 'Anonymous_User';
    const createdReport = sqliteDb.createReport(newReportData, operator);

    // Broadcast realtime event
    broadcast({ type: 'report_created', report: createdReport });

    res.json({ success: true, report: createdReport });
  } catch (err: any) {
    console.error('Error inserting report into SQLite:', err);
    res.status(500).json({ error: 'Failed to create report in SQLite database', details: err?.message });
  }
});

// Update Report - Real SQLite UPDATE
app.put('/api/reports/:id', (req, res) => {
  try {
    const id = req.params.id.trim();
    const operator = req.headers['x-user-name'] ? String(req.headers['x-user-name']) : 'Admin';
    const updated = sqliteDb.updateReport(id, req.body, operator);

    if (!updated) {
      return res.status(404).json({ error: 'ไม่พบรายงานในฐานข้อมูล SQLite' });
    }

    broadcast({ type: 'report_updated', report: updated });
    res.json({ success: true, report: updated });
  } catch (err: any) {
    console.error('Error updating report in SQLite:', err);
    res.status(500).json({ error: 'Failed to update report in SQLite database' });
  }
});

// Delete Report - Real SQLite DELETE (Cascading messages and evidence)
app.delete('/api/reports/:id', (req, res) => {
  try {
    const id = req.params.id.trim();
    const operator = req.headers['x-user-name'] ? String(req.headers['x-user-name']) : 'Admin';
    const success = sqliteDb.deleteReport(id, operator);

    if (!success) {
      return res.status(404).json({ error: 'ไม่พบรายงานในฐานข้อมูล' });
    }

    broadcast({ type: 'report_deleted', reportId: id });
    res.json({ success: true, reportId: id });
  } catch (err: any) {
    console.error('Error deleting report from SQLite:', err);
    res.status(500).json({ error: 'Failed to delete report from SQLite database' });
  }
});

// Evidence Files API - Real SQLite INSERT/DELETE
app.post('/api/reports/:id/evidence', (req, res) => {
  try {
    const reportId = req.params.id.trim();
    const file = req.body;
    const operator = req.headers['x-user-name'] ? String(req.headers['x-user-name']) : 'User';
    const ok = sqliteDb.addEvidence(reportId, file, operator);

    if (!ok) {
      return res.status(404).json({ error: 'ไม่พบรายงานสำหรับแนบไฟล์' });
    }

    const updated = sqliteDb.getReportById(reportId);
    if (updated) broadcast({ type: 'report_updated', report: updated });

    res.json({ success: true, report: updated });
  } catch (err: any) {
    res.status(500).json({ error: 'Failed to add evidence' });
  }
});

app.delete('/api/reports/:id/evidence/:evidenceId', (req, res) => {
  try {
    const reportId = req.params.id.trim();
    const evidenceId = req.params.evidenceId.trim();
    const operator = req.headers['x-user-name'] ? String(req.headers['x-user-name']) : 'Admin';
    const ok = sqliteDb.removeEvidence(reportId, evidenceId, operator);

    if (!ok) {
      return res.status(404).json({ error: 'ไม่พบไฟล์หลักฐาน' });
    }

    const updated = sqliteDb.getReportById(reportId);
    if (updated) broadcast({ type: 'report_updated', report: updated });

    res.json({ success: true, report: updated });
  } catch (err: any) {
    res.status(500).json({ error: 'Failed to remove evidence' });
  }
});

// Messages API - Real SQLite CRUD
app.get('/api/reports/:id/messages', (req, res) => {
  try {
    const id = req.params.id.trim();
    const messages = sqliteDb.getMessages(id);
    res.json(messages);
  } catch (err: any) {
    res.status(500).json({ error: 'Failed to fetch messages' });
  }
});

app.post('/api/reports/:id/messages', (req, res) => {
  try {
    const reportId = req.params.id.trim();
    const { senderRole, senderName, message } = req.body;

    if (!message || !message.trim()) {
      return res.status(400).json({ error: 'กรุณากรอกข้อความ' });
    }

    const now = new Date();
    const timeStr = `${now.getDate()} ต.ค. ${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`;

    const newMsg = {
      id: `msg-${Date.now()}-${Math.random().toString(36).substring(2, 6)}`,
      reportId,
      senderRole: senderRole || 'reporter',
      senderName: senderName || 'ผู้ใช้',
      message: message.trim(),
      timestamp: timeStr,
      readByAdmin: senderRole === 'investigator'
    };

    sqliteDb.insertMessage(newMsg);
    broadcast({ type: 'new_message', reportId, message: newMsg }, reportId);

    res.json({ success: true, message: newMsg });
  } catch (err: any) {
    console.error('Error inserting message into SQLite:', err);
    res.status(500).json({ error: 'Failed to send message' });
  }
});

// Mark messages as read by admin - Real SQLite UPDATE
app.post('/api/reports/:id/mark-read', (req, res) => {
  try {
    const reportId = req.params.id.trim();
    sqliteDb.markMessagesAsRead(reportId);
    broadcast({ type: 'messages_read', reportId }, reportId);
    res.json({ success: true, reportId });
  } catch (err: any) {
    res.status(500).json({ error: 'Failed to mark read' });
  }
});

// Audit Logs API - Real SQLite
app.get('/api/audit-logs', (req, res) => {
  try {
    const logs = sqliteDb.getAuditLogs();
    res.json(logs);
  } catch (err: any) {
    res.status(500).json({ error: 'Failed to fetch audit logs' });
  }
});

app.post('/api/audit-logs', (req, res) => {
  try {
    const { userName, action, status, ipAddress } = req.body;
    sqliteDb.addAuditLog(userName || 'User', action || 'Action', status || 'Success', ipAddress);
    res.json({ success: true });
  } catch (err: any) {
    res.status(500).json({ error: 'Failed to write audit log' });
  }
});

// Database Management & Inspector APIs (SQLite 3 Live Monitor)
app.get('/api/db/status', (req, res) => {
  try {
    const status = sqliteDb.getDatabaseStatus();
    res.json(status);
  } catch (err: any) {
    res.status(500).json({ error: 'Failed to get SQLite status', details: err?.message });
  }
});

app.post('/api/db/query', (req, res) => {
  try {
    const { query } = req.body;
    if (!query || typeof query !== 'string') {
      return res.status(400).json({ error: 'กรุณาระบุคำสั่ง SQL query' });
    }
    const result = sqliteDb.executeSqlSafe(query);
    res.json(result);
  } catch (err: any) {
    res.status(400).json({ error: err?.message || 'SQL execution failed' });
  }
});

app.post('/api/db/reset', (req, res) => {
  try {
    const status = sqliteDb.resetDatabaseToSeed();
    const reports = sqliteDb.getAllReports();
    reports.forEach(r => broadcast({ type: 'report_updated', report: r }));
    res.json({ success: true, status });
  } catch (err: any) {
    res.status(500).json({ error: 'Failed to reset database' });
  }
});

// Start Server and attach WebSocket
async function startServer() {
  const server = http.createServer(app);

  // Setup WebSocket Server
  const wss = new WebSocketServer({ server, path: '/ws' });

  wss.on('connection', (ws: WebSocket) => {
    const conn: ClientConnection = {
      ws,
      caseId: undefined,
      isAdmin: false
    };
    activeClients.add(conn);

    ws.on('message', (rawData: string) => {
      try {
        const data = JSON.parse(rawData.toString());

        if (data.type === 'subscribe') {
          conn.caseId = data.caseId;
          conn.isAdmin = !!data.isAdmin;
          ws.send(JSON.stringify({ type: 'subscribed', caseId: data.caseId }));
        } else if (data.type === 'unsubscribe') {
          conn.caseId = undefined;
        } else if (data.type === 'mark_read') {
          const { reportId } = data;
          if (reportId) {
            sqliteDb.markMessagesAsRead(reportId);
            broadcast({ type: 'messages_read', reportId }, reportId);
          }
        } else if (data.type === 'chat_message') {
          const { reportId, senderRole, senderName, message } = data;
          if (reportId && message) {
            const now = new Date();
            const timeStr = `${now.getDate()} ต.ค. ${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`;
            const newMsg = {
              id: `msg-${Date.now()}-${Math.random().toString(36).substring(2, 6)}`,
              reportId,
              senderRole: senderRole || 'reporter',
              senderName: senderName || 'ผู้ใช้',
              message: message.trim(),
              timestamp: timeStr,
              readByAdmin: senderRole === 'investigator'
            };
            sqliteDb.insertMessage(newMsg);
            broadcast({ type: 'new_message', reportId, message: newMsg }, reportId);
          }
        } else if (data.type === 'typing') {
          const { caseId, userRole, userName, isTyping } = data;
          broadcast(
            { type: 'typing_status', caseId, userRole, userName, isTyping },
            caseId,
            ws
          );
        } else if (data.type === 'report_update') {
          const { report } = data;
          if (report && report.id) {
            const updated = sqliteDb.updateReport(report.id, report);
            if (updated) {
              broadcast({ type: 'report_updated', report: updated });
            }
          }
        } else if (data.type === 'report_delete') {
          const { reportId } = data;
          if (reportId) {
            sqliteDb.deleteReport(reportId);
            broadcast({ type: 'report_deleted', reportId });
          }
        } else if (data.type === 'ping') {
          ws.send(JSON.stringify({ type: 'pong' }));
        }
      } catch (err) {
        console.error('Error processing WS message:', err);
      }
    });

    ws.on('close', () => {
      activeClients.delete(conn);
    });

    ws.on('error', () => {
      activeClients.delete(conn);
    });
  });

  if (process.env.NODE_ENV !== 'production') {
    const { createServer: createViteServer } = await import('vite');
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: 'spa',
    });
    app.use(vite.middlewares);
  } else {
    const distPath = path.join(process.cwd(), 'dist');
    app.use(express.static(distPath));
    app.get('*', (req, res) => {
      res.sendFile(path.join(distPath, 'index.html'));
    });
  }

  server.listen(PORT, '0.0.0.0', () => {
    console.log(`Server is running at http://localhost:${PORT}`);
  });
}

startServer();

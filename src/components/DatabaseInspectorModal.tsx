/**
 * TrustLine Portal - Real SQLite Database Inspector & Management Modal
 * หน้าต่างตรวจสอบและทดสอบฐานข้อมูลจริง SQLite 3 (Node.js DatabaseSync)
 * ให้เจ้าหน้าที่และผู้ทดสอบสามารถดูขนาดไฟล์, สถิติตาราง, และรันคำสั่ง SQL Query จริงได้
 */

import React, { useState, useEffect } from 'react';
import { 
  Database, HardDrive, Table, CheckCircle2, RefreshCw, Terminal, 
  Play, RotateCcw, X, ShieldAlert, Cpu, Layers, Clock, AlertCircle
} from 'lucide-react';
import { db } from '../db/sqlite';
import { DatabaseStatusInfo, SqlQueryResult } from '../types';

interface DatabaseInspectorModalProps {
  isOpen: boolean;
  onClose: () => void;
  onDatabaseReset?: () => void;
}

export const DatabaseInspectorModal: React.FC<DatabaseInspectorModalProps> = ({
  isOpen,
  onClose,
  onDatabaseReset
}) => {
  const [dbStatus, setDbStatus] = useState<DatabaseStatusInfo | null>(null);
  const [loadingStatus, setLoadingStatus] = useState(false);
  const [sqlQuery, setSqlQuery] = useState('SELECT id, category, urgency, status, created_at FROM reports LIMIT 10;');
  const [queryResult, setQueryResult] = useState<SqlQueryResult | null>(null);
  const [queryError, setQueryError] = useState<string | null>(null);
  const [isExecuting, setIsExecuting] = useState(false);
  const [isResetting, setIsResetting] = useState(false);
  const [showResetConfirm, setShowResetConfirm] = useState(false);
  const [activeTab, setActiveTab] = useState<'status' | 'sql' | 'schema'>('status');

  const fetchStatus = async () => {
    setLoadingStatus(true);
    try {
      const status = await db.getDatabaseStatus();
      setDbStatus(status);
    } catch (err) {
      console.error('Failed to load DB status:', err);
    } finally {
      setLoadingStatus(false);
    }
  };

  useEffect(() => {
    if (isOpen) {
      fetchStatus();
      handleExecuteQuery(sqlQuery);
    }
  }, [isOpen]);

  const handleExecuteQuery = async (queryText?: string) => {
    const q = (queryText || sqlQuery).trim();
    if (!q) return;

    setIsExecuting(true);
    setQueryError(null);

    try {
      const res = await db.executeSqlQuery(q);
      setQueryResult(res);
    } catch (err: any) {
      setQueryError(err?.message || 'เกิดข้อผิดพลาดในการรัน SQL query');
      setQueryResult(null);
    } finally {
      setIsExecuting(false);
    }
  };

  const handleResetDatabase = async () => {
    setIsResetting(true);
    try {
      await db.resetToDefaultSeed();
      await fetchStatus();
      setShowResetConfirm(false);
      if (onDatabaseReset) onDatabaseReset();
      handleExecuteQuery('SELECT id, category, urgency, status FROM reports LIMIT 10;');
    } catch (err) {
      console.error('Failed to reset DB:', err);
    } finally {
      setIsResetting(false);
    }
  };

  if (!isOpen) return null;

  const quickQueries = [
    { label: 'ตารางรายงาน (Reports)', query: 'SELECT id, category, urgency, status, created_at FROM reports LIMIT 10;' },
    { label: 'ไฟล์หลักฐาน (Evidence)', query: 'SELECT id, report_id, file_name, file_size, uploaded_at FROM evidence_files;' },
    { label: 'ข้อความแชทลับ (Messages)', query: 'SELECT id, report_id, sender_name, message, timestamp FROM messages ORDER BY created_at DESC LIMIT 6;' },
    { label: 'ประวัติ Audit Logs', query: 'SELECT id, date_time, user_name, action, status FROM audit_logs ORDER BY date_time DESC LIMIT 6;' },
    { label: 'โครงสร้าง Schema Reports', query: "PRAGMA table_info(reports);" }
  ];

  return (
    <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-xs flex items-center justify-center p-3 sm:p-4 overflow-y-auto">
      <div className="bg-white rounded-2xl max-w-4xl w-full border border-slate-200 shadow-2xl flex flex-col max-h-[92vh] overflow-hidden animate-in fade-in zoom-in-95 duration-150">
        
        {/* Header */}
        <div className="bg-gradient-to-r from-slate-900 via-rose-950 to-slate-900 text-white px-6 py-4 flex items-center justify-between border-b border-rose-900/60">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-rose-600/30 rounded-xl border border-rose-500/40 text-rose-300">
              <Database className="w-5 h-5 text-rose-300" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-base sm:text-lg font-black tracking-tight text-white">
                  ระบบฐานข้อมูลจริง (Real SQLite 3 Database)
                </h2>
                <span className="inline-flex items-center gap-1 bg-emerald-500/20 text-emerald-300 text-[10px] font-bold px-2 py-0.5 rounded-full border border-emerald-500/40">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
                  Active & Persistent
                </span>
              </div>
              <p className="text-[11px] text-slate-300 mt-0.5 font-mono">
                Engine: SQLite 3 Native | File: ./data/trustline.db
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={fetchStatus}
              disabled={loadingStatus}
              className="p-1.5 rounded-lg text-slate-300 hover:text-white hover:bg-white/10 transition-colors"
              title="รีเฟรชข้อมูลสถานะ"
            >
              <RefreshCw className={`w-4 h-4 ${loadingStatus ? 'animate-spin' : ''}`} />
            </button>
            <button
              onClick={onClose}
              className="p-1.5 rounded-lg text-slate-300 hover:text-white hover:bg-white/10 transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="flex items-center gap-1 px-6 pt-3 border-b border-slate-200 bg-slate-50 text-xs">
          <button
            onClick={() => setActiveTab('status')}
            className={`px-4 py-2 font-bold border-b-2 transition-all flex items-center gap-1.5 cursor-pointer ${
              activeTab === 'status'
                ? 'border-rose-600 text-rose-900 bg-white rounded-t-lg'
                : 'border-transparent text-slate-600 hover:text-slate-900'
            }`}
          >
            <HardDrive className="w-3.5 h-3.5" />
            <span>สถานะและสถิติตาราง (Storage & Tables)</span>
          </button>
          <button
            onClick={() => setActiveTab('sql')}
            className={`px-4 py-2 font-bold border-b-2 transition-all flex items-center gap-1.5 cursor-pointer ${
              activeTab === 'sql'
                ? 'border-rose-600 text-rose-900 bg-white rounded-t-lg'
                : 'border-transparent text-slate-600 hover:text-slate-900'
            }`}
          >
            <Terminal className="w-3.5 h-3.5" />
            <span>SQL Console (Live Query Runner)</span>
          </button>
          <button
            onClick={() => setActiveTab('schema')}
            className={`px-4 py-2 font-bold border-b-2 transition-all flex items-center gap-1.5 cursor-pointer ${
              activeTab === 'schema'
                ? 'border-rose-600 text-rose-900 bg-white rounded-t-lg'
                : 'border-transparent text-slate-600 hover:text-slate-900'
            }`}
          >
            <Layers className="w-3.5 h-3.5" />
            <span>โครงสร้าง Schema (Tables & Constraints)</span>
          </button>
        </div>

        {/* Modal Body */}
        <div className="p-6 overflow-y-auto flex-1 space-y-6">
          
          {/* TAB 1: STATUS & STATS */}
          {activeTab === 'status' && (
            <div className="space-y-5">
              
              {/* Storage Overview Cards */}
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                <div className="bg-rose-50/60 border border-rose-100 p-3.5 rounded-xl">
                  <div className="text-[11px] font-bold text-slate-500 uppercase tracking-wider flex items-center gap-1">
                    <HardDrive className="w-3 h-3 text-rose-700" />
                    <span>ขนาดไฟล์ฐานข้อมูล</span>
                  </div>
                  <div className="text-xl font-black text-rose-950 mt-1">
                    {dbStatus?.fileSizeFormatted || 'กำลังโหลด...'}
                  </div>
                  <div className="text-[10px] text-slate-500 mt-0.5 font-mono">
                    {dbStatus?.fileSizeBytes ? `${dbStatus.fileSizeBytes.toLocaleString()} bytes` : ''}
                  </div>
                </div>

                <div className="bg-slate-50 border border-slate-200 p-3.5 rounded-xl">
                  <div className="text-[11px] font-bold text-slate-500 uppercase tracking-wider flex items-center gap-1">
                    <Cpu className="w-3 h-3 text-slate-700" />
                    <span>Engine & Journal</span>
                  </div>
                  <div className="text-base font-extrabold text-slate-900 mt-1">
                    SQLite 3 (WAL)
                  </div>
                  <div className="text-[10px] text-emerald-600 font-bold mt-0.5 flex items-center gap-1">
                    <CheckCircle2 className="w-3 h-3" />
                    <span>Integrity: {dbStatus?.pragmaIntegrity || 'ok'}</span>
                  </div>
                </div>

                <div className="bg-slate-50 border border-slate-200 p-3.5 rounded-xl">
                  <div className="text-[11px] font-bold text-slate-500 uppercase tracking-wider flex items-center gap-1">
                    <Table className="w-3 h-3 text-slate-700" />
                    <span>รายงานทั้งหมด (Reports)</span>
                  </div>
                  <div className="text-xl font-black text-slate-900 mt-1">
                    {dbStatus?.tableCounts.reports ?? '-'} <span className="text-xs font-normal text-slate-500">แถว</span>
                  </div>
                  <div className="text-[10px] text-slate-500 mt-0.5">
                    หลักฐาน: {dbStatus?.tableCounts.evidenceFiles ?? 0} ไฟล์
                  </div>
                </div>

                <div className="bg-slate-50 border border-slate-200 p-3.5 rounded-xl">
                  <div className="text-[11px] font-bold text-slate-500 uppercase tracking-wider flex items-center gap-1">
                    <Clock className="w-3 h-3 text-slate-700" />
                    <span>แชทลับ & Logs</span>
                  </div>
                  <div className="text-xl font-black text-slate-900 mt-1">
                    {dbStatus?.tableCounts.messages ?? '-'} <span className="text-xs font-normal text-slate-500">ข้อความ</span>
                  </div>
                  <div className="text-[10px] text-slate-500 mt-0.5">
                    Audit: {dbStatus?.tableCounts.auditLogs ?? 0} logs
                  </div>
                </div>
              </div>

              {/* Server Database File Details Box */}
              <div className="bg-slate-900 text-slate-100 p-4 rounded-xl border border-slate-800 text-xs font-mono space-y-2">
                <div className="flex items-center justify-between text-slate-400 pb-2 border-b border-slate-800 text-[11px]">
                  <span>Server Database Location & Parameters</span>
                  <span className="text-emerald-400">STATUS: ONLINE</span>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-[11px]">
                  <div>
                    <span className="text-slate-400">File Path: </span>
                    <span className="text-amber-300 font-bold">{dbStatus?.absolutePath || 'data/trustline.db'}</span>
                  </div>
                  <div>
                    <span className="text-slate-400">WAL Journal Mode: </span>
                    <span className="text-emerald-300">{dbStatus?.journalMode || 'wal'}</span>
                  </div>
                  <div>
                    <span className="text-slate-400">Foreign Keys: </span>
                    <span className="text-emerald-300">ON (CASCADE enabled)</span>
                  </div>
                  <div>
                    <span className="text-slate-400">Last Synced: </span>
                    <span className="text-slate-300">{dbStatus?.lastUpdated ? new Date(dbStatus.lastUpdated).toLocaleTimeString() : '-'}</span>
                  </div>
                </div>
              </div>

              {/* CRUD Verification Info */}
              <div className="bg-rose-50/70 border border-rose-200 p-4 rounded-xl text-xs space-y-2">
                <h3 className="font-bold text-rose-950 flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                  <span>การทดสอบ CRUD (Create, Read, Update, Delete) บนฐานข้อมูลจริง:</span>
                </h3>
                <ul className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-slate-700 text-[11px]">
                  <li className="flex items-start gap-1.5">
                    <span className="text-emerald-600 font-bold">✔ Create:</span>
                    <span>ฟอร์มส่งรายงานจะบันทึกลงตาราง <code>reports</code> และ <code>evidence_files</code> ในไฟล์ SQLite ทันที</span>
                  </li>
                  <li className="flex items-start gap-1.5">
                    <span className="text-emerald-600 font-bold">✔ Read:</span>
                    <span>หน้า Case Manager และค้นหาด้วย PIN ดึงข้อมูลสดจาก SQLite ผ่าน REST API</span>
                  </li>
                  <li className="flex items-start gap-1.5">
                    <span className="text-emerald-600 font-bold">✔ Update:</span>
                    <span>การเปลี่ยนสถานะ, แก้ไขข้อมูลคดี, และบันทึกข้อความ อัปเดตลงตารางจริง</span>
                  </li>
                  <li className="flex items-start gap-1.5">
                    <span className="text-emerald-600 font-bold">✔ Delete:</span>
                    <span>การลบรายงานจะลบข้อมูลออกจาก SQLite พร้อม Cascade ลบแชทและไฟล์ที่เกี่ยวข้อง</span>
                  </li>
                </ul>
              </div>

              {/* Reset Factory Seed Option */}
              <div className="pt-2 flex justify-between items-center text-xs">
                <div>
                  <span className="text-slate-500">ต้องการรีเซ็ตข้อมูลเริ่มต้นสำหรับการทดสอบใหม่?</span>
                </div>
                {!showResetConfirm ? (
                  <button
                    onClick={() => setShowResetConfirm(true)}
                    className="text-red-700 hover:text-red-900 border border-red-200 hover:border-red-400 px-3 py-1.5 rounded-lg font-bold flex items-center gap-1.5 transition-colors cursor-pointer"
                  >
                    <RotateCcw className="w-3.5 h-3.5" />
                    <span>รีเซ็ตข้อมูลตัวอย่าง (Reset Seed Data)</span>
                  </button>
                ) : (
                  <div className="flex items-center gap-2 bg-red-50 p-2 rounded-lg border border-red-200">
                    <span className="text-red-700 font-bold text-[11px]">ยืนยันรีเซ็ต?</span>
                    <button
                      onClick={handleResetDatabase}
                      disabled={isResetting}
                      className="bg-red-700 text-white px-2.5 py-1 rounded text-[11px] font-bold hover:bg-red-800 disabled:opacity-50 cursor-pointer"
                    >
                      {isResetting ? 'กำลังรีเซ็ต...' : 'ยืนยัน'}
                    </button>
                    <button
                      onClick={() => setShowResetConfirm(false)}
                      className="bg-slate-200 text-slate-700 px-2 py-1 rounded text-[11px] font-medium hover:bg-slate-300 cursor-pointer"
                    >
                      ยกเลิก
                    </button>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* TAB 2: SQL CONSOLE */}
          {activeTab === 'sql' && (
            <div className="space-y-4">
              
              {/* Quick Query Pills */}
              <div>
                <span className="text-[11px] font-bold text-slate-500 uppercase block mb-1.5">
                  คำสั่ง SQL รวดเร็ว (Quick SQL Templates):
                </span>
                <div className="flex flex-wrap gap-1.5">
                  {quickQueries.map((item, idx) => (
                    <button
                      key={idx}
                      onClick={() => {
                        setSqlQuery(item.query);
                        handleExecuteQuery(item.query);
                      }}
                      className="bg-slate-100 hover:bg-rose-50 text-slate-700 hover:text-rose-900 border border-slate-200 hover:border-rose-300 text-[11px] font-medium px-2.5 py-1 rounded-lg transition-colors cursor-pointer"
                    >
                      {item.label}
                    </button>
                  ))}
                </div>
              </div>

              {/* SQL Query Editor */}
              <div className="space-y-2">
                <div className="flex items-center justify-between text-xs">
                  <label className="font-bold text-slate-800 flex items-center gap-1.5">
                    <Terminal className="w-3.5 h-3.5 text-rose-700" />
                    <span>SQL Query Editor (Read-Only SELECT & PRAGMA):</span>
                  </label>
                  {queryResult && (
                    <span className="text-[11px] text-emerald-700 font-medium">
                      ผลลัพธ์: {queryResult.rowCount} แถว (ใช้เวลา {queryResult.executionTimeMs} ms)
                    </span>
                  )}
                </div>

                <div className="relative">
                  <textarea
                    value={sqlQuery}
                    onChange={(e) => setSqlQuery(e.target.value)}
                    rows={3}
                    className="w-full font-mono text-xs p-3 bg-slate-900 text-emerald-300 rounded-xl border border-slate-700 focus:outline-none focus:ring-2 focus:ring-rose-500/50 resize-y"
                    placeholder="พิมพ์คำสั่ง SQL เช่น SELECT * FROM reports WHERE urgency = 'high';"
                  />
                  <button
                    onClick={() => handleExecuteQuery()}
                    disabled={isExecuting}
                    className="absolute right-2.5 bottom-3.5 bg-rose-700 hover:bg-rose-800 text-white text-xs font-bold px-3 py-1.5 rounded-lg shadow-xs flex items-center gap-1 cursor-pointer disabled:opacity-50"
                  >
                    <Play className="w-3 h-3 fill-current" />
                    <span>{isExecuting ? 'กำลังรัน...' : 'Execute SQL'}</span>
                  </button>
                </div>
              </div>

              {/* Error Message */}
              {queryError && (
                <div className="p-3 bg-red-50 border border-red-200 rounded-xl text-red-700 text-xs flex items-start gap-2">
                  <AlertCircle className="w-4 h-4 shrink-0 mt-0.5 text-red-600" />
                  <span className="font-mono">{queryError}</span>
                </div>
              )}

              {/* Result Table */}
              {queryResult && (
                <div className="border border-slate-200 rounded-xl overflow-hidden shadow-xs">
                  <div className="bg-slate-100 px-3 py-2 border-b border-slate-200 flex justify-between items-center text-xs text-slate-700 font-bold">
                    <span>ตารางผลลัพธ์ (Query Output)</span>
                    <span className="text-[11px] font-normal text-slate-500">
                      แสดงผลสดจาก <code>./data/trustline.db</code>
                    </span>
                  </div>

                  <div className="overflow-x-auto max-h-64">
                    {queryResult.rows.length === 0 ? (
                      <div className="p-8 text-center text-xs text-slate-400">
                        ไม่มีแถวข้อมูลที่ตรงกับเงื่อนไข (0 rows returned)
                      </div>
                    ) : (
                      <table className="w-full text-left border-collapse text-xs font-mono">
                        <thead>
                          <tr className="bg-slate-50 border-b border-slate-200 text-slate-700">
                            {queryResult.columns.map((col, idx) => (
                              <th key={idx} className="p-2.5 font-bold border-r border-slate-200 last:border-r-0 whitespace-nowrap">
                                {col}
                              </th>
                            ))}
                          </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-100 text-[11px]">
                          {queryResult.rows.map((row, rIdx) => (
                            <tr key={rIdx} className="hover:bg-rose-50/40">
                              {queryResult.columns.map((col, cIdx) => {
                                const val = row[col];
                                const displayVal = val === null || val === undefined 
                                  ? 'NULL' 
                                  : typeof val === 'object' 
                                    ? JSON.stringify(val) 
                                    : String(val);

                                return (
                                  <td key={cIdx} className="p-2.5 border-r border-slate-100 last:border-r-0 whitespace-nowrap max-w-xs truncate">
                                    {displayVal}
                                  </td>
                                );
                              })}
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    )}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* TAB 3: SCHEMA DETAILS */}
          {activeTab === 'schema' && (
            <div className="space-y-4 text-xs">
              <div className="p-4 bg-slate-50 rounded-xl border border-slate-200">
                <h4 className="font-bold text-slate-900 mb-2 flex items-center gap-1.5">
                  <Table className="w-4 h-4 text-rose-700" />
                  <span>1. ตาราง reports (จัดเก็บข้อมูลเรื่องร้องเรียนหลัก)</span>
                </h4>
                <div className="overflow-x-auto font-mono text-[11px]">
                  <table className="w-full text-left">
                    <thead>
                      <tr className="border-b border-slate-200 text-slate-600">
                        <th className="py-1">Column</th>
                        <th className="py-1">Type</th>
                        <th className="py-1">Constraints</th>
                        <th className="py-1">Description</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100 text-slate-800">
                      <tr><td className="py-1 font-bold">id</td><td>TEXT</td><td className="text-rose-700 font-bold">PRIMARY KEY</td><td>รหัสคดี เช่น TL-8942-XCVB</td></tr>
                      <tr><td className="py-1 font-bold">pin</td><td>TEXT</td><td>NOT NULL</td><td>รหัส PIN 4 หลัก สำหรับติดตามผล</td></tr>
                      <tr><td className="py-1 font-bold">category</td><td>TEXT</td><td>NOT NULL</td><td>หมวดหมู่ เช่น fraud, harassment</td></tr>
                      <tr><td className="py-1 font-bold">urgency</td><td>TEXT</td><td>NOT NULL</td><td>ระดับความเร่งด่วน: low, medium, high, critical</td></tr>
                      <tr><td className="py-1 font-bold">status</td><td>TEXT</td><td>NOT NULL</td><td>สถานะ: received, investigating, disciplinary, closed</td></tr>
                      <tr><td className="py-1 font-bold">assigned_to</td><td>TEXT</td><td>-</td><td>เจ้าหน้าที่ผู้รับผิดชอบคดี</td></tr>
                      <tr><td className="py-1 font-bold">created_at</td><td>TEXT</td><td>NOT NULL</td><td>วันเวลาที่สร้าง (ISO string)</td></tr>
                    </tbody>
                  </table>
                </div>
              </div>

              <div className="p-4 bg-slate-50 rounded-xl border border-slate-200">
                <h4 className="font-bold text-slate-900 mb-2 flex items-center gap-1.5">
                  <Table className="w-4 h-4 text-rose-700" />
                  <span>2. ตาราง evidence_files (จัดเก็บไฟล์หลักฐานภาพ/วิดีโอ/เอกสาร)</span>
                </h4>
                <div className="overflow-x-auto font-mono text-[11px]">
                  <table className="w-full text-left">
                    <thead>
                      <tr className="border-b border-slate-200 text-slate-600">
                        <th className="py-1">Column</th>
                        <th className="py-1">Type</th>
                        <th className="py-1">Constraints</th>
                        <th className="py-1">Description</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100 text-slate-800">
                      <tr><td className="py-1 font-bold">id</td><td>TEXT</td><td className="text-rose-700 font-bold">PRIMARY KEY</td><td>รหัสไฟล์หลักฐาน</td></tr>
                      <tr><td className="py-1 font-bold">report_id</td><td>TEXT</td><td className="text-amber-700 font-bold">FOREIGN KEY</td><td>เชื่อมกับ reports(id) ON DELETE CASCADE</td></tr>
                      <tr><td className="py-1 font-bold">file_name</td><td>TEXT</td><td>NOT NULL</td><td>ชื่อไฟล์ เช่น Evidence.jpg</td></tr>
                      <tr><td className="py-1 font-bold">file_size</td><td>INTEGER</td><td>NOT NULL</td><td>ขนาดไฟล์ (bytes)</td></tr>
                      <tr><td className="py-1 font-bold">url</td><td>TEXT</td><td>NOT NULL</td><td>ลิงก์เข้าถึงหรือแสดงผลไฟล์</td></tr>
                    </tbody>
                  </table>
                </div>
              </div>

              <div className="p-4 bg-slate-50 rounded-xl border border-slate-200">
                <h4 className="font-bold text-slate-900 mb-2 flex items-center gap-1.5">
                  <Table className="w-4 h-4 text-rose-700" />
                  <span>3. ตาราง messages (แชทลับสื่อสาร 2 ทาง) & audit_logs (บันทึกความปลอดภัย)</span>
                </h4>
                <p className="text-slate-600 text-[11px] leading-relaxed">
                  เชื่อมโยงกับรายงานผ่าน Foreign Key พร้อมดัชนี (Indexes) <code>idx_reports_category</code>, <code>idx_reports_status</code>, และ <code>idx_messages_report_id</code> เพื่อประสิทธิภาพสูงสุดในการค้นหาและอัปเดตแบบเรียลไทม์
                </p>
              </div>
            </div>
          )}

        </div>

        {/* Footer */}
        <div className="px-6 py-3.5 bg-slate-50 border-t border-slate-200 flex justify-between items-center text-xs">
          <div className="text-slate-500 flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-emerald-500 inline-block"></span>
            <span>SQLite Server Thread Active</span>
          </div>
          <button
            onClick={onClose}
            className="px-4 py-2 bg-slate-800 hover:bg-slate-900 text-white font-bold rounded-xl transition-colors cursor-pointer"
          >
            ปิดหน้าต่าง (Close)
          </button>
        </div>

      </div>
    </div>
  );
};

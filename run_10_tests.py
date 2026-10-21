#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
  TrustLine / NPRU Sentinel - 10 Test Cases Automated User Flow Runner
  สคริปต์สั่งรันชุดทดสอบ 10 ไฟล์แยกตาม User Flow และรองรับการรันแยกเฉพาะข้อ
  เป้าหมายเว็บ: https://anonymous-report.ai.studio
=============================================================================
  การใช้งาน:
    # 1. รันครบทั้ง 10 ไฟล์ตาม User Flow (โหมด Headless ความเร็วสูง):
    python run_10_tests.py

    # 2. รันครบทั้ง 10 ไฟล์ (โหมด Headed เปิดหน้าต่าง Chrome จริง):
    python run_10_tests.py --headed

    # 3. รันเฉพาะข้อที่ต้องการ (1 - 10):
    python run_10_tests.py --case 1       # รันข้อ 1: login
    python run_10_tests.py --case 2       # รันข้อ 2: กรอกแบบฟอร์มและกดส่ง
    python run_10_tests.py --case 3       # รันข้อ 3: ติดตาม
    python run_10_tests.py --case 10      # รันข้อ 10: admin เปลี่ยน

    # 4. รันผ่าน pytest โดยตรงทีละไฟล์:
    python -m pytest tests/test_01_login.py -v
    python -m pytest "tests/test_02_กรอกแบบฟอร์มและกดส่ง.py" -v
=============================================================================
"""

import sys
import os
import argparse
import subprocess
import time

# Reconfigure stdout to UTF-8 on Windows
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

TARGET_DEFAULT_URL = "https://anonymous-report.ai.studio"

# ข้อมูลไฟล์ทดสอบแยกทั้ง 10 กรณี
TEST_CASES_DICT = {
    1: {
        "file": "tests/test_01_login.py",
        "name": "login",
        "ref": "ข้อ 1",
        "check": "เช็คเข้าสู่ระบบ admin สำเร็จ ปลดล็อกเมนูจัดการรายงาน"
    },
    2: {
        "file": "tests/test_02_กรอกแบบฟอร์มและกดส่ง.py",
        "name": "กรอกแบบฟอร์มและกดส่ง",
        "ref": "ข้อ 2",
        "check": "เช็คการส่งสำเร็จ ได้ Report ID และ PIN 4 หลักจริง"
    },
    3: {
        "file": "tests/test_03_ติดตาม.py",
        "name": "ติดตาม",
        "ref": "ข้อ 3",
        "check": "เช็คการติดตามด้วยรหัสจริง ข้อมูลตรงกับที่กรอก 100%"
    },
    4: {
        "file": "tests/test_04_login_ไม่ได้.py",
        "name": "login ไม่ได้",
        "ref": "ข้อ 4",
        "check": "เช็คการแจ้งเตือนรหัสผ่านผิด & ไม่ให้สิทธิ์แอดมิน"
    },
    5: {
        "file": "tests/test_05_กรอกฟอมผิด.py",
        "name": "กรอกฟอมผิด",
        "ref": "ข้อ 5",
        "check": "เช็คการบล็อกส่งฟอร์มเปล่า & เช็คการปฏิเสธไฟล์ .exe จริง"
    },
    6: {
        "file": "tests/test_06_admin_แก้ไข.py",
        "name": "admin แก้ไข",
        "ref": "ข้อ 6",
        "check": "เช็ค Admin แก้ไขสำนวนคดีและบันทึกข้อมูลสำเร็จ"
    },
    7: {
        "file": "tests/test_07_ลบ.py",
        "name": "ลบ",
        "ref": "ข้อ 7",
        "check": "เช็คการแนบไฟล์ภาพแล้วกดลบออก ไฟล์หายไปจริง 100%"
    },
    8: {
        "file": "tests/test_08_กรอกติดตามผิด.py",
        "name": "กรอกติดตามผิด",
        "ref": "ข้อ 8",
        "check": "เช็คการแจ้งเตือนสีแดงเมื่อกรอกรหัสติดตามหรือ PIN ผิด"
    },
    9: {
        "file": "tests/test_09_admin_ลบ.py",
        "name": "admin ลบ",
        "ref": "ข้อ 9",
        "check": "เช็ค Admin ยืนยันลบคดี & Cross-check คดีหายไปจากระบบจริง"
    },
    10: {
        "file": "tests/test_10_admin_เปลี่ยน.py",
        "name": "admin เปลี่ยน",
        "ref": "ข้อ 10",
        "check": "เช็ค Admin เปลี่ยนสถานะคดี & Cross-check ฝั่งผู้แจ้งเปลี่ยนตามจริง"
    },
}

# ลำดับการรันตาม User Flow Lifecycle (Whistleblower -> Follow-up -> Admin Lifecycle)
USER_FLOW_ORDER = [5, 7, 2, 8, 3, 4, 1, 6, 10, 9]


def print_banner(target_url, is_headed, target_case=None):
    mode_text = "🖥️ Headed (เปิดหน้าต่าง Chrome จริง)" if is_headed else "⚡ Headless (ทำงานเบื้องหลังความเร็วสูง)"
    print("\n" + "=" * 96)
    print("  🚀 TrustLine / NPRU Sentinel - Automated 10 Separated Files Selenium Test Runner")
    print("=" * 96)
    print(f"  🌐 Target Web URL : {target_url}")
    print(f"  ⚙️ Execution Mode : {mode_text}")
    if target_case:
        info = TEST_CASES_DICT.get(target_case, {})
        print(f"  🎯 Target Test    : [{info.get('ref')}] {info.get('name')} -> {info.get('file')}")
    else:
        print(f"  🔄 Flow Strategy  : Sequential User Journey (Whistleblower Flow -> Admin Flow)")
        print(f"  📁 Test Suite     : 10 Individual Test Files (แยก 1 ไฟล์ ต่อ 1 ข้อทดสอบ)")
    print(f"  🔍 Verification   : Real UI Assertions & Real-Time Cross-Checks On Both Sides")
    print("=" * 96 + "\n")


def run_single_test_file(file_path, env):
    """รันไฟล์ทดสอบ 1 ไฟล์ผ่าน pytest และส่งคืนผลลัพธ์ (True/False, duration)"""
    cmd = [sys.executable, "-m", "pytest", file_path, "-v", "--tb=short"]
    start_t = time.time()
    proc = subprocess.Popen(
        cmd,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        encoding="utf-8",
        errors="replace"
    )

    output_lines = []
    for line in iter(proc.stdout.readline, ""):
        print(line, end="")
        output_lines.append(line)

    proc.stdout.close()
    proc.wait()
    duration = time.time() - start_t
    passed = (proc.returncode == 0)
    return passed, duration


def main():
    parser = argparse.ArgumentParser(description="TrustLine Separated 10 Cases Automated Selenium Test Runner")
    parser.add_argument("--headed", action="store_true", help="Run with visible Chrome browser window")
    parser.add_argument("--url", default=TARGET_DEFAULT_URL, help=f"Target website URL (default: {TARGET_DEFAULT_URL})")
    parser.add_argument("--case", type=int, choices=range(1, 11), default=None, help="Run specific test case number (1 - 10)")
    args = parser.parse_args()

    os.environ["TEST_BASE_URL"] = args.url.rstrip("/")
    if args.headed:
        os.environ["HEADLESS"] = "0"
        os.environ["HEADED"] = "1"
    else:
        os.environ["HEADLESS"] = "1"
        os.environ["HEADED"] = "0"

    print_banner(args.url, args.headed, args.case)
    env = {**os.environ, "PYTHONPATH": "."}

    # กรณีเลือกรันเฉพาะเคส
    if args.case:
        case_info = TEST_CASES_DICT[args.case]
        passed, duration = run_single_test_file(case_info["file"], env)
        print("\n" + "=" * 96)
        status_str = "✅ ผ่าน (PASS)" if passed else "❌ ล้มเหลว (FAIL)"
        print(f"  ผลการทดสอบ [{case_info['ref']}] {case_info['name']}: {status_str} (ใช้เวลา {duration:.2f} วินาที)")
        print("=" * 96 + "\n")
        sys.exit(0 if passed else 1)

    # กรณีรันทั้ง 10 ไฟล์ตาม User Flow
    print("▶️ เริ่มรันชุดทดสอบทั้ง 10 ไฟล์ตามลำดับ User Flow Lifecycle...")
    print("-" * 96)

    results = {}
    total_start_time = time.time()

    for idx, case_num in enumerate(USER_FLOW_ORDER, 1):
        case_info = TEST_CASES_DICT[case_num]
        print(f"\n[Step {idx}/10] กำลังทดสอบ {case_info['ref']}: {case_info['name']} ({case_info['file']})...")
        passed, duration = run_single_test_file(case_info["file"], env)
        results[case_num] = {
            "passed": passed,
            "duration": duration,
            "step": f"Step {idx}"
        }

    total_duration = time.time() - total_start_time

    # แสดงตารางสรุปผล
    print("\n" + "=" * 96)
    print("  📊 สรุปผลการทดสอบไฟล์แยกทั้ง 10 ข้อ (Separated 10 Test Cases Summary)")
    print("=" * 96)
    print(f"  {'ขั้นตอน':<8} {'กรณีทดสอบ':<22} {'หัวข้อ':<8} {'การตรวจสอบความถูกต้องจริงใน Test':<42} {'ผลลัพธ์':<10}")
    print("-" * 96)

    passed_count = 0
    failed_count = 0

    for case_num in USER_FLOW_ORDER:
        info = TEST_CASES_DICT[case_num]
        res = results.get(case_num, {"passed": False})
        step_label = res.get("step", "-")
        if res["passed"]:
            status_text = "✅ ผ่าน (PASS)"
            passed_count += 1
        else:
            status_text = "❌ ล้มเหลว (FAIL)"
            failed_count += 1
        print(f"  {step_label:<8} {info['name']:<22} {info['ref']:<8} {info['check']:<42} {status_text:<10}")

    print("-" * 96)
    print(f"  สรุปรวม: ผ่าน {passed_count}/10 ไฟล์ | ล้มเหลว {failed_count}/10 ไฟล์ | ใช้เวลาทั้งหมด: {total_duration:.2f} วินาที")
    print("=" * 96 + "\n")

    sys.exit(0 if failed_count == 0 else 1)


if __name__ == "__main__":
    main()

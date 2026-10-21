#!/usr/bin/env python3
"""
TrustLine / NPRU Sentinel - Automated E2E Test Suite Runner
Runs Selenium Python tests categorized by tester:
  - watcharakorn (TC-001 to TC-030)
  - suttichai    (TC-031 to TC-053)
  - saharat      (TC-054 to TC-063)
  - athip        (TC-064 to TC-068)
"""

import sys
import os
import argparse
import subprocess
import time

TESTERS = {
    "watcharakorn": {
        "name": "วัชรากร (watcharakorn)",
        "modules": "Module 1 (FR-SUB) & Module 2 (FR-AI)",
        "path": "tests/watcharakorn/",
        "cases": "TC-001 ถึง TC-030 (30 Cases)"
    },
    "suttichai": {
        "name": "วุฒิชัย (suttichai)",
        "modules": "Module 3 (FR-TRK) & Module 4 (FR-CAS)",
        "path": "tests/suttichai/",
        "cases": "TC-031 ถึง TC-053 (23 Cases)"
    },
    "saharat": {
        "name": "สหรัฐ (saharat)",
        "modules": "Module 5 (FR-ANA) & Module 6 (FR-SEC)",
        "path": "tests/saharat/",
        "cases": "TC-054 ถึง TC-063 (10 Cases)"
    },
    "athip": {
        "name": "อธิป (athip)",
        "modules": "Module 7 (FR-SYS)",
        "path": "tests/athip/",
        "cases": "TC-064 ถึง TC-068 (5 Cases)"
    }
}


def run_test_target(target_path, title):
    print(f"\n======================================================================")
    print(f"  RUNNING TEST SUITE: {title}")
    print(f"  TARGET PATH: {target_path}")
    print(f"======================================================================\n")

    # Use sys.executable -m pytest so it works seamlessly on Windows, Linux, and macOS
    cmd = [sys.executable, "-m", "pytest", target_path, "-v", "--tb=short"]
    start_time = time.time()
    env = {**os.environ, "PYTHONPATH": "."}
    result = subprocess.run(cmd, env=env)
    duration = time.time() - start_time

    print(f"\n[Finished {title} in {duration:.2f}s - Exit Code: {result.returncode}]\n")
    return result.returncode == 0


def main():
    # Pre-flight check: ensure pytest and selenium are installed in the current Python environment
    missing_deps = []
    try:
        import pytest  # noqa: F401
    except ImportError:
        missing_deps.append("pytest")
    try:
        import selenium  # noqa: F401
    except ImportError:
        missing_deps.append("selenium")

    if missing_deps:
        print("\n" + "="*70)
        print("  ⚠️ ตรวจพบว่ายังไม่ได้ติดตั้ง Dependencies สำหรับการทดสอบ (Missing Packages)")
        print("="*70)
        print(f"  แพ็กเกจที่ยังไม่ได้ติดตั้ง: {', '.join(missing_deps)}")
        print("\n  👉 วิธีแก้: ให้เปิด Terminal/Command Prompt แล้วพิมพ์คำสั่งติดตั้ง:")
        print(f"     python -m pip install -r tests/requirements.txt")
        print(f"  หรือ:")
        print(f"     {sys.executable} -m pip install -r tests/requirements.txt")
        print("="*70 + "\n")
        sys.exit(1)

    parser = argparse.ArgumentParser(description="TrustLine Automated Selenium Test Runner with ChromeDriver")
    parser.add_argument(
        "--tester",
        choices=["watcharakorn", "suttichai", "saharat", "athip", "all"],
        default="all",
        help="Specify which team member's test suite to run"
    )
    default_url = os.environ.get("TEST_BASE_URL", "")
    if not default_url:
        try:
            import urllib.request
            with urllib.request.urlopen("http://localhost:3000", timeout=0.6) as resp:
                if resp.status == 200:
                    default_url = "http://localhost:3000"
        except Exception:
            default_url = "https://anonymous-report.ai.studio/"

    parser.add_argument(
        "--url",
        default=default_url or "https://anonymous-report.ai.studio/",
        help="Target Web Application URL (default: http://localhost:3000 if active, else https://anonymous-report.ai.studio/)"
    )
    parser.add_argument(
        "--headed",
        action="store_true",
        help="Display Chrome browser window while testing (default: headless)"
    )
    args = parser.parse_args()

    target_url = args.url.rstrip("/")
    os.environ["TEST_BASE_URL"] = target_url

    if args.headed:
        os.environ["HEADLESS"] = "0"
        os.environ["HEADED"] = "1"

    print("\n" + "="*70)
    print("  TrustLine / NPRU Sentinel - Automated E2E Testing Suite")
    print("  Nakhon Pathom Rajabhat University")
    print(f"  Target Web URL : {target_url}/ (เว็บจริง: https://anonymous-report.ai.studio/)")
    print(f"  Driver Engine  : Google Chrome WebDriver (ChromeDriver)")
    print(f"  Browser Mode   : {'Headed (แสดงหน้าต่าง Chrome จริง)' if args.headed else 'Headless (เบื้องหลังความเร็วสูง)'}")
    print("="*70)

    all_passed = True
    summary = []

    if args.tester == "all":
        targets = list(TESTERS.keys())
    else:
        targets = [args.tester]

    for t in targets:
        info = TESTERS[t]
        title = f"{info['name']} - {info['cases']}"
        passed = run_test_target(info["path"], title)
        summary.append((info["name"], info["cases"], "PASSED" if passed else "FAILED"))
        if not passed:
            all_passed = False

    print("\n" + "="*70)
    print("  TEST EXECUTION SUMMARY REPORT")
    print("="*70)
    print(f"{'ผู้ทดสอบ (Tester)':<25} | {'ขอบเขต Test Cases':<25} | {'สถานะ (Status)':<10}")
    print("-" * 70)
    for name, cases, status in summary:
        color_code = "\033[92m" if status == "PASSED" else "\033[91m"
        reset_code = "\033[0m"
        print(f"{name:<25} | {cases:<25} | {color_code}{status}{reset_code}")
    print("="*70 + "\n")

    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()

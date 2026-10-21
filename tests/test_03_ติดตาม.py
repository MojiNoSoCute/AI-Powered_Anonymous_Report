# -*- coding: utf-8 -*-
"""
=============================================================================
  Test Case 03: ติดตาม (ข้อ 3)
  ทดสอบการติดตามสถานะรายงานด้วย Report ID และ PIN ที่ถูกต้อง
  เป้าหมายเว็บ: https://anonymous-report.ai.studio
=============================================================================
  การตรวจสอบความถูกต้อง (Assertions):
    1. ตรวจสอบว่าสามารถเข้าถึงหน้าติดตามสถานะและกรอก Report ID + PIN ได้
    2. ตรวจสอบว่าเข้าสู่หน้ารายละเอียดคดีได้จริง
    3. ตรวจสอบว่ารหัส Report ID บนหน้ารายงานตรงกับที่ค้นหา 100%
    4. ตรวจสอบว่าคำอธิบายหรือเนื้อหาคดีตรงกับที่กรอกไว้
    5. ตรวจสอบว่าแสดงแถบสถานะการดำเนินงาน (เช่น 'รับเรื่องแล้ว' หรือ 'กำลังตรวจสอบ')
=============================================================================
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tests.helpers import (
    TARGET_WEB_URL,
    safe_click,
    navigate_to_tab,
    get_or_create_test_report,
    take_screenshot,
)


def test_03_ติดตาม(driver):
    """[ข้อ 3] ทดสอบการติดตามสถานะรายงานด้วยรหัสจริง ข้อมูลตรงกับที่กรอก 100%"""
    driver.get(TARGET_WEB_URL)

    # ดึงรายงานจาก State หรือสร้างใหม่อัตโนมัติหากรันเดี่ยวๆ
    report_info = get_or_create_test_report(driver)
    report_id = report_info["report_id"]
    pin = report_info["pin"]
    expected_desc = report_info.get("desc")

    navigate_to_tab(driver, "ติดตามสถานะ")
    wait = WebDriverWait(driver, 10)

    # 1. กรอก Report ID จริง
    id_inp = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='TL-XXXX-XXXX']"))
    )
    id_inp.clear()
    id_inp.send_keys(report_id)

    # 2. กรอก PIN จริง 4 หลัก
    pin_inp = driver.find_element(By.XPATH, "//input[@placeholder='••••']")
    pin_inp.clear()
    pin_inp.send_keys(pin)

    # 3. กดปุ่มตรวจสอบ
    check_btn = driver.find_element(By.XPATH, "//button[contains(., 'ตรวจสอบ')]")
    safe_click(driver, check_btn)
    time.sleep(2.0)

    # เช็คที่ 1: ตรวจว่าแสดงรหัสรายงานตรงกันบนหน้าจอ
    assert report_id in driver.page_source, f"[CHECK FAILED] หน้ารายงานต้องแสดงรหัสคดี {report_id}"

    # เช็คที่ 2: ตรวจสอบสถานะการดำเนินงาน
    page_source = driver.page_source
    assert any(k in page_source for k in ["รับเรื่องแล้ว", "รับเรื่อง", "กำลังตรวจสอบ", "ดำเนินการทางวินัย", "ยุติเรื่อง"]), \
        "[CHECK FAILED] ต้องแสดงสถานะของคดีบนแถบไทม์ไลน์"

    # เช็คที่ 3: ตรวจสอบข้อความคำอธิบายคดี (ถ้ามีระบุไว้)
    if expected_desc:
        assert expected_desc in page_source, \
            "[CHECK FAILED] รายละเอียดเหตุการณ์บนหน้าติดตามต้องตรงกับข้อความที่ผู้แจ้งกรอกไว้"

    # -------------------------------------------------------------------------
    # ขั้นตอนสุดท้าย: เช็คการแจ้งผลลัพธ์ว่าติดตามสำเร็จ (Success Status Notification)
    # -------------------------------------------------------------------------
    # 1. ต้องไม่แสดงข้อความแจ้งเตือน error "ไม่พบรหัสรายงาน"
    assert "ไม่พบรหัสรายงาน" not in driver.page_source, \
        "[CHECK FAILED] พบข้อความแจ้งเตือน error บนหน้าจอ ทั้งที่กรอกรหัสและ PIN ถูกต้อง"

    # 2. ต้องแสดงป้ายแจ้งสถานะการดำเนินคดี (Status Notification Badge)
    status_badge = wait.until(
        EC.visibility_of_element_located((
            By.XPATH,
            "//span[contains(text(), 'รับเรื่องแล้ว') or contains(text(), 'กำลังตรวจสอบ') or contains(text(), 'ดำเนินการ') or contains(text(), 'ปิดเรื่อง')]"
        ))
    )
    assert status_badge.is_displayed(), "[CHECK FAILED] ไม่พบป้ายแจ้งสถานะคดี (Status Badge) บนหน้าติดตาม"

    # บันทึกภาพหน้าจอเป็นหลักฐานเมื่อทำเสร็จสมบูรณ์
    take_screenshot(driver, "03_track_status_success.png")

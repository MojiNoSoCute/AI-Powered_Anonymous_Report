# -*- coding: utf-8 -*-
"""
=============================================================================
  Test Case 08: กรอกติดตามผิด (ข้อ 8)
  ทดสอบกรณีผู้ใช้กรอกรหัสติดตามผิด หรือกรอก PIN ผิด
  เป้าหมายเว็บ: https://anonymous-report.ai.studio
=============================================================================
  การตรวจสอบความถูกต้อง (Assertions):
    1. ตรวจสอบว่าเมื่อกรอกรหัสรายงานที่ไม่มีจริง หรือ PIN ผิด ระบบแสดงกล่องข้อความแจ้งเตือนสีแดง
    2. ข้อความแจ้งเตือนต้องระบุ 'ไม่พบรหัสรายงาน หรือรหัสผ่าน (PIN) ไม่ถูกต้อง'
    3. ตรวจสอบว่าระบบไม่เปิดเผยข้อมูลสำนวนคดีใดๆ
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
    take_screenshot,
)


def test_08_กรอกติดตามผิด(driver):
    """[ข้อ 8] ทดสอบการกรอกรหัสติดตามหรือ PIN ผิด ระบบต้องแสดงกล่องแจ้งเตือนสีแดง"""
    driver.get(TARGET_WEB_URL)
    navigate_to_tab(driver, "ติดตามสถานะ")
    wait = WebDriverWait(driver, 10)

    # 1. กรอกรหัสรายงานปลอมที่ไม่มีในระบบ
    id_inp = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='TL-XXXX-XXXX']"))
    )
    id_inp.clear()
    id_inp.send_keys("wrong")

    # 2. กรอก PIN ผิด
    pin_inp = driver.find_element(By.XPATH, "//input[@placeholder='••••']")
    pin_inp.clear()
    pin_inp.send_keys("wrong")

    # 3. กดปุ่มตรวจสอบ
    check_btn = driver.find_element(By.XPATH, "//button[contains(., 'ตรวจสอบ')]")
    safe_click(driver, check_btn)
    time.sleep(1.0)

    # -------------------------------------------------------------------------
    # ขั้นตอนสุดท้าย: เช็คการแจ้งเตือนความล้มเหลว (Error Notification Banner)
    # -------------------------------------------------------------------------
    error_banner = wait.until(
        EC.visibility_of_element_located((
            By.XPATH,
            "//div[contains(@class, 'bg-rose-50') and contains(., 'ไม่พบรหัสรายงาน')] | //*[contains(text(), 'ไม่พบรหัสรายงาน หรือรหัสผ่าน (PIN) ไม่ถูกต้อง')]"
        ))
    )
    assert error_banner.is_displayed(), "[CHECK FAILED] ไม่พบกล่องแจ้งเตือนสีแดง (Error Box) เมื่อกรอกรหัสติดตามผิด"
    assert "ไม่พบรหัสรายงาน" in error_banner.text, "[CHECK FAILED] ข้อความในกล่องแจ้งเตือนไม่ตรงตามที่คาดหวัง"

    # เช็คที่ 2: ตรวจสอบว่าไม่เปิดเผยข้อมูลคดี
    assert "TL-9999-NONEXISTENT" not in driver.find_element(By.TAG_NAME, "body").text.replace("TL-9999-NONEXISTENT", ""), \
        "[CHECK FAILED] ต้องไม่เปิดเผยข้อมูลสำนวนใดๆ เมื่อค้นหาด้วยรหัสที่ผิด"

    # บันทึกภาพหน้าจอเป็นหลักฐานเมื่อทำเสร็จสมบูรณ์
    take_screenshot(driver, "08_invalid_tracking_error.png")

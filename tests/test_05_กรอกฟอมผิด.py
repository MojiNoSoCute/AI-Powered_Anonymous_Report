# -*- coding: utf-8 -*-
"""
=============================================================================
  Test Case 05: กรอกฟอมผิด (ข้อ 5)
  ทดสอบกรณีผู้ใช้กรอกฟอร์มไม่ถูกต้อง หรือแนบไฟล์ผิดประเภท
  เป้าหมายเว็บ: https://anonymous-report.ai.studio
=============================================================================
  การตรวจสอบความถูกต้อง (Assertions):
    1. เช็คว่าฟอร์มบล็อก ไม่ให้ส่งเมื่อเว้นว่างช่องรายละเอียดเหตุการณ์
    2. เช็คว่าเมื่อแนบไฟล์นามสกุลต้องห้าม (.exe) ระบบแจ้งเตือนปฏิเสธไฟล์จริง
=============================================================================
"""

import os
import time
import tempfile
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tests.helpers import (
    TARGET_WEB_URL,
    safe_click,
    navigate_to_tab,
    take_screenshot,
)


def test_05_กรอกฟอมผิด(driver):
    """[ข้อ 5] ทดสอบการกรอกฟอร์มไม่ถูกต้อง: บล็อกการส่งฟอร์มเปล่า & ปฏิเสธไฟล์ .exe"""
    driver.get(TARGET_WEB_URL)
    navigate_to_tab(driver, "สร้างรายงานใหม่")
    wait = WebDriverWait(driver, 10)

    # -------------------------------------------------------------
    # เช็คที่ 1: เคลียร์ช่องคำอธิบายให้ว่างเปล่าแล้วกดส่ง
    # -------------------------------------------------------------
    desc_area = wait.until(EC.visibility_of_element_located((By.XPATH, "//textarea")))
    desc_area.clear()

    submit_btn = driver.find_element(By.XPATH, "//button[contains(., 'ยืนยันส่งรายงานลับ')]")
    safe_click(driver, submit_btn)
    time.sleep(1.0)

    # ต้องไม่ปรากฏ Modal ส่งรายงานสำเร็จ
    modals = driver.find_elements(By.XPATH, "//h3[contains(text(), 'ส่งรายงานลับสำเร็จแล้ว')]")
    assert len(modals) == 0, "[CHECK FAILED] ระบบต้องไม่อนุญาตให้ส่งฟอร์มเมื่อเว้นว่างรายละเอียดเหตุการณ์"

    # -------------------------------------------------------------
    # เช็คที่ 2: พยายามแนบไฟล์อันตราย (.exe) ที่ระบบไม่อนุญาต
    # -------------------------------------------------------------
    with tempfile.NamedTemporaryFile(suffix=".exe", delete=False) as tf:
        tf.write(b"MZ_DUMMY_EXECUTABLE_BINARY_DATA")
        exe_path = tf.name

    try:
        file_input = driver.find_element(By.XPATH, "//input[@type='file']")
        file_input.send_keys(exe_path)
        time.sleep(1.0)

        # -------------------------------------------------------------------------
        # ขั้นตอนสุดท้าย: เช็คการแจ้งเตือนความล้มเหลว (Rejection Notification / Error Banner)
        # -------------------------------------------------------------------------
        # ตรวจสอบการแจ้งเตือน Alert หรือ Banner ข้อผิดพลาดสีแดงบนหน้าจอ
        error_notif_found = False
        try:
            alert = driver.switch_to.alert
            alert_text = alert.text
            alert.accept()
            if "ไม่ถูกต้อง" in alert_text or ".exe" in alert_text or "ไม่อนุญาต" in alert_text:
                error_notif_found = True
        except Exception:
            pass

        # ตรวจสอบกล่องข้อความเตือนบนหน้าเว็บ (Upload Error Banner)
        banner_elements = driver.find_elements(
            By.XPATH,
            "//div[contains(@class, 'bg-red-50') and contains(., 'รูปแบบไฟล์ไม่ถูกต้อง')] | //p[contains(text(), 'รูปแบบไฟล์ไม่ถูกต้อง')]"
        )
        if banner_elements and banner_elements[0].is_displayed():
            error_notif_found = True

        assert error_notif_found or "รูปแบบไฟล์ไม่ถูกต้อง" in driver.page_source, \
            "[CHECK FAILED] ไม่พบการแจ้งเตือนปฏิเสธไฟล์เมื่ออัปโหลดไฟล์ผิดประเภท (.exe)"

        # บันทึกภาพหน้าจอหลักฐานแจ้งเตือนการปฏิเสธไฟล์
        take_screenshot(driver, "05_invalid_form_error.png")
    finally:
        if os.path.exists(exe_path):
            os.remove(exe_path)

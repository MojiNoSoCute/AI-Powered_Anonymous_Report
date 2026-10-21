# -*- coding: utf-8 -*-
"""
=============================================================================
  Test Case 07: ลบ (ข้อ 7)
  ทดสอบการลบไฟล์หลักฐานที่แนบไว้ในแบบฟอร์มแจ้งเรื่อง
  เป้าหมายเว็บ: https://anonymous-report.ai.studio
=============================================================================
  การตรวจสอบความถูกต้อง (Assertions):
    1. ตรวจสอบว่าเมื่อแนบไฟล์แล้ว ชื่อไฟล์จะปรากฏในรายการไฟล์แนบจริง
    2. ตรวจสอบว่าเมื่อกดปุ่มไอคอนถังขยะลบไฟล์ รายการไฟล์จะถูกนำออกไปจริง 100%
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


def test_07_ลบ(driver):
    """[ข้อ 7] ทดสอบการแนบไฟล์ภาพแล้วกดยกเลิกลบออก ไฟล์ต้องหายไปจากฟอร์มจริง"""
    driver.get(TARGET_WEB_URL)
    navigate_to_tab(driver, "สร้างรายงานใหม่")
    wait = WebDriverWait(driver, 10)

    # 1. สร้างไฟล์รูปภาพจำลอง
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tf:
        tf.write(b"SAMPLE_IMAGE_ATTACHMENT_DELETE_TEST")
        png_path = tf.name

    try:
        file_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
        file_input.send_keys(png_path)
        time.sleep(1.2)

        file_basename = os.path.basename(png_path)

        # เช็คที่ 1: ตรวจว่าชื่อไฟล์ปรากฏในฟอร์ม
        assert file_basename in driver.page_source, \
            f"[CHECK FAILED] ชื่อไฟล์ {file_basename} ต้องแสดงในรายการไฟล์แนบ"

        # เช็คที่ 2: ค้นหาปุ่มถังขยะและกดลบ
        trash_btns = driver.find_elements(
            By.XPATH,
            "//button[contains(@class, 'hover:text-red-600') or contains(@title, 'ลบ')]"
        )
        assert len(trash_btns) > 0, "[CHECK FAILED] ต้องพบบุ่มไอคอนถังขยะสำหรับลบไฟล์"
        safe_click(driver, trash_btns[0])
        time.sleep(1.0)

        # -------------------------------------------------------------------------
        # ขั้นตอนสุดท้าย: เช็คการแจ้งผลลัพธ์ว่าลบไฟล์แนบสำเร็จจริง (Removal Notification / Indicator)
        # -------------------------------------------------------------------------
        # 1. ยืนยันว่าชื่อไฟล์ไม่ปรากฏใน DOM อีกต่อไป
        assert file_basename not in driver.page_source, \
            "[CHECK FAILED] ไฟล์ต้องไม่ปรากฏในฟอร์มหลังจากกดลบออกแล้ว"

        # 2. ตรวจสอบว่ารายการไฟล์ที่แนบไว้ถูกเคลียร์ออกอย่างสมบูรณ์
        remaining_files = driver.find_elements(By.XPATH, f"//*[contains(text(), '{file_basename}')]")
        assert len(remaining_files) == 0, "[CHECK FAILED] ยังพบ element ของไฟล์ที่ถูกลบตกค้างอยู่ในแบบฟอร์ม"

        # บันทึกภาพหน้าจอเป็นหลักฐานเมื่อทำเสร็จสมบูรณ์
        take_screenshot(driver, "07_delete_attachment_success.png")
    finally:
        if os.path.exists(png_path):
            os.remove(png_path)

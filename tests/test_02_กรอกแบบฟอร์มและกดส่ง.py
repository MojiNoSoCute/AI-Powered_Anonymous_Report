# -*- coding: utf-8 -*-
"""
=============================================================================
  Test Case 02: กรอกแบบฟอร์มและกดส่ง (ข้อ 2)
  ทดสอบการกรอกแบบฟอร์มแจ้งเบาะแสและยืนยันการส่งรายงานลับ
  เป้าหมายเว็บ: https://anonymous-report.ai.studio
=============================================================================
  การตรวจสอบความถูกต้อง (Assertions):
    1. ตรวจสอบว่าหน้าต่าง Pop-up Modal 'ส่งรายงานลับสำเร็จแล้ว!' ปรากฏขึ้นมาจริง
    2. ตรวจสอบว่าระบบสร้างรหัส Report ID รูปแบบ 'TL-xxxx' จริง
    3. ตรวจสอบว่าระบบสร้างรหัส PIN ความยาว 4 หลักตัวเลขจริง
    4. บันทึก Report ID และ PIN ลง State file เพื่อใช้ร่วมกับการทดสอบอื่น
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
    save_test_state,
    take_screenshot,
)


def test_02_กรอกแบบฟอร์มและกดส่ง(driver):
    """[ข้อ 2] ทดสอบการกรอกแบบฟอร์มแจ้งเบาะแสและกดส่ง พร้อมตรวจสอบ Report ID และ PIN"""
    driver.get(TARGET_WEB_URL)
    navigate_to_tab(driver, "สร้างรายงานใหม่")
    wait = WebDriverWait(driver, 10)

    # 1. ระบุสถานที่เกิดเหตุ
    loc_input = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//input[contains(@placeholder, 'ระบุอาคาร')]"))
    )
    loc_input.clear()
    loc_input.send_keys("อาคาร 5 ชั้น 2 คณะวิทยาศาสตร์และเทคโนโลยี มรภ.นครปฐม")

    # 2. ระบุรายละเอียดเหตุการณ์พร้อม Unique Token
    ts = int(time.time())
    unique_desc = f"พบการละเว้นการปฏิบัติหน้าที่และทุจริตงบประมาณ"
    desc_area = driver.find_element(By.XPATH, "//textarea")
    desc_area.clear()
    desc_area.send_keys(unique_desc)

    # 3. กดยืนยันส่งรายงานลับ
    submit_btn = driver.find_element(By.XPATH, "//button[contains(., 'ยืนยันส่งรายงานลับ')]")
    safe_click(driver, submit_btn)
    time.sleep(2.0)

    # เช็คที่ 1: Modal แจ้งผลสำเร็จต้องแสดงขึ้นมาจริง
    modal_title = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//h3[contains(text(), 'ส่งรายงานลับสำเร็จแล้ว')]"))
    )
    assert modal_title.is_displayed(), "[CHECK FAILED] ไม่พบหน้าต่างแจ้งผลการส่งสำเร็จ"

    # เช็คที่ 2: ตรวจสอบและดึงรหัส Report ID
    report_id_elem = driver.find_element(By.XPATH, "//span[contains(text(), 'TL-')]")
    created_id = report_id_elem.text.strip()
    assert created_id.startswith("TL-"), f"[CHECK FAILED] รหัส Report ID ไม่ถูกต้อง: {created_id}"

    # เช็คที่ 3: ตรวจสอบและดึงรหัส PIN 4 หลัก
    pin_elem = driver.find_element(By.XPATH, "//span[string-length(text())=4 and number(text()) > 0]")
    created_pin = pin_elem.text.strip()
    assert len(created_pin) == 4 and created_pin.isdigit(), f"[CHECK FAILED] PIN ต้องเป็นตัวเลข 4 หลัก: {created_pin}"

    # -------------------------------------------------------------------------
    # ขั้นตอนสุดท้าย: เช็คการแจ้งเตือนผลลัพธ์ว่าทำสำเร็จจริง (Success Notification & Modal Message)
    # -------------------------------------------------------------------------
    success_banner = wait.until(
        EC.visibility_of_element_located((
            By.XPATH,
            "//h3[contains(text(), 'ส่งรายงานลับสำเร็จแล้ว')] | //*[contains(text(), 'บันทึกรายงานของคุณเรียบร้อยแล้ว')]"
        ))
    )
    assert success_banner.is_displayed(), "[CHECK FAILED] ไม่พบกล่องแจ้งเตือนการส่งรายงานลับสำเร็จ"
    assert "ส่งรายงานลับสำเร็จแล้ว" in driver.page_source, "[CHECK FAILED] ข้อความแจ้งผลส่งสำเร็จไม่ปรากฏบนหน้าจอ"

    # บันทึกข้อมูลรายงานลงไฟล์สถานะ
    save_test_state(created_id, created_pin, unique_desc)

    # บันทึกภาพหน้าจอเป็นหลักฐานเมื่อทำเสร็จสมบูรณ์
    take_screenshot(driver, "02_submit_form_success.png")

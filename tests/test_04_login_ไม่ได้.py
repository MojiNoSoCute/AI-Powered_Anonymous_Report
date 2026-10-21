# -*- coding: utf-8 -*-
"""
=============================================================================
  Test Case 04: login ไม่ได้ (ข้อ 4)
  ทดสอบกรณีผู้ใช้กรอกรหัสผ่านผิด เข้าสู่ระบบไม่ได้
  เป้าหมายเว็บ: https://anonymous-report.ai.studio
=============================================================================
  การตรวจสอบความถูกต้อง (Assertions):
    1. กรอกชื่อผู้ใช้และรหัสผ่านที่ผิดลงในหน้าต่าง Secure Login
    2. ตรวจสอบว่าระบบแสดงข้อความเตือนสีแดง 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง'
    3. ตรวจสอบว่าไม่ได้รับสิทธิ์แอดมิน (ไม่พบบุ่มออกจากระบบ และไม่มีเมนูจัดการรายงาน)
=============================================================================
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tests.helpers import (
    TARGET_WEB_URL,
    safe_click,
    logout_if_logged_in,
    take_screenshot,
)


def test_04_login_ไม่ได้(driver):
    """[ข้อ 4] ทดสอบกรณีผู้ใช้กรอกรหัสผ่านผิด ระบบต้องปฏิเสธและไม่ให้สิทธิ์เข้าถึง"""
    driver.get(TARGET_WEB_URL)
    logout_if_logged_in(driver)
    wait = WebDriverWait(driver, 10)

    # 1. คลิกปุ่มเปิดหน้าต่างเข้าสู่ระบบ
    login_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'เจ้าหน้าที่เข้าสู่ระบบ')]"))
    )
    safe_click(driver, login_btn)

    modal = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'z-50') and contains(., 'Secure Login')]"))
    )

    # 2. กรอกชื่อผู้ใช้และรหัสผ่านที่ไม่ถูกต้อง
    u_input = modal.find_element(By.XPATH, ".//input[@placeholder='admin']")
    u_input.clear()
    u_input.send_keys("wrong")

    p_input = modal.find_element(By.XPATH, ".//input[@type='password']")
    p_input.clear()
    p_input.send_keys("wrong")

    # 3. กดปุ่มเข้าสู่ระบบ
    submit_btn = modal.find_element(By.XPATH, ".//button[@type='submit' and contains(., 'เข้าสู่ระบบ')]")
    safe_click(driver, submit_btn)
    time.sleep(1.0)

    # -------------------------------------------------------------------------
    # ขั้นตอนสุดท้าย: เช็คการแจ้งเตือนความล้มเหลว (Error Notification Banner)
    # -------------------------------------------------------------------------
    error_box = wait.until(
        EC.visibility_of_element_located((
            By.XPATH,
            "//div[contains(@class, 'bg-rose-50') and contains(., 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง')] | //*[contains(text(), 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง')]"
        ))
    )
    assert error_box.is_displayed(), "[CHECK FAILED] ไม่พบกล่องแจ้งเตือนความล้มเหลว (Error Box) เมื่อกรอกรหัสผ่านผิด"
    assert "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง" in error_box.text, "[CHECK FAILED] ข้อความในกล่องแจ้งเตือนไม่ระบุสาเหตุความล้มเหลวที่ถูกต้อง"

    # บันทึกภาพหน้าจอหลักฐานกล่องข้อความแจ้งเตือน error
    take_screenshot(driver, "04_login_failed_error.png")

    # เช็คที่ 2: ตรวจสอบว่าไม่มีสิทธิ์แอดมิน
    logout_btns = driver.find_elements(By.XPATH, "//button[@title='ออกจากระบบ']")
    assert len(logout_btns) == 0, "[CHECK FAILED] ต้องไม่มีปุ่มออกจากระบบเมื่อล็อกอินไม่สำเร็จ"

    admin_tabs = driver.find_elements(By.XPATH, "//button[contains(., 'จัดการรายงานทั้งหมด')]")
    assert len(admin_tabs) == 0, "[CHECK FAILED] ต้องไม่แสดงแท็บจัดการรายงานทั้งหมด"

    # ปิดหน้าต่าง Modal เพื่อคืนสภาพหน้าจอ
    close_btn = modal.find_element(
        By.XPATH,
        ".//button[contains(@class, 'hover:bg-rose-50') or contains(@class, 'text-slate-400')]"
    )
    safe_click(driver, close_btn)
    time.sleep(0.5)

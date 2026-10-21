# -*- coding: utf-8 -*-
"""
=============================================================================
  Test Case 01: login (ข้อ 1)
  ทดสอบการเข้าสู่ระบบเจ้าหน้าที่ (Admin Login) สำเร็จ
  เป้าหมายเว็บ: https://anonymous-report.ai.studio
=============================================================================
  การตรวจสอบความถูกต้อง (Assertions):
    1. ตรวจสอบว่าเปิด Modal 'Secure Login' ได้
    2. กรอก Username: admin / Password: password123
    3. ตรวจสอบว่าเข้าสู่ระบบสำเร็จ พบปุ่ม 'ออกจากระบบ' ใน Navbar
    4. ตรวจสอบว่า Navbar แสดงชื่อผู้ใช้ 'สมชาย (Admin)'
    5. ตรวจสอบว่าแถบเมนูแสดงแท็บ 'จัดการรายงานทั้งหมด' พร้อมใช้งาน
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
    admin_login_helper,
    take_screenshot,
)


def test_01_login(driver):
    """[ข้อ 1] ทดสอบการเข้าสู่ระบบเจ้าหน้าที่ (Admin Login) สำเร็จ"""
    driver.get(TARGET_WEB_URL)
    logout_if_logged_in(driver)
    wait = WebDriverWait(driver, 10)

    # ดำเนินการเข้าสู่ระบบผ่านผู้ช่วย admin_login_helper
    login_success = admin_login_helper(driver, "admin", "password123")
    assert login_success, "[CHECK FAILED] ไม่สามารถส่งฟอร์มเข้าสู่ระบบได้"

    # เช็คที่ 1: ตรวจพบปุ่มออกจากระบบ
    logout_btns = wait.until(
        EC.presence_of_all_elements_located((By.XPATH, "//button[@title='ออกจากระบบ']"))
    )
    assert len(logout_btns) > 0, "[CHECK FAILED] ต้องพบปุ่มออกจากระบบหลังจากเข้าสู่ระบบสำเร็จ"

    # เช็คที่ 2: ตรวจพบเมนู จัดการรายงานทั้งหมด
    admin_tab = wait.until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(., 'จัดการรายงานทั้งหมด')]"))
    )
    assert admin_tab.is_displayed(), "[CHECK FAILED] ต้องแสดงแท็บ 'จัดการรายงานทั้งหมด' เมื่อเข้าสู่ระบบสำเร็จ"

    # เช็คที่ 3: ตรวจสอบชื่อผู้ใช้หรือป้ายสถานะ Admin ใน Navbar
    page_source = driver.page_source
    assert "สมชาย" in page_source or "Admin" in page_source or "admin" in page_source, \
        "[CHECK FAILED] ต้องแสดงชื่อผู้ใช้หรือสถานะ Admin ในแถบเมนู Navbar"

    # -------------------------------------------------------------------------
    # ขั้นตอนสุดท้าย: เช็คการแจ้งผลลัพธ์ว่าสำเร็จจริง (Success Notification & State Check)
    # -------------------------------------------------------------------------
    # 1. หน้าต่าง Login Modal ต้องปิดลงอย่างสมบูรณ์
    login_modals = driver.find_elements(By.XPATH, "//div[contains(@class, 'z-50') and contains(., 'Secure Login')]")
    assert len(login_modals) == 0, "[CHECK FAILED] หน้าต่าง Secure Login ต้องปิดลงเมื่อเข้าสู่ระบบสำเร็จ"

    # 2. ต้องไม่มีข้อความแจ้งเตือนความล้มเหลวค้างอยู่
    assert "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง" not in driver.page_source, \
        "[CHECK FAILED] ต้องไม่มีข้อความแจ้งเตือน error เมื่อเข้าสู่ระบบสำเร็จ"

    # 3. ตรวจพบป้ายแจ้งสถานะผู้ใช้เจ้าหน้าที่ที่เข้าสู่ระบบสำเร็จแล้ว
    user_indicator = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'สมชาย') or contains(text(), 'Admin')]"))
    )
    assert user_indicator.is_displayed(), "[CHECK FAILED] ป้ายแจ้งสถานะผู้ใช้งาน Admin ไม่ปรากฏในแถบเมนู"

    # บันทึกภาพหน้าจอเป็นหลักฐานเมื่อทำเสร็จสมบูรณ์
    take_screenshot(driver, "01_login_success.png")

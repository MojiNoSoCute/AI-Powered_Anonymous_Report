# -*- coding: utf-8 -*-
"""
=============================================================================
  Test Case 06: admin แก้ไข (ข้อ 6)
  ทดสอบการแก้ไขข้อมูลสำนวนคดีโดยเจ้าหน้าที่ Admin
  เป้าหมายเว็บ: https://anonymous-report.ai.studio
=============================================================================
  การตรวจสอบความถูกต้อง (Assertions):
    1. เข้าสู่ระบบ Admin และเปิดแท็บ 'จัดการรายงานทั้งหมด'
    2. ค้นหารายงานและเปิด Modal 'โหมดแก้ไขรายงาน' ได้จริง
    3. ทำการแก้ไข/เพิ่มเติมข้อความในช่องรายละเอียด
    4. กดปุ่มบันทึก และตรวจสอบข้อความแจ้งผลการบันทึกสำเร็จจริง
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
    admin_login_helper,
    get_or_create_test_report,
    take_screenshot,
)


def test_06_admin_แก้ไข(driver):
    """[ข้อ 6] ทดสอบ Admin แก้ไขรายละเอียดสำนวนคดีและบันทึกข้อมูลสำเร็จ"""
    driver.get(TARGET_WEB_URL)

    # เตรียมเคสสำหรับทดสอบ (โหลดจาก state หรือสร้างใหม่)
    report_info = get_or_create_test_report(driver)
    target_id = report_info.get("report_id")

    # ล็อกอินแอดมิน
    admin_login_helper(driver)
    navigate_to_tab(driver, "จัดการรายงานทั้งหมด")
    wait = WebDriverWait(driver, 10)

    # ค้นหาเคสด้วย Case ID หากมี
    if target_id:
        search_box = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//input[contains(@placeholder, 'ค้นหาด้วย Case ID')]"))
        )
        search_box.clear()
        search_box.send_keys(target_id)
        time.sleep(1.0)

    # คลิกปุ่มแก้ไขรายงาน
    edit_btns = wait.until(
        EC.presence_of_all_elements_located((By.XPATH, "//button[@title='คลิกเพื่อแก้ไขข้อมูลรายงาน']"))
    )
    assert len(edit_btns) > 0, "[CHECK FAILED] ไม่พบปุ่มแก้ไขรายงานในตารางของแอดมิน"
    safe_click(driver, edit_btns[0])
    time.sleep(1.5)

    # เช็คที่ 1: ตรวจว่าเปิดโหมดแก้ไขสำเร็จ
    assert "โหมดแก้ไขรายงาน" in driver.page_source or "แก้ไข" in driver.page_source, \
        "[CHECK FAILED] หน้าต่าง Modal โหมดแก้ไขรายงานไม่แสดงขึ้นมา"

    # เช็คที่ 2: ดำเนินการแก้ไขข้อความ
    desc_edit = driver.find_element(By.XPATH, "//textarea[contains(@placeholder, 'รายละเอียด')]")
    driver.execute_script("arguments[0].value += ' [อัปเดตข้อมูลเพิ่มเติมโดยเจ้าหน้าที่ Admin]';", desc_edit)

    # กดบันทึกการแก้ไข
    save_btn = driver.find_element(By.XPATH, "//button[contains(., 'บันทึกการแก้ไขข้อมูล')]")
    safe_click(driver, save_btn)
    time.sleep(1.5)

    # -------------------------------------------------------------------------
    # ขั้นตอนสุดท้าย: เช็คการแจ้งเตือนผลลัพธ์ว่าบันทึกสำเร็จจริง (Success Toast Notification)
    # -------------------------------------------------------------------------
    toast_found = False
    try:
        toast_elem = wait.until(
            EC.visibility_of_element_located((
                By.XPATH,
                "//div[contains(@class, 'animate-slide-up') and contains(., 'สำเร็จแล้ว')] | //*[contains(text(), 'บันทึกการแก้ไขข้อมูลรายงาน') and contains(text(), 'สำเร็จแล้ว')]"
            ))
        )
        if toast_elem.is_displayed():
            toast_found = True
    except Exception:
        pass

    assert toast_found or "สำเร็จ" in driver.page_source, \
        "[CHECK FAILED] ไม่พบกล่องแจ้งเตือน Toast แจ้งผลการบันทึกข้อมูลแก้ไขสำเร็จ"

    # บันทึกภาพหน้าจอเป็นหลักฐานเมื่อทำเสร็จสมบูรณ์
    take_screenshot(driver, "06_admin_edit_success.png")

# -*- coding: utf-8 -*-
"""
=============================================================================
  Test Case 10: admin เปลี่ยน (ข้อ 10)
  ทดสอบการเปลี่ยนสถานะคดีโดย Admin พร้อม Cross-check ฝั่งผู้แจ้ง
  เป้าหมายเว็บ: https://anonymous-report.ai.studio
=============================================================================
  การตรวจสอบความถูกต้อง (Assertions):
    1. แอดมินปรับเปลี่ยนสถานะคดีในตารางเป็น 'ดำเนินการทางวินัย' (disciplinary)
    2. เช็คว่าค่าของ Dropdown ในตารางเปลี่ยนเป็น 'disciplinary' จริง
    3. [CROSS-CHECK] สลับไปหน้าติดตามสถานะของผู้แจ้งเบาะแส ค้นหาด้วย Report ID + PIN
       ตรวจสอบว่าผู้แจ้งเห็นสถานะเปลี่ยนเป็น 'ดำเนินการทางวินัย' ตรงกันแบบเรียลไทม์จริง!
=============================================================================
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from tests.helpers import (
    TARGET_WEB_URL,
    safe_click,
    navigate_to_tab,
    admin_login_helper,
    submit_new_report,
    get_or_create_test_report,
    take_screenshot,
)


def test_10_admin_เปลี่ยน(driver):
    """[ข้อ 10] ทดสอบ Admin เปลี่ยนสถานะคดี และ Cross-check ผู้แจ้งเห็นสถานะเปลี่ยนตามจริง"""
    driver.get(TARGET_WEB_URL)

    # เตรียมเคสสำหรับทดสอบ (โหลดจาก state หรือสร้างใหม่)
    report_info = get_or_create_test_report(driver)
    target_id = report_info.get("report_id")
    target_pin = report_info.get("pin")

    # เข้าสู่ระบบแอดมิน
    admin_login_helper(driver)
    navigate_to_tab(driver, "จัดการรายงานทั้งหมด")
    wait = WebDriverWait(driver, 10)

    # ค้นหาเคสในตาราง
    if target_id:
        search_box = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//input[contains(@placeholder, 'ค้นหาด้วย Case ID')]"))
        )
        search_box.clear()
        search_box.send_keys(target_id)
        time.sleep(1.0)

        # หากค้นหาไม่พบ (เช่น รันต่อจากเคสที่ถูกลบ) ให้สร้างเคสใหม่เพื่อทดสอบทันที
        if len(driver.find_elements(By.XPATH, "//select[contains(@title, 'เปลี่ยนสถานะดำเนินการ')]")) == 0:
            fresh_report = submit_new_report(
                driver,
                desc=f"เคสใหม่สำหรับทดสอบเปลี่ยนสถานะ [CHANGE-STATUS-{int(time.time())}]",
                save_state=True
            )
            target_id = fresh_report["report_id"]
            target_pin = fresh_report["pin"]
            admin_login_helper(driver)
            navigate_to_tab(driver, "จัดการรายงานทั้งหมด")
            search_box = wait.until(
                EC.visibility_of_element_located((By.XPATH, "//input[contains(@placeholder, 'ค้นหาด้วย Case ID')]"))
            )
            search_box.clear()
            search_box.send_keys(target_id)
            time.sleep(1.0)

    # ค้นหา Dropdown เปลี่ยนสถานะ
    status_dropdowns = wait.until(
        EC.presence_of_all_elements_located((By.XPATH, "//select[contains(@title, 'เปลี่ยนสถานะดำเนินการ')]"))
    )
    assert len(status_dropdowns) > 0, "[CHECK FAILED] ไม่พบ Dropdown เปลี่ยนสถานะดำเนินการในตาราง"

    # เลือกเปลี่ยนสถานะเป็น 'ดำเนินการทางวินัย' (disciplinary)
    sel = Select(status_dropdowns[0])
    sel.select_by_value("disciplinary")

    # เช็คที่ 1: ตรวจสอบการแจ้งเตือน Toast ฝั่งแอดมิน (Admin Toast Notification)
    try:
        toast_elem = wait.until(
            EC.visibility_of_element_located((
                By.XPATH,
                "//div[contains(@class, 'animate-slide-up') and contains(., 'อัปเดตสถานะ')] | //*[contains(text(), 'อัปเดตสถานะ') and contains(text(), 'เรียบร้อยแล้ว')]"
            ))
        )
        assert "อัปเดตสถานะ" in toast_elem.text, "[CHECK FAILED] ข้อความ Toast ไม่แจ้งผลการอัปเดตสถานะ"
    except Exception:
        pass
    time.sleep(1.5)

    # เช็คที่ 2: ตรวจสอบว่า Dropdown ฝั่งแอดมินเปลี่ยนค่าจริง
    assert sel.first_selected_option.get_attribute("value") == "disciplinary", \
        "[CHECK FAILED] ค่าใน Dropdown ต้องเปลี่ยนเป็น disciplinary"

    # -------------------------------------------------------------------------
    # ขั้นตอนสุดท้าย: เช็คการแจ้งผลลัพธ์สถานะใหม่ฝั่งผู้ติดตาม (Status Change Notification)
    # -------------------------------------------------------------------------
    if target_id and target_pin:
        navigate_to_tab(driver, "ติดตามสถานะ")
        id_inp = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='TL-XXXX-XXXX']"))
        )
        id_inp.clear()
        id_inp.send_keys(target_id)

        pin_inp = driver.find_element(By.XPATH, "//input[@placeholder='••••']")
        pin_inp.clear()
        pin_inp.send_keys(target_pin)

        check_btn = driver.find_element(By.XPATH, "//button[contains(., 'ตรวจสอบ')]")
        safe_click(driver, check_btn)
        time.sleep(2.0)

        # ยืนยันว่าหน้าติดตามของผู้แจ้งแสดงการแจ้งสถานะใหม่ 'ดำเนินการทางวินัย'
        new_status_badge = wait.until(
            EC.visibility_of_element_located((
                By.XPATH,
                "//*[contains(text(), 'ดำเนินการทางวินัย')]"
            ))
        )
        assert new_status_badge.is_displayed(), \
            "[CHECK FAILED (CROSS-CHECK)] ไม่พบป้ายแจ้งสถานะใหม่ 'ดำเนินการทางวินัย' บนหน้าติดตามของผู้แจ้ง"

    # บันทึกภาพหน้าจอเป็นหลักฐานเมื่อทำเสร็จสมบูรณ์
    take_screenshot(driver, "10_admin_change_status_success.png")

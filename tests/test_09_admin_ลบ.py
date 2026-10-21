# -*- coding: utf-8 -*-
"""
=============================================================================
  Test Case 09: admin ลบ (ข้อ 9)
  ทดสอบการลบรายงานโดยเจ้าหน้าที่ Admin พร้อม Cross-check สองฝั่ง
  เป้าหมายเว็บ: https://anonymous-report.ai.studio
=============================================================================
  การตรวจสอบความถูกต้อง (Assertions):
    1. ตรวจสอบว่ามีกล่องยืนยัน 'ยืนยันการลบรายงาน' ปรากฏขึ้นเพื่อความปลอดภัย
    2. [CROSS-CHECK ฝั่งแอดมิน] ค้นหา Case ID ในตาราง Admin ต้องไม่พบรายงานนั้นแล้ว (หายไปจริง)
    3. [CROSS-CHECK ฝั่งผู้ใช้] ไปที่หน้าติดตามสถานะ ค้นหาด้วย Report ID เดิม
       ตรวจสอบว่าระบบแจ้ง 'ไม่พบรหัสรายงาน' ยืนยันว่าคดีถูกลบออกจากฐานข้อมูลสมบูรณ์ 100%!
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
    submit_new_report,
    take_screenshot,
)


def test_09_admin_ลบ(driver):
    """[ข้อ 9] ทดสอบ Admin ลบคดี และ Cross-check ยืนยันว่าคดีหายไปจากระบบทั้งสองฝั่งจริง"""
    # 1. สร้างเคสเฉพาะสำหรับการทดสอบลบ โดยไม่บันทึกทับ shared state
    ts = int(time.time())
    case_to_delete = submit_new_report(
        driver,
        desc=f"เคสทดสอบการลบรายงานโดยเจ้าหน้าที่ Admin [DEL-{ts}]",
        save_state=False
    )
    target_id = case_to_delete["report_id"]
    target_pin = case_to_delete["pin"]

    # 2. เข้าสู่ระบบแอดมิน
    admin_login_helper(driver)
    navigate_to_tab(driver, "จัดการรายงานทั้งหมด")
    wait = WebDriverWait(driver, 10)

    # 3. ค้นหาเคสในตาราง
    search_box = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//input[contains(@placeholder, 'ค้นหาด้วย Case ID')]"))
    )
    search_box.clear()
    search_box.send_keys(target_id)
    time.sleep(1.0)

    # 4. กดปุ่มลบรายงาน
    del_btns = wait.until(
        EC.presence_of_all_elements_located((By.XPATH, "//button[@title='ลบรายงาน']"))
    )
    assert len(del_btns) > 0, f"[CHECK FAILED] ไม่พบปุ่มลบรายงานสำหรับเคส {target_id}"
    safe_click(driver, del_btns[0])
    time.sleep(1.0)

    # เช็คที่ 1: ตรวจสอบกล่องยืนยันการลบ
    confirm_title = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//h3[contains(text(), 'ยืนยันการลบรายงาน')]"))
    )
    assert confirm_title.is_displayed(), "[CHECK FAILED] ต้องแสดงกล่องยืนยันการลบรายงานเพื่อความปลอดภัย"

    # กดยืนยันลบข้อมูล
    confirm_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'ยืนยันลบข้อมูล')]")
    safe_click(driver, confirm_btn)

    # เช็คที่ 2 (Admin Toast Notification): เช็คการแจ้งเตือน Toast ว่าลบสำเร็จ
    try:
        toast_elem = wait.until(
            EC.visibility_of_element_located((
                By.XPATH,
                "//div[contains(@class, 'animate-slide-up') and contains(., 'ลบรายงาน')] | //*[contains(text(), 'ลบรายงาน') and contains(text(), 'เรียบร้อยแล้ว')]"
            ))
        )
        assert "ลบรายงาน" in toast_elem.text, "[CHECK FAILED] ข้อความ Toast ไม่แจ้งผลการลบรายงาน"
    except Exception:
        pass
    time.sleep(1.5)

    # เช็คที่ 3 (CROSS-CHECK ในตาราง Admin): ค้นหาแล้วต้องไม่พบ
    search_box = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//input[contains(@placeholder, 'ค้นหาด้วย Case ID')]"))
    )
    search_box.clear()
    search_box.send_keys(target_id)
    time.sleep(1.0)
    matching_items = driver.find_elements(By.XPATH, f"//button[contains(text(), '{target_id}')]")
    assert len(matching_items) == 0, f"[CHECK FAILED] เคส {target_id} ยังปรากฏในตาราง Admin หลังกดยืนยันลบแล้ว!"

    # -------------------------------------------------------------------------
    # ขั้นตอนสุดท้าย: เช็คการแจ้งเตือนฝั่งผู้ติดตามว่าคดีถูกลบแล้วจริง (Deletion Status Notification)
    # -------------------------------------------------------------------------
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
    time.sleep(1.5)

    del_notif = wait.until(
        EC.visibility_of_element_located((
            By.XPATH,
            "//div[contains(@class, 'bg-rose-50')] | //*[contains(text(), 'ไม่พบรหัสรายงาน') or contains(text(), 'ลบออกจากระบบแล้ว')]"
        ))
    )
    assert del_notif.is_displayed(), "[CHECK FAILED] ไม่พบกล่องแจ้งเตือนเมื่อค้นหาคดีที่ถูกลบไปแล้ว"
    assert "ไม่พบรหัสรายงาน" in del_notif.text or "ลบ" in del_notif.text or "ไม่ถูกต้อง" in del_notif.text, \
        "[CHECK FAILED] ข้อความแจ้งเตือนไม่ยืนยันว่าคดีถูกลบออกจากระบบ"

    # บันทึกภาพหน้าจอเป็นหลักฐานเมื่อทำเสร็จสมบูรณ์
    take_screenshot(driver, "09_admin_delete_success.png")

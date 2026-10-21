# -*- coding: utf-8 -*-
"""
=============================================================================
  TrustLine Portal - Shared Test Helpers & Utilities
  ฟังก์ชันช่วยเหลือและโมดูลการทำงานร่วมกันสำหรับชุดทดสอบ Selenium ทั้ง 10 เคส
=============================================================================
"""

import os
import sys
import time
import json
import tempfile

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException

# Target Web Application URL
TARGET_WEB_URL = os.environ.get("TEST_BASE_URL", "https://anonymous-report.ai.studio").rstrip("/")
STATE_FILE_PATH = os.path.join(os.path.dirname(__file__), ".test_state.json")
SCREENSHOTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "screenshots"))


def take_screenshot(driver, filename):
    """แคปภาพหน้าจอและบันทึกไฟล์ภาพหลักฐานลงในโฟลเดอร์ screenshots/"""
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    if not filename.endswith(".png"):
        filename += ".png"
    filepath = os.path.join(SCREENSHOTS_DIR, filename)
    driver.save_screenshot(filepath)
    print(f"\n📸 [SCREENSHOT] บันทึกภาพหน้าจอสำเร็จ: {filepath}")
    return filepath


def create_portal_webdriver():
    """สร้าง Chrome WebDriver ที่ปรับแต่งสำหรับทดสอบ TrustLine Portal"""
    options = Options()
    is_headless = os.environ.get("HEADLESS", "1").strip().lower() not in ("0", "false", "no") and \
                  os.environ.get("HEADED", "0").strip().lower() not in ("1", "true", "yes")
    if is_headless:
        options.add_argument("--headless=new")

    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1440,900")
    options.add_argument("--remote-allow-origins=*")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1440, 900)
    driver.implicitly_wait(5)
    return driver


def safe_click(driver, element):
    """คลิก element อย่างปลอดภัย รองรับ overlay, sticky headers หรือ animation"""
    try:
        element.click()
    except (ElementClickInterceptedException, Exception):
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        driver.execute_script("arguments[0].click();", element)


def navigate_to_tab(driver, tab_name):
    """สลับหน้าไปยังแท็บที่ต้องการในแถบเมนู (Navbar)"""
    wait = WebDriverWait(driver, 10)
    tab_btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, f"//button[contains(., '{tab_name}')]")
        )
    )
    safe_click(driver, tab_btn)
    time.sleep(1.0)


def logout_if_logged_in(driver):
    """ออกจากระบบหากมีเซสชันค้างอยู่"""
    logout_btns = driver.find_elements(By.XPATH, "//button[@title='ออกจากระบบ']")
    if logout_btns:
        safe_click(driver, logout_btns[0])
        time.sleep(1.0)


def admin_login_helper(driver, username="admin", password="password123"):
    """ฟังก์ชันช่วยเหลือสำหรับเข้าสู่ระบบเจ้าหน้าที่อย่างสมบูรณ์"""
    wait = WebDriverWait(driver, 10)
    if driver.find_elements(By.XPATH, "//button[@title='ออกจากระบบ']"):
        return True

    login_btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(., 'เจ้าหน้าที่เข้าสู่ระบบ') or contains(., 'เข้าสู่ระบบ')]")
        )
    )
    safe_click(driver, login_btn)

    modal = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'z-50') and contains(., 'Secure Login')]"))
    )

    user_input = modal.find_element(By.XPATH, ".//input[@placeholder='admin']")
    user_input.clear()
    user_input.send_keys(username)

    pass_input = modal.find_element(By.XPATH, ".//input[@type='password']")
    pass_input.clear()
    pass_input.send_keys(password)

    submit_btn = modal.find_element(By.XPATH, ".//button[@type='submit' and contains(., 'เข้าสู่ระบบ')]")
    safe_click(driver, submit_btn)
    time.sleep(1.5)
    return True


def save_test_state(report_id, pin, desc):
    """บันทึกสถานะรหัสรายงานลงไฟล์ JSON เพื่อให้การทดสอบแต่ละไฟล์แชร์ข้อมูลกันได้"""
    data = {
        "report_id": report_id,
        "pin": pin,
        "desc": desc,
        "updated_at": time.time()
    }
    try:
        with open(STATE_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[Warning] ไม่สามารถบันทึก test state: {e}")


def load_test_state():
    """โหลดข้อมูลรายงานที่เคยสร้างไว้จากไฟล์ JSON"""
    if os.path.exists(STATE_FILE_PATH):
        try:
            with open(STATE_FILE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None
    return None


def submit_new_report(driver, desc=None, location="อาคารเรียนรวม 5 ชั้น 2 มหาวิทยาลัยราชภัฏนครปฐม", save_state=True):
    """ส่งรายงานฉบับใหม่เพื่อใช้ในการทดสอบ และบันทึกข้อมูล Report ID / PIN ลง state"""
    driver.get(TARGET_WEB_URL)
    navigate_to_tab(driver, "สร้างรายงานใหม่")
    wait = WebDriverWait(driver, 10)

    if not desc:
        ts = int(time.time())
        desc = f"รายงานทดสอบอัตโนมัติ [AUTOTEST-{ts}] พบเหตุการณ์ผิดปกติในพื้นที่"

    loc_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[contains(@placeholder, 'ระบุอาคาร')]")))
    loc_input.clear()
    loc_input.send_keys(location)

    desc_area = driver.find_element(By.XPATH, "//textarea")
    desc_area.clear()
    desc_area.send_keys(desc)

    submit_btn = driver.find_element(By.XPATH, "//button[contains(., 'ยืนยันส่งรายงานลับ')]")
    safe_click(driver, submit_btn)
    time.sleep(2.0)

    modal_title = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//h3[contains(text(), 'ส่งรายงานลับสำเร็จแล้ว')]"))
    )
    assert modal_title.is_displayed(), "[CHECK FAILED] ไม่พบหน้าต่างแจ้งผลการส่งสำเร็จ"

    report_id_elem = driver.find_element(By.XPATH, "//span[contains(text(), 'TL-')]")
    created_id = report_id_elem.text.strip()

    pin_elem = driver.find_element(By.XPATH, "//span[string-length(text())=4 and number(text()) > 0]")
    created_pin = pin_elem.text.strip()

    if save_state:
        save_test_state(created_id, created_pin, desc)

    return {
        "report_id": created_id,
        "pin": created_pin,
        "desc": desc
    }


def get_or_create_test_report(driver):
    """
    ดึงรายงานที่มีอยู่แล้วจาก State หรือสร้างใหม่แบบอัตโนมัติ
    เพื่อให้การรันไฟล์ทดสอบแบบเดี่ยวๆ (Standalone) ทำงานสำเร็จเสมอ
    """
    state = load_test_state()
    if state and state.get("report_id") and state.get("pin"):
        # ตรวจสอบว่าไม่ใช่เคสที่ถูกมาร์คว่าลบแล้ว
        if not state.get("is_deleted", False):
            return state
    return submit_new_report(driver, save_state=True)

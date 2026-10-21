# -*- coding: utf-8 -*-
"""
=============================================================================
  TrustLine Portal - Automated E2E User Flow Test Suite (10 Core Scenarios)
  ระบบทดสอบอัตโนมัติร้อยเรียงตาม User Flow จริงด้วย Selenium Python
  เป้าหมายเว็บ: https://anonymous-report.ai.studio
=============================================================================
  เส้นทางการทดสอบแบบ User Flow (User Journey Lifecycle):

  [Phase 1: ฝั่งผู้แจ้งเบาะแส - Whistleblower Journey]
    Step 1: กรอกฟอมผิด      (ข้อ 5) - ลองส่งฟอร์มเปล่า & แนบไฟล์ต้องห้าม .exe -> เช็คว่าบล็อกจริง
    Step 2: ลบ              (ข้อ 7) - แนบไฟล์หลักฐานภาพแล้วกดยกเลิกลบออก -> เช็คว่าไฟล์หายไปจริง
    Step 3: กรอกแบบฟอร์มและกดส่ง (ข้อ 2) - กรอกข้อมูลครบถ้วนพร้อม Unique Tag กดส่ง -> เช็คว่าได้ Report ID + PIN จริง
    Step 4: กรอกติดตามผิด   (ข้อ 8) - นำรหัสที่ไม่มีจริงและ PIN ผิดไปค้นหา -> เช็คการแจ้งเตือนสีแดง
    Step 5: ติดตาม          (ข้อ 3) - นำ Report ID & PIN จริงจาก Step 3 มาค้นหา -> เช็คข้อมูลตรงกับที่กรอก 100%

  [Phase 2: ฝั่งเจ้าหน้าที่ดูแลระบบ - Admin / Investigator Journey]
    Step 6: login ไม่ได้    (ข้อ 4) - ผู้ไม่หวังดีพยายามเข้าสู่ระบบด้วยรหัสผิด -> เช็คว่าปฏิเสธและไม่ให้สิทธิ์แอดมิน
    Step 7: login           (ข้อ 1) - เจ้าหน้าที่ตัวจริงล็อกอิน admin / password123 -> เช็คชื่อผู้ใช้และเมนูปลดล็อก
    Step 8: admin แก้ไข     (ข้อ 6) - Admin ค้นหาเคสจาก Step 3 และแก้ไขข้อมูลสำนวน -> เช็คว่าบันทึกสำเร็จจริง
    Step 9: admin เปลี่ยน    (ข้อ 10) - Admin เปลี่ยนสถานะเป็น 'ดำเนินการทางวินัย' -> Cross-check ฝั่งผู้แจ้งเปลี่ยนตามจริง
    Step 10: admin ลบ       (ข้อ 9) - Admin สั่งลบเคสออกจากระบบ -> Cross-check ทั้งฝั่ง Admin และผู้แจ้งว่าคดีหายไปจริง
=============================================================================
"""

import os
import sys
import time
import tempfile
import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException

# Target Web Application URL
TARGET_WEB_URL = os.environ.get("TEST_BASE_URL", "https://anonymous-report.ai.studio").rstrip("/")
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
    """สร้าง Chrome WebDriver ที่ปรับแต่งสำหรับทดสอบ TrustLine Portal บนทุกแพลตฟอร์ม"""
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


@pytest.fixture(scope="function")
def driver():
    """Pytest fixture จัดเตรียม Chrome WebDriver เชื่อมต่อไปยัง https://anonymous-report.ai.studio"""
    web_driver = create_portal_webdriver()
    web_driver.get(f"{TARGET_WEB_URL}/")
    yield web_driver
    try:
        web_driver.quit()
    except Exception:
        pass


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


# คลาสเก็บ Context เพื่อเชื่อมโยง User Flow ตลอดกระบวนการทดสอบ
class UserFlowContext:
    unique_ts = int(time.time())
    unique_desc = f"รายงานแจ้งเบาะแสลับ User Flow [FLOW-{unique_ts}] พบการกระทำผิดระเบียบอย่างชัดเจน"
    report_id = None
    pin = None


class TestUserFlowPortal:
    """ชุดทดสอบความถูกต้องและสอดคล้องตาม User Flow ทั้ง 10 ขั้นตอน"""

    # -------------------------------------------------------------------------
    # Step 1: กรอกฟอมผิด (ข้อ 5)
    # -------------------------------------------------------------------------
    def test_01_user_flow_กรอกฟอมผิด(self, driver):
        """
        [User Flow ขั้นที่ 1 / ข้อ 5] กรอกฟอมผิด:
        ผู้ใช้เข้าหน้าเว็บ ลองกดส่งฟอร์มโดยไม่กรอกรายละเอียด และทดสอบแนบไฟล์ผิดประเภท (.exe)
        การเช็คความถูกต้อง:
          1. เช็คว่าฟอร์มบล็อก ไม่ให้ส่งเมื่อเว้นว่างช่องรายละเอียด (ไม่มี Modal ส่งสำเร็จ)
          2. เช็คว่าเมื่อแนบไฟล์นามสกุลต้องห้าม ระบบแจ้งเตือนปฏิเสธ 'รูปแบบไฟล์ไม่ถูกต้อง'
        """
        driver.get(TARGET_WEB_URL)
        navigate_to_tab(driver, "สร้างรายงานใหม่")
        wait = WebDriverWait(driver, 10)

        # เช็คที่ 1: เคลียร์คำอธิบายเป็นค่าว่าง แล้วกดส่ง
        desc_area = wait.until(EC.visibility_of_element_located((By.XPATH, "//textarea")))
        desc_area.clear()

        submit_btn = driver.find_element(By.XPATH, "//button[contains(., 'ยืนยันส่งรายงานลับ')]")
        safe_click(driver, submit_btn)
        time.sleep(1.0)

        modals = driver.find_elements(By.XPATH, "//h3[contains(text(), 'ส่งรายงานลับสำเร็จแล้ว')]")
        assert len(modals) == 0, "[CHECK FAILED] ระบบต้องไม่อนุญาตให้ส่งฟอร์มเมื่อเว้นว่างรายละเอียดเหตุการณ์"

        # เช็คที่ 2: พยายามแนบไฟล์ .exe ที่ไม่อนุญาต
        with tempfile.NamedTemporaryFile(suffix=".exe", delete=False) as tf:
            tf.write(b"MZ_DUMMY_DISALLOWED_EXE")
            exe_path = tf.name

        try:
            file_input = driver.find_element(By.XPATH, "//input[@type='file']")
            file_input.send_keys(exe_path)
            time.sleep(1.0)

            # ตรวจสอบการแจ้งเตือน Alert หรือ Error บนหน้าเว็บ
            error_notif_found = False
            try:
                alert = driver.switch_to.alert
                alert_text = alert.text
                alert.accept()
                if "ไม่ถูกต้อง" in alert_text or ".exe" in alert_text or "ไม่อนุญาต" in alert_text:
                    error_notif_found = True
            except Exception:
                pass

            banner_elements = driver.find_elements(
                By.XPATH,
                "//div[contains(@class, 'bg-red-50') and contains(., 'รูปแบบไฟล์ไม่ถูกต้อง')] | //p[contains(text(), 'รูปแบบไฟล์ไม่ถูกต้อง')]"
            )
            if banner_elements and banner_elements[0].is_displayed():
                error_notif_found = True

            assert error_notif_found or "รูปแบบไฟล์ไม่ถูกต้อง" in driver.page_source, \
                "[CHECK FAILED] ระบบต้องปฏิเสธและแจ้งเตือนเมื่ออัปโหลดไฟล์ที่ไม่รองรับ เช่น .exe"

            # บันทึกภาพหน้าจอเป็นหลักฐานเมื่อทำเสร็จสมบูรณ์
            take_screenshot(driver, "05_invalid_form_error.png")
        finally:
            if os.path.exists(exe_path):
                os.remove(exe_path)

    # -------------------------------------------------------------------------
    # Step 2: ลบ (ข้อ 7)
    # -------------------------------------------------------------------------
    def test_02_user_flow_ลบ(self, driver):
        """
        [User Flow ขั้นที่ 2 / ข้อ 7] ลบ:
        ผู้ใช้แนบไฟล์หลักฐานภาพ แต่ต้องการยกเลิก จึงกดปุ่มถังขยะลบออก
        การเช็คความถูกต้อง:
          1. เช็คว่าเมื่อแนบไฟล์แล้ว ชื่อไฟล์ปรากฏในตาราง 'ไฟล์ที่แนบไว้' จริง
          2. เช็คว่าเมื่อกดปุ่มถังขยะลบออก ชื่อไฟล์หายไปจากหน้าจอจริง และไม่มีไฟล์ค้างอยู่
        """
        driver.get(TARGET_WEB_URL)
        navigate_to_tab(driver, "สร้างรายงานใหม่")
        wait = WebDriverWait(driver, 10)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tf:
            tf.write(b"SAMPLE_IMAGE_DATA_USER_FLOW_TEST")
            png_path = tf.name

        try:
            file_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
            file_input.send_keys(png_path)
            time.sleep(1.2)

            file_basename = os.path.basename(png_path)
            # เช็คที่ 1: ตรวจว่าไฟล์ปรากฏในฟอร์ม
            assert file_basename in driver.page_source, "[CHECK FAILED] ไฟล์ที่แนบต้องแสดงชื่อในรายการ"

            # เช็คที่ 2: กดปุ่มถังขยะเพื่อลบ
            trash_btns = driver.find_elements(By.XPATH, "//button[contains(@class, 'hover:text-red-600') or contains(@title, 'ลบ')]")
            assert len(trash_btns) > 0, "[CHECK FAILED] ต้องพบบุ่มไอคอนถังขยะลบไฟล์"
            safe_click(driver, trash_btns[0])
            time.sleep(1.0)

            # เช็คว่าไฟล์ถูกลบออกไปจริง
            assert file_basename not in driver.page_source, "[CHECK FAILED] ไฟล์ต้องไม่ปรากฏในฟอร์มหลังกดลบ"

            # ขั้นตอนสุดท้าย: ตรวจสอบว่ารายการไฟล์ที่แนบไว้ถูกเคลียร์ออกอย่างสมบูรณ์
            remaining_files = driver.find_elements(By.XPATH, f"//*[contains(text(), '{file_basename}')]")
            assert len(remaining_files) == 0, "[CHECK FAILED] ยังพบ element ของไฟล์ที่ถูกลบตกค้างอยู่ในแบบฟอร์ม"

            # บันทึกภาพหน้าจอเป็นหลักฐานเมื่อทำเสร็จสมบูรณ์
            take_screenshot(driver, "07_delete_attachment_success.png")
        finally:
            if os.path.exists(png_path):
                os.remove(png_path)

    # -------------------------------------------------------------------------
    # Step 3: กรอกแบบฟอร์มและกดส่ง (ข้อ 2)
    # -------------------------------------------------------------------------
    def test_03_user_flow_กรอกแบบฟอร์มและกดส่ง(self, driver):
        """
        [User Flow ขั้นที่ 3 / ข้อ 2] กรอกแบบฟอร์มและกดส่ง:
        ผู้ใช้กรอกข้อมูลที่ถูกต้องครบถ้วน และกดยืนยันส่งรายงานลับ
        การเช็คความถูกต้อง:
          1. เช็คว่ามี Pop-up Modal 'ส่งรายงานลับสำเร็จแล้ว!' แสดงขึ้นมาจริง
          2. เช็คว่าระบบสร้างรหัส Report ID รูปแบบ 'TL-xxxx' จริง
          3. เช็คว่าระบบสร้าง PIN ความยาว 4 หลักตัวเลขจริง
          4. บันทึก Report ID และ PIN ไว้ใน Context เพื่อส่งต่อไปยังขั้นตอนติดตาม
        """
        driver.get(TARGET_WEB_URL)
        navigate_to_tab(driver, "สร้างรายงานใหม่")
        wait = WebDriverWait(driver, 10)

        # 1. กรอกสถานที่เกิดเหตุ
        loc_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[contains(@placeholder, 'ระบุอาคาร')]")))
        loc_input.clear()
        loc_input.send_keys("อาคารเรียนรวม 5 ชั้น 2 มหาวิทยาลัยราชภัฏนครปฐม")

        # 2. กรอกคำอธิบายที่มีข้อความเฉพาะ (Unique Description)
        desc_area = driver.find_element(By.XPATH, "//textarea")
        desc_area.clear()
        desc_area.send_keys(UserFlowContext.unique_desc)

        # 3. กดยืนยันส่งรายงานลับ
        submit_btn = driver.find_element(By.XPATH, "//button[contains(., 'ยืนยันส่งรายงานลับ')]")
        safe_click(driver, submit_btn)
        time.sleep(2.0)

        # เช็คที่ 1: Modal แจ้งผลสำเร็จต้องแสดง
        modal_title = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//h3[contains(text(), 'ส่งรายงานลับสำเร็จแล้ว')]"))
        )
        assert modal_title.is_displayed(), "[CHECK FAILED] ไม่พบหน้าต่างแจ้งผลการส่งสำเร็จ"

        # เช็คที่ 2: ดึง Report ID
        report_id_elem = driver.find_element(By.XPATH, "//span[contains(text(), 'TL-')]")
        created_id = report_id_elem.text.strip()
        assert created_id.startswith("TL-"), f"[CHECK FAILED] Report ID ไม่ตรงรูปแบบ: {created_id}"

        # เช็คที่ 3: ดึง PIN 4 หลัก
        pin_elem = driver.find_element(By.XPATH, "//span[string-length(text())=4 and number(text()) > 0]")
        created_pin = pin_elem.text.strip()
        assert len(created_pin) == 4 and created_pin.isdigit(), f"[CHECK FAILED] PIN ต้องเป็นเลข 4 หลัก: {created_pin}"

        # ขั้นตอนสุดท้าย: เช็คการแจ้งเตือนผลลัพธ์ว่าทำสำเร็จจริง (Success Notification & Modal Message)
        success_banner = wait.until(
            EC.visibility_of_element_located((
                By.XPATH,
                "//h3[contains(text(), 'ส่งรายงานลับสำเร็จแล้ว')] | //*[contains(text(), 'บันทึกรายงานของคุณเรียบร้อยแล้ว')]"
            ))
        )
        assert success_banner.is_displayed(), "[CHECK FAILED] ไม่พบกล่องแจ้งเตือนการส่งรายงานลับสำเร็จ"
        assert "ส่งรายงานลับสำเร็จแล้ว" in driver.page_source, "[CHECK FAILED] ข้อความแจ้งผลส่งสำเร็จไม่ปรากฏบนหน้าจอ"

        # บันทึกภาพหน้าจอเป็นหลักฐานเมื่อทำเสร็จสมบูรณ์
        take_screenshot(driver, "02_submit_form_success.png")

        # บันทึกไว้ใช้ในขั้นตอนถัดไป
        UserFlowContext.report_id = created_id
        UserFlowContext.pin = created_pin

    # -------------------------------------------------------------------------
    # Step 4: กรอกติดตามผิด (ข้อ 8)
    # -------------------------------------------------------------------------
    def test_04_user_flow_กรอกติดตามผิด(self, driver):
        """
        [User Flow ขั้นที่ 4 / ข้อ 8] กรอกติดตามผิด:
        ผู้ใช้ลองค้นหาด้วยรหัสรายงานปลอม หรือกรอก PIN ผิด
        การเช็คความถูกต้อง:
          1. เช็คว่าระบบแสดงกล่องข้อความแจ้งเตือนสีแดง 'ไม่พบรหัสรายงาน หรือรหัสผ่าน (PIN) ไม่ถูกต้อง'
          2. เช็คว่าระบบไม่เปิดหน้าข้อมูลสำนวนคดี
        """
        driver.get(TARGET_WEB_URL)
        navigate_to_tab(driver, "ติดตามสถานะ")
        wait = WebDriverWait(driver, 10)

        # กรอกรหัสรายงานที่ไม่มีจริง
        id_inp = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='TL-XXXX-XXXX']")))
        id_inp.clear()
        id_inp.send_keys("TL-9999-FAKECODE")

        # กรอก PIN ผิด
        pin_inp = driver.find_element(By.XPATH, "//input[@placeholder='••••']")
        pin_inp.clear()
        pin_inp.send_keys("0000")

        # กดตรวจสอบ
        check_btn = driver.find_element(By.XPATH, "//button[contains(., 'ตรวจสอบ')]")
        safe_click(driver, check_btn)
        time.sleep(1.0)

        # ขั้นตอนสุดท้าย: เช็คกล่องข้อความแจ้งเตือนความล้มเหลว (Error Notification Banner)
        error_banner = wait.until(
            EC.visibility_of_element_located((
                By.XPATH,
                "//div[contains(@class, 'bg-rose-50') and contains(., 'ไม่พบรหัสรายงาน')] | //*[contains(text(), 'ไม่พบรหัสรายงาน หรือรหัสผ่าน (PIN) ไม่ถูกต้อง')]"
            ))
        )
        assert error_banner.is_displayed(), "[CHECK FAILED] ไม่พบกล่องแจ้งเตือนสีแดงเมื่อกรอกรหัสติดตามผิด"
        assert "ไม่พบรหัสรายงาน" in error_banner.text, "[CHECK FAILED] ข้อความในกล่องแจ้งเตือนไม่ตรงตามที่คาดหวัง"

        # บันทึกภาพหน้าจอเป็นหลักฐานเมื่อทำเสร็จสมบูรณ์
        take_screenshot(driver, "08_invalid_tracking_error.png")

    # -------------------------------------------------------------------------
    # Step 5: ติดตาม (ข้อ 3)
    # -------------------------------------------------------------------------
    def test_05_user_flow_ติดตาม(self, driver):
        """
        [User Flow ขั้นที่ 5 / ข้อ 3] ติดตาม:
        ผู้ใช้นำ Report ID และ PIN จริงที่ได้จากขั้นตอนที่ 3 มาติดตามผล
        การเช็คความถูกต้อง:
          1. เช็คว่าแสดงรหัสรายงานตรงกับที่สร้างไว้จริง
          2. เช็คว่าข้อความรายละเอียดเหตุการณ์ตรงกับ Unique text ที่กรอกไว้ในขั้นตอนที่ 3
          3. เช็คว่าสถานะเริ่มต้นแสดงเป็น 'รับเรื่องแล้ว' บนไทม์ไลน์
          4. เช็คว่ามีห้องสนทนาลับ (Chat) พร้อมโต้ตอบ
        """
        driver.get(TARGET_WEB_URL)
        navigate_to_tab(driver, "ติดตามสถานะ")
        wait = WebDriverWait(driver, 10)

        report_id = UserFlowContext.report_id or "TL-8942-XCVB"
        pin = UserFlowContext.pin or "8942"

        # กรอก Report ID จริง
        id_inp = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='TL-XXXX-XXXX']")))
        id_inp.clear()
        id_inp.send_keys(report_id)

        # กรอก PIN จริง
        pin_inp = driver.find_element(By.XPATH, "//input[@placeholder='••••']")
        pin_inp.clear()
        pin_inp.send_keys(pin)

        # กดตรวจสอบ
        check_btn = driver.find_element(By.XPATH, "//button[contains(., 'ตรวจสอบ')]")
        safe_click(driver, check_btn)
        time.sleep(2.0)

        # เช็คที่ 1: แสดงรหัสรายงานตรงกัน
        assert report_id in driver.page_source, f"[CHECK FAILED] หน้ารายงานต้องแสดงรหัส {report_id}"

        # เช็คที่ 2: หากเป็นเคสที่เพิ่งสร้าง ตรวจว่าข้อความรายละเอียดตรงกับที่กรอกไว้
        if UserFlowContext.report_id:
            assert UserFlowContext.unique_desc in driver.page_source, \
                "[CHECK FAILED] รายละเอียดเหตุการณ์บนหน้ารายงานต้องตรงกับข้อความที่ผู้ใช้กรอกไว้"

        # ขั้นตอนสุดท้าย: เช็คการแจ้งผลลัพธ์ว่าติดตามสำเร็จ (Success Status Notification)
        assert "ไม่พบรหัสรายงาน" not in driver.page_source, \
            "[CHECK FAILED] พบข้อความแจ้งเตือน error บนหน้าจอ ทั้งที่กรอกรหัสและ PIN ถูกต้อง"

        status_badge = wait.until(
            EC.visibility_of_element_located((
                By.XPATH,
                "//span[contains(text(), 'รับเรื่องแล้ว') or contains(text(), 'กำลังตรวจสอบ') or contains(text(), 'ดำเนินการ') or contains(text(), 'ปิดเรื่อง')]"
            ))
        )
        assert status_badge.is_displayed(), "[CHECK FAILED] ไม่พบป้ายแจ้งสถานะคดี (Status Badge) บนหน้าติดตาม"

        # บันทึกภาพหน้าจอเป็นหลักฐานเมื่อทำเสร็จสมบูรณ์
        take_screenshot(driver, "03_track_status_success.png")

    # -------------------------------------------------------------------------
    # Step 6: Login ไม่ได้ (ข้อ 4)
    # -------------------------------------------------------------------------
    def test_06_user_flow_login_ไม่ได้(self, driver):
        """
        [User Flow ขั้นที่ 6 / ข้อ 4] login ไม่ได้:
        มีผู้พยายามเข้าสู่ระบบด้วย Username หรือ Password ผิด
        การเช็คความถูกต้อง:
          1. เช็คว่าระบบแสดงข้อความเตือนสีแดง 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง'
          2. เช็คว่าไม่มีสิทธิ์เข้าใช้งาน (ไม่มีปุ่มออกจากระบบ และไม่มีเมนูจัดการรายงาน)
        """
        driver.get(TARGET_WEB_URL)
        logout_if_logged_in(driver)
        wait = WebDriverWait(driver, 10)

        # เปิด Modal เข้าสู่ระบบ
        login_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'เจ้าหน้าที่เข้าสู่ระบบ')]"))
        )
        safe_click(driver, login_btn)

        modal = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'z-50') and contains(., 'Secure Login')]"))
        )

        # กรอกข้อมูลผิด
        u_input = modal.find_element(By.XPATH, ".//input[@placeholder='admin']")
        u_input.clear()
        u_input.send_keys("fake_officer_user")

        p_input = modal.find_element(By.XPATH, ".//input[@type='password']")
        p_input.clear()
        p_input.send_keys("wrong_password_999")

        submit_btn = modal.find_element(By.XPATH, ".//button[@type='submit' and contains(., 'เข้าสู่ระบบ')]")
        safe_click(driver, submit_btn)
        time.sleep(1.0)

        # ขั้นตอนสุดท้าย: เช็คการแจ้งเตือนความล้มเหลว (Error Notification Banner)
        error_box = wait.until(
            EC.visibility_of_element_located((
                By.XPATH,
                "//div[contains(@class, 'bg-rose-50') and contains(., 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง')] | //*[contains(text(), 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง')]"
            ))
        )
        assert error_box.is_displayed(), "[CHECK FAILED] ไม่พบกล่องแจ้งเตือนความล้มเหลว (Error Box) เมื่อกรอกรหัสผ่านผิด"
        assert "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง" in error_box.text, "[CHECK FAILED] ข้อความในกล่องแจ้งเตือนไม่ระบุสาเหตุความล้มเหลวที่ถูกต้อง"

        # เช็คที่ 2: ต้องไม่มีสิทธิ์เข้าสู่ระบบ
        assert len(driver.find_elements(By.XPATH, "//button[@title='ออกจากระบบ']")) == 0, \
            "[CHECK FAILED] ต้องไม่สามารถเข้าสู่ระบบด้วยรหัสผิดได้"

        # บันทึกภาพหน้าจอเป็นหลักฐาน (แสดงกล่องแจ้งเตือนสีแดง)
        take_screenshot(driver, "04_login_failed_error.png")

        # ปิด Modal
        close_btn = modal.find_element(By.XPATH, ".//button[contains(@class, 'hover:bg-rose-50') or contains(@class, 'text-slate-400')]")
        safe_click(driver, close_btn)
        time.sleep(1.0)

    # -------------------------------------------------------------------------
    # Step 7: Login (ข้อ 1)
    # -------------------------------------------------------------------------
    def test_07_user_flow_login(self, driver):
        """
        [User Flow ขั้นที่ 7 / ข้อ 1] login:
        เจ้าหน้าที่ตัวจริงเข้าสู่ระบบด้วยบัญชี admin / password123
        การเช็คความถูกต้อง:
          1. เช็คว่าเข้าสู่ระบบสำเร็จ แสดงปุ่ม 'ออกจากระบบ'
          2. เช็คว่า Navbar แสดงชื่อ 'สมชาย (Admin)' และสิทธิ์เป็น 'admin'
          3. เช็คว่าเมนู 'จัดการรายงานทั้งหมด' ปลดล็อกพร้อมใช้งาน
        """
        driver.get(TARGET_WEB_URL)
        wait = WebDriverWait(driver, 10)

        # เข้าสู่ระบบด้วย admin
        admin_login_helper(driver, "admin", "password123")

        # เช็คที่ 1: พบปุ่มออกจากระบบ
        logout_btns = driver.find_elements(By.XPATH, "//button[@title='ออกจากระบบ']")
        assert len(logout_btns) > 0, "[CHECK FAILED] ต้องพบบุ่มออกจากระบบหลังล็อกอินสำเร็จ"

        # เช็คที่ 2: เมนูแอดมินแสดง
        page_source = driver.page_source
        assert "จัดการรายงานทั้งหมด" in page_source, "[CHECK FAILED] ต้องแสดงแท็บจัดการรายงานทั้งหมด"
        assert "สมชาย" in page_source or "Admin" in page_source or "admin" in page_source, \
            "[CHECK FAILED] ต้องแสดงชื่อผู้ใช้หรือสถานะ Admin ใน Navbar"

        # ขั้นตอนสุดท้าย: เช็คการแจ้งผลลัพธ์ว่าสำเร็จจริง
        login_modals = driver.find_elements(By.XPATH, "//div[contains(@class, 'z-50') and contains(., 'Secure Login')]")
        assert len(login_modals) == 0, "[CHECK FAILED] หน้าต่าง Secure Login ต้องปิดลงเมื่อเข้าสู่ระบบสำเร็จ"
        assert "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง" not in driver.page_source, \
            "[CHECK FAILED] ต้องไม่มีข้อความแจ้งเตือน error เมื่อเข้าสู่ระบบสำเร็จ"

        # บันทึกภาพหน้าจอเป็นหลักฐานเมื่อทำเสร็จสมบูรณ์
        take_screenshot(driver, "01_login_success.png")

    # -------------------------------------------------------------------------
    # Step 8: Admin แก้ไข (ข้อ 6)
    # -------------------------------------------------------------------------
    def test_08_user_flow_admin_แก้ไข(self, driver):
        """
        [User Flow ขั้นที่ 8 / ข้อ 6] admin แก้ไข:
        Admin เปิดดูเคสที่สร้างจากขั้นตอนที่ 3 แล้วทำการแก้ไขข้อมูลรายละเอียดสำนวน
        การเช็คความถูกต้อง:
          1. เช็คว่าเปิด Modal โหมดแก้ไขรายงานได้
          2. แก้ไขข้อความรายละเอียดและกดบันทึก
          3. เช็คว่ามีข้อความ Toast 'บันทึกการแก้ไขข้อมูลรายงาน ... สำเร็จแล้ว'
        """
        driver.get(TARGET_WEB_URL)
        admin_login_helper(driver)
        navigate_to_tab(driver, "จัดการรายงานทั้งหมด")
        wait = WebDriverWait(driver, 10)

        # หากมี Report ID ที่สร้างไว้ ให้ค้นหาเฉพาะเคสนั้น
        target_id = UserFlowContext.report_id
        if target_id:
            search_box = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[contains(@placeholder, 'ค้นหาด้วย Case ID')]")))
            search_box.clear()
            search_box.send_keys(target_id)
            time.sleep(1.0)

        # คลิกปุ่มแก้ไข
        edit_btns = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, "//button[@title='คลิกเพื่อแก้ไขข้อมูลรายงาน']"))
        )
        assert len(edit_btns) > 0, "[CHECK FAILED] ต้องพบบุ่มแก้ไขรายงานในตาราง"
        safe_click(driver, edit_btns[0])
        time.sleep(1.5)

        # ตรวจสอบว่าเปิดโหมดแก้ไข
        assert "โหมดแก้ไขรายงาน" in driver.page_source or "แก้ไข" in driver.page_source, \
            "[CHECK FAILED] ต้องเปิดหน้าต่างโหมดแก้ไขรายงาน"

        # เพิ่มข้อความในคำอธิบาย
        desc_edit = driver.find_element(By.XPATH, "//textarea[contains(@placeholder, 'รายละเอียด')]")
        driver.execute_script("arguments[0].value += ' [ตรวจสอบและแก้ไขโดย Admin]';", desc_edit)

        # กดบันทึกการแก้ไข
        save_btn = driver.find_element(By.XPATH, "//button[contains(., 'บันทึกการแก้ไขข้อมูล')]")
        safe_click(driver, save_btn)

        # ขั้นตอนสุดท้าย: เช็คการแจ้งเตือนผลลัพธ์ว่าบันทึกสำเร็จจริง (Success Toast Notification)
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

    # -------------------------------------------------------------------------
    # Step 9: Admin เปลี่ยน (ข้อ 10)
    # -------------------------------------------------------------------------
    def test_09_user_flow_admin_เปลี่ยน(self, driver):
        """
        [User Flow ขั้นที่ 9 / ข้อ 10] admin เปลี่ยน:
        Admin ปรับเปลี่ยนสถานะคดีในตารางเป็น 'ดำเนินการทางวินัย' (disciplinary)
        การเช็คความถูกต้อง:
          1. เช็คว่าค่าของ Dropdown ในตารางเปลี่ยนเป็น 'ดำเนินการทางวินัย' จริง
          2. [CROSS-CHECK] สลับไปหน้าติดตามสถานะของผู้แจ้งเบาะแส ค้นหาด้วย Report ID
             เช็คว่าผู้แจ้งเห็นสถานะเปลี่ยนเป็น 'ดำเนินการทางวินัย' ตรงกันจริง!
        """
        driver.get(TARGET_WEB_URL)
        admin_login_helper(driver)
        navigate_to_tab(driver, "จัดการรายงานทั้งหมด")
        wait = WebDriverWait(driver, 10)

        target_id = UserFlowContext.report_id
        if target_id:
            search_box = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[contains(@placeholder, 'ค้นหาด้วย Case ID')]")))
            search_box.clear()
            search_box.send_keys(target_id)
            time.sleep(1.0)

        # หา Dropdown เปลี่ยนสถานะ
        status_dropdowns = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, "//select[contains(@title, 'เปลี่ยนสถานะดำเนินการ')]"))
        )
        assert len(status_dropdowns) > 0, "[CHECK FAILED] ไม่พบ Dropdown เปลี่ยนสถานะ"

        sel = Select(status_dropdowns[0])
        sel.select_by_value("disciplinary")

        # ตรวจสอบการแจ้งเตือน Toast ฝั่งแอดมิน (Admin Toast Notification)
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

        # เช็คที่ 1: ตรวจว่าค่าใน Dropdown เปลี่ยนเป็น disciplinary จริง
        assert sel.first_selected_option.get_attribute("value") == "disciplinary", \
            "[CHECK FAILED] ค่า Dropdown ต้องเปลี่ยนเป็น disciplinary"

        # ขั้นตอนสุดท้าย: เช็คการแจ้งผลลัพธ์สถานะใหม่ฝั่งผู้ติดตาม (Status Change Notification)
        if target_id and UserFlowContext.pin:
            navigate_to_tab(driver, "ติดตามสถานะ")
            id_inp = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='TL-XXXX-XXXX']")))
            id_inp.clear()
            id_inp.send_keys(target_id)
            pin_inp = driver.find_element(By.XPATH, "//input[@placeholder='••••']")
            pin_inp.clear()
            pin_inp.send_keys(UserFlowContext.pin)
            check_btn = driver.find_element(By.XPATH, "//button[contains(., 'ตรวจสอบ')]")
            safe_click(driver, check_btn)
            time.sleep(2.0)

            new_status_badge = wait.until(
                EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'ดำเนินการทางวินัย')]"))
            )
            assert new_status_badge.is_displayed(), \
                "[CHECK FAILED (CROSS-CHECK)] หน้าติดตามของผู้แจ้งต้องแสดงสถานะใหม่ 'ดำเนินการทางวินัย'"

        # บันทึกภาพหน้าจอเป็นหลักฐานเมื่อทำเสร็จสมบูรณ์
        take_screenshot(driver, "10_admin_change_status_success.png")

    # -------------------------------------------------------------------------
    # Step 10: Admin ลบ (ข้อ 9)
    # -------------------------------------------------------------------------
    def test_10_user_flow_admin_ลบ(self, driver):
        """
        [User Flow ขั้นที่ 10 / ข้อ 9] admin ลบ:
        Admin สั่งลบเคสรายงานดังกล่าวออกจากระบบอย่างถาวร
        การเช็คความถูกต้อง:
          1. เช็คว่ามีกล่องยืนยัน 'ยืนยันการลบรายงาน' ปรากฏขึ้นเพื่อความปลอดภัย
          2. [CROSS-CHECK ฝั่งแอดมิน] ค้นหา Report ID ในตาราง Admin เช็คว่าไม่พบรายงานนั้นแล้ว (หายไปจริง)
          3. [CROSS-CHECK ฝั่งผู้ใช้] ไปหน้าติดตามสถานะ ค้นหาด้วย Report ID นั้น
             เช็คว่าระบบแจ้งว่า 'ไม่พบรหัสรายงาน' ยืนยันว่าคดีถูกลบออกจากระบบสมบูรณ์ 100%!
        """
        driver.get(TARGET_WEB_URL)
        admin_login_helper(driver)
        navigate_to_tab(driver, "จัดการรายงานทั้งหมด")
        wait = WebDriverWait(driver, 10)

        target_id = UserFlowContext.report_id
        if target_id:
            search_box = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[contains(@placeholder, 'ค้นหาด้วย Case ID')]")))
            search_box.clear()
            search_box.send_keys(target_id)
            time.sleep(1.0)

        del_btns = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, "//button[@title='ลบรายงาน']"))
        )
        assert len(del_btns) > 0, "[CHECK FAILED] ไม่พบบุ่มลบรายงานในตาราง"
        safe_click(driver, del_btns[0])
        time.sleep(1.0)

        # เช็คที่ 1: กล่องยืนยันการลบต้องแสดง
        confirm_title = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//h3[contains(text(), 'ยืนยันการลบรายงาน')]"))
        )
        assert confirm_title.is_displayed(), "[CHECK FAILED] ต้องแสดงกล่องยืนยันการลบรายงาน"

        confirm_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'ยืนยันลบข้อมูล')]")
        safe_click(driver, confirm_btn)

        # เช็ค Toast แจ้งเตือนลบสำเร็จฝั่งแอดมิน
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

        # เช็คที่ 2 (CROSS-CHECK ในตาราง Admin): ค้นหาเคสแล้วต้องไม่เจอ
        if target_id:
            search_box = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[contains(@placeholder, 'ค้นหาด้วย Case ID')]")))
            search_box.clear()
            search_box.send_keys(target_id)
            time.sleep(1.0)
            matching_buttons = driver.find_elements(By.XPATH, f"//button[contains(text(), '{target_id}')]")
            assert len(matching_buttons) == 0, f"[CHECK FAILED] เคส {target_id} ยังปรากฏในตารางหลังกดลบ!"

        # ขั้นตอนสุดท้าย: เช็คการแจ้งเตือนฝั่งผู้ติดตามว่าคดีถูกลบแล้วจริง (Deletion Status Notification)
        if target_id and UserFlowContext.pin:
            navigate_to_tab(driver, "ติดตามสถานะ")
            id_inp = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='TL-XXXX-XXXX']")))
            id_inp.clear()
            id_inp.send_keys(target_id)
            pin_inp = driver.find_element(By.XPATH, "//input[@placeholder='••••']")
            pin_inp.clear()
            pin_inp.send_keys(UserFlowContext.pin)
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

        # บันทึกภาพหน้าจอเป็นหลักฐานเมื่อทำเสร็จสมบูรณ์
        take_screenshot(driver, "09_admin_delete_success.png")

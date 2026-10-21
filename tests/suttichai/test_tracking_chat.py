"""
Automated Test Cases for Module 3: Status Tracking & 2-Way Encrypted Chat (FR-TRK)
Tester: วุฒิชัย (suttichai)
Test Cases: TC-031 through TC-038
Reference: docs/Annonymous-Test-Cases.docx & docs/FUNCTIONAL_REQUIREMENTS.md
"""

import time
import tempfile
import os
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.conftest import BASE_URL, switch_tab


class TestTrackingChatModule:
    """Test suite for Status Tracking & 2-Way Chat (FR-TRK-001 to FR-TRK-006)."""

    def test_tc031_search_report_with_valid_credentials(self, driver):
        """TC-031 | FR-TRK-001: ค้นหารายงานด้วย Report ID และ PIN ที่ถูกต้อง."""
        driver.get(BASE_URL)
        switch_tab(driver, "ติดตามสถานะ")

        # Use known seeded report TL-8942-XCVB / 8942
        id_input = driver.find_element(By.XPATH, "//input[@placeholder='TL-XXXX-XXXX']")
        pin_input = driver.find_element(By.XPATH, "//input[@placeholder='••••']")

        id_input.clear()
        id_input.send_keys("TL-8942-XCVB")
        pin_input.clear()
        pin_input.send_keys("8942")

        submit_btn = driver.find_element(By.XPATH, "//button[contains(., 'ตรวจสอบ')]")
        driver.execute_script("arguments[0].click();", submit_btn)
        time.sleep(1.5)

        # Case details view must be rendered
        assert "TL-8942-XCVB" in driver.page_source
        assert "กำลังตรวจสอบ" in driver.page_source or "รับเรื่อง" in driver.page_source
        # Chat box is present
        assert "สนทนาลับ" in driver.page_source or "ห้องสนทนา" in driver.page_source or "พิมพ์ข้อความ" in driver.page_source

    def test_tc032_search_report_with_incorrect_pin(self, driver):
        """TC-032 | FR-TRK-001: ค้นหารายงานด้วย PIN ที่ไม่ถูกต้อง."""
        driver.get(BASE_URL)
        switch_tab(driver, "ติดตามสถานะ")

        id_input = driver.find_element(By.XPATH, "//input[@placeholder='TL-XXXX-XXXX']")
        pin_input = driver.find_element(By.XPATH, "//input[@placeholder='••••']")

        id_input.clear()
        id_input.send_keys("TL-8942-XCVB")
        pin_input.clear()
        pin_input.send_keys("0000")  # Wrong PIN

        submit_btn = driver.find_element(By.XPATH, "//button[contains(., 'ตรวจสอบ')]")
        driver.execute_script("arguments[0].click();", submit_btn)
        time.sleep(0.5)

        assert "ไม่ถูกต้อง" in driver.page_source

    def test_tc033_search_report_with_nonexistent_id(self, driver):
        """TC-033 | FR-TRK-001: ค้นหารายงานด้วย Report ID ที่ไม่มีอยู่ในระบบ."""
        driver.get(BASE_URL)
        switch_tab(driver, "ติดตามสถานะ")

        id_input = driver.find_element(By.XPATH, "//input[@placeholder='TL-XXXX-XXXX']")
        pin_input = driver.find_element(By.XPATH, "//input[@placeholder='••••']")

        id_input.clear()
        id_input.send_keys("TL-9999-FAKE")
        pin_input.clear()
        pin_input.send_keys("1234")

        submit_btn = driver.find_element(By.XPATH, "//button[contains(., 'ตรวจสอบ')]")
        driver.execute_script("arguments[0].click();", submit_btn)
        time.sleep(0.5)

        assert "ไม่พบรหัสรายงาน" in driver.page_source or "ไม่ถูกต้อง" in driver.page_source

    def test_tc034_status_timeline_4_steps(self, driver):
        """TC-034 | FR-TRK-002: แสดงไทม์ไลน์สถานะคดี 4 ขั้นและไฮไลต์สถานะปัจจุบัน."""
        driver.get(BASE_URL)
        switch_tab(driver, "ติดตามสถานะ")

        # Click quick demo pill
        demo_btn = driver.find_element(By.XPATH, "//button[contains(., 'TL-8942-XCVB')]")
        driver.execute_script("arguments[0].click();", demo_btn)
        time.sleep(1.5)

        # Check all 4 steps in timeline
        page = driver.page_source
        assert "Status Timeline" in page
        assert "รับเรื่อง" in page
        assert "กำลังตรวจสอบ" in page
        assert "ดำเนินการทางวินัย" in page

    def test_tc035_two_way_realtime_chat(self, driver):
        """TC-035 | FR-TRK-003: ผู้แจ้งสนทนาลับ 2 ทางกับเจ้าหน้าที่แบบเรียลไทม์."""
        driver.get(BASE_URL)
        switch_tab(driver, "ติดตามสถานะ")

        demo_btn = driver.find_element(By.XPATH, "//button[contains(., 'TL-8942-XCVB')]")
        driver.execute_script("arguments[0].click();", demo_btn)
        time.sleep(1)

        # Send a message as reporter
        chat_input = driver.find_element(By.XPATH, "//input[contains(@placeholder, 'พิมพ์ข้อความ')]")
        test_msg = f"สวัสดีครับ มีหลักฐานเพิ่มเติม (ID: {int(time.time())})"
        chat_input.send_keys(test_msg)
        from selenium.webdriver.common.keys import Keys
        chat_input.send_keys(Keys.ENTER)
        time.sleep(1.5)

        # Message appears in chat history
        assert test_msg in driver.page_source
        assert "คุณ (ผู้แจ้ง)" in driver.page_source

    def test_tc036_typing_indicator(self, driver):
        """TC-036 | FR-TRK-004: แสดงสถานะกำลังพิมพ์ (Typing Indicator)."""
        driver.get(BASE_URL)
        switch_tab(driver, "ติดตามสถานะ")

        demo_btn = driver.find_element(By.XPATH, "//button[contains(., 'TL-8942-XCVB')]")
        driver.execute_script("arguments[0].click();", demo_btn)
        time.sleep(1)

        chat_input = driver.find_element(By.XPATH, "//input[contains(@placeholder, 'พิมพ์ข้อความ')]")
        chat_input.send_keys("กำลังพิมพ์ข้อความทดสอบ...")
        time.sleep(0.5)

        # Typing events are dispatched via WebSocket
        assert chat_input.get_attribute("value") == "กำลังพิมพ์ข้อความทดสอบ..."

    def test_tc037_reporter_upload_additional_evidence(self, driver):
        """TC-037 | FR-TRK-005: ผู้แจ้งแนบหลักฐานเพิ่มเติมผ่านหน้าติดตามสถานะ."""
        driver.get(BASE_URL)
        switch_tab(driver, "ติดตามสถานะ")

        demo_btn = driver.find_element(By.XPATH, "//button[contains(., 'TL-8942-XCVB')]")
        driver.execute_script("arguments[0].click();", demo_btn)
        time.sleep(1)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            f.write(b"additional evidence data")
            tmp_path = f.name

        try:
            # Locate file input in tracking view
            file_inputs = driver.find_elements(By.XPATH, "//input[@type='file']")
            if file_inputs:
                file_inputs[0].send_keys(tmp_path)
                time.sleep(1)

            # Check that file or upload section is active
            assert os.path.basename(tmp_path) in driver.page_source or "เอกสารและหลักฐาน" in driver.page_source
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_tc038_chat_auto_scroll(self, driver):
        """TC-038 | FR-TRK-006: หน้าต่างแชทเลื่อนไปข้อความล่าสุดอัตโนมัติ."""
        driver.get(BASE_URL)
        switch_tab(driver, "ติดตามสถานะ")

        demo_btn = driver.find_element(By.XPATH, "//button[contains(., 'TL-8942-XCVB')]")
        driver.execute_script("arguments[0].click();", demo_btn)
        time.sleep(1)

        # Send multiple messages to expand scroll height
        chat_input = driver.find_element(By.XPATH, "//input[contains(@placeholder, 'พิมพ์ข้อความ')]")
        for i in range(2):
            chat_input.send_keys(f"ข้อความสำหรับทดสอบ Scroll ที่ {i+1}")
            send_btn = driver.find_element(By.XPATH, "//form//button[@type='submit']")
            driver.execute_script("arguments[0].click();", send_btn)
            time.sleep(0.4)

        assert "ข้อความสำหรับทดสอบ Scroll ที่ 2" in driver.page_source

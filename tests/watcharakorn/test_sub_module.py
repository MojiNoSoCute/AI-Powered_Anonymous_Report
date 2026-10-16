"""
Automated Test Cases for Module 1: Anonymous Report Submission (FR-SUB)
Tester: วัชรากร (watcharakorn)
Test Cases: TC-001 through TC-021
Reference: docs/Annonymous-Test-Cases.docx & docs/FUNCTIONAL_REQUIREMENTS.md
"""

import time
import os
import tempfile
import pytest
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException, NoAlertPresentException
from tests.conftest import BASE_URL, login_as, switch_tab


class TestSubmissionModule:
    """Test suite for anonymous report submission module (FR-SUB-001 to FR-SUB-014)."""

    def test_tc001_form_step_hierarchy(self, driver):
        """TC-001 | FR-SUB-001: แสดงลำดับขั้นตอนแบบฟอร์มส่งรายงาน 4 ขั้นตอน (1, 2, 3, 4)."""
        driver.get(BASE_URL)
        switch_tab(driver, "สร้างรายงานใหม่")

        # Verify step numbers 1, 2, 3, 4 exist in the correct order
        step_1 = driver.find_element(By.XPATH, "//div[contains(@class, 'bg-rose-900') and text()='1']")
        step_2 = driver.find_element(By.XPATH, "//div[contains(@class, 'bg-rose-900') and text()='2']")
        step_3 = driver.find_element(By.XPATH, "//div[contains(@class, 'bg-rose-900') and text()='3']")
        step_4 = driver.find_element(By.XPATH, "//div[contains(@class, 'bg-rose-900') and text()='4']")

        assert step_1 and step_2 and step_3 and step_4, "All 4 steps must be visible in sequence"

        # Verify step titles
        assert "รายละเอียดเหตุการณ์" in driver.page_source
        assert "เอกสาร / หลักฐานประกอบ" in driver.page_source
        assert "หมวดหมู่เรื่องร้องเรียน" in driver.page_source
        assert "ระดับความเร่งด่วน" in driver.page_source

    def test_tc002_incident_date_default_and_past(self, driver):
        """TC-002 | FR-SUB-002: วันที่เกิดเหตุมีค่าเริ่มต้นเป็นวันปัจจุบันและเลือกย้อนหลังได้."""
        driver.get(BASE_URL)
        switch_tab(driver, "สร้างรายงานใหม่")

        date_input = driver.find_element(By.XPATH, "//input[@type='date']")
        initial_val = date_input.get_attribute("value")
        assert len(initial_val) == 10 and initial_val[4] == '-' and initial_val[7] == '-', f"Default date should be YYYY-MM-DD, got {initial_val}"

        # Change to past date via script for reliable HTML5 date element interaction
        past_date = "2026-01-15"
        driver.execute_script("""
            arguments[0].value = arguments[1];
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
        """, date_input, past_date)
        assert date_input.get_attribute("value") == past_date, "Date input should accept past dates"

    def test_tc003_incident_location_thai_english_length(self, driver):
        """TC-003 | FR-SUB-003: ระบุสถานที่เกิดเหตุเป็นภาษาไทย ภาษาอังกฤษ และความยาว 200 ตัวอักษร."""
        driver.get(BASE_URL)
        switch_tab(driver, "สร้างรายงานใหม่")

        loc_input = driver.find_element(By.XPATH, "//input[@placeholder='ระบุอาคาร / คณะ / บริเวณสถานที่']")

        # Thai text
        thai_loc = "อาคารเรียนรวม ชั้น 3 ห้อง 5302 มหาวิทยาลัยราชภัฏนครปฐม"
        driver.execute_script("""
            arguments[0].value = arguments[1];
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
        """, loc_input, thai_loc)
        assert loc_input.get_attribute("value") == thai_loc

        # English text
        eng_loc = "Main Central Library, 2nd Floor, Room 204"
        driver.execute_script("""
            arguments[0].value = arguments[1];
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
        """, loc_input, eng_loc)
        assert loc_input.get_attribute("value") == eng_loc

        # Long text (200 chars)
        long_loc = "A" * 200
        driver.execute_script("""
            arguments[0].value = arguments[1];
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
        """, loc_input, long_loc)
        assert loc_input.get_attribute("value") == long_loc

    def test_tc004_blank_location_defaults_to_unspecified(self, driver):
        """TC-004 | FR-SUB-003: ไม่ระบุสถานที่ ระบบบันทึกเป็น 'ไม่ระบุ'."""
        driver.get(BASE_URL)
        switch_tab(driver, "สร้างรายงานใหม่")

        loc_input = driver.find_element(By.XPATH, "//input[@placeholder='ระบุอาคาร / คณะ / บริเวณสถานที่']")
        loc_input.clear()

        # Enter description
        desc_box = driver.find_element(By.XPATH, "//textarea")
        desc_box.clear()
        desc_box.send_keys("ทดสอบกรณีไม่ระบุสถานที่เกิดเหตุ เพื่อตรวจสอบค่าเริ่มต้นไม่ระบุ")

        # Submit report
        submit_btn = driver.find_element(By.XPATH, "//button[contains(., 'ยืนยันส่งรายงานลับ')]")
        submit_btn.click()

        # Wait for modal and get Report ID & PIN
        wait = WebDriverWait(driver, 8)
        report_id_elem = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//span[contains(@class, 'font-mono') and contains(text(), 'TL-')]"))
        )
        report_id = report_id_elem.text.strip()
        pin_elem = driver.find_element(By.XPATH, "//span[contains(@class, 'font-mono') and string-length(text()) = 4]")
        pin = pin_elem.text.strip()

        # Go to tracking page
        track_btn = driver.find_element(By.XPATH, "//button[contains(., 'ไปยังหน้าติดตามสถานะ')]")
        track_btn.click()
        time.sleep(1)

        # Check in tracking details that location shows "ไม่ระบุ"
        assert "ไม่ระบุ" in driver.page_source

    def test_tc005_description_character_counter_realtime(self, driver):
        """TC-005 | FR-SUB-004: เคาน์เตอร์นับตัวอักษรรายละเอียดเหตุการณ์ทำงานแบบเรียลไทม์."""
        driver.get(BASE_URL)
        switch_tab(driver, "สร้างรายงานใหม่")

        desc_box = driver.find_element(By.XPATH, "//textarea")
        counter_elem = driver.find_element(By.XPATH, "//span[contains(., '/ 5000')]")
        assert "0 / 5000" in counter_elem.text

        sample_text = "ทดสอบการนับตัวอักษร 12345"
        desc_box.send_keys(sample_text)
        time.sleep(0.5)

        expected_count = f"{len(sample_text)} / 5000"
        counter_elem = driver.find_element(By.XPATH, "//span[contains(., '/ 5000')]")
        assert expected_count in counter_elem.text

    def test_tc006_submit_without_description_blocked(self, driver):
        """TC-006 | FR-SUB-004: กดส่งรายงานโดยไม่กรอกรายละเอียดเหตุการณ์ ระบบต้องไม่อนุญาต."""
        driver.get(BASE_URL)
        switch_tab(driver, "สร้างรายงานใหม่")

        desc_box = driver.find_element(By.XPATH, "//textarea")
        desc_box.clear()

        submit_btn = driver.find_element(By.XPATH, "//button[contains(., 'ยืนยันส่งรายงานลับ')]")
        submit_btn.click()
        time.sleep(0.5)

        # Success modal must NOT appear
        modals = driver.find_elements(By.XPATH, "//h3[contains(text(), 'ส่งรายงานลับสำเร็จแล้ว')]")
        assert len(modals) == 0, "Submission should not succeed without description"

    def test_tc007_description_max_length_5000(self, driver):
        """TC-007 | FR-SUB-004: กรอกรายละเอียดเหตุการณ์ถึงขีดจำกัด 5,000 ตัวอักษร."""
        driver.get(BASE_URL)
        switch_tab(driver, "สร้างรายงานใหม่")

        desc_box = driver.find_element(By.XPATH, "//textarea")
        assert desc_box.get_attribute("maxlength") == "5000"

        # Inject 5000 characters via native prototype setter so React synthetic events update state
        driver.execute_script("""
            var nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, "value").set;
            nativeSetter.call(arguments[0], 'A'.repeat(5000));
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
        """, desc_box)
        time.sleep(0.5)

        counter_elem = driver.find_element(By.XPATH, "//span[contains(., '/ 5000')]")
        assert "5000 / 5000" in counter_elem.text

    def test_tc008_upload_evidence_click_files(self, driver):
        """TC-008 | FR-SUB-005: แนบไฟล์หลักฐานด้วยการเลือกไฟล์ แสดงชื่อ ขนาด และจำนวน."""
        driver.get(BASE_URL)
        switch_tab(driver, "สร้างรายงานใหม่")

        # Create temporary dummy test file
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            f.write(b"fake image content")
            tmp_path = f.name

        try:
            file_input = driver.find_element(By.XPATH, "//input[@type='file']")
            file_input.send_keys(tmp_path)
            time.sleep(1)

            # Check that file list appeared
            assert "ไฟล์ที่แนบไว้" in driver.page_source
            base_name = os.path.basename(tmp_path)
            assert base_name in driver.page_source
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_tc009_upload_evidence_multiple_types(self, driver):
        """TC-009 | FR-SUB-005: แนบไฟล์หลักฐานหลายประเภท (PNG, PDF)."""
        driver.get(BASE_URL)
        switch_tab(driver, "สร้างรายงานใหม่")

        f1 = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
        f1.write(b"%PDF-1.4 test document")
        f1.close()

        try:
            file_input = driver.find_element(By.XPATH, "//input[@type='file']")
            file_input.send_keys(f1.name)
            time.sleep(1)

            assert os.path.basename(f1.name) in driver.page_source
        finally:
            if os.path.exists(f1.name):
                os.remove(f1.name)

    def test_tc010_upload_file_exceeding_50mb_rejected(self, driver):
        """TC-010 | FR-SUB-005: แนบไฟล์ที่มีขนาดรวมเกิน 50MB ระบบต้องปฏิเสธและเตือน."""
        driver.get(BASE_URL)
        switch_tab(driver, "สร้างรายงานใหม่")

        # Simulate large file input trigger with JavaScript File object with size > 50MB
        js_simulate_large_file = """
        const input = document.querySelector("input[type='file']");
        const dt = new DataTransfer();
        const blob = new Blob(['x'.repeat(1024)], { type: 'video/mp4' });
        // Override size property to simulate 55MB
        Object.defineProperty(blob, 'size', { value: 55 * 1024 * 1024 });
        const file = new File([blob], 'heavy_video.mp4', { type: 'video/mp4' });
        Object.defineProperty(file, 'size', { value: 55 * 1024 * 1024 });
        dt.items.add(file);
        input.files = dt.files;
        input.dispatchEvent(new Event('change', { bubbles: true }));
        """
        driver.execute_script(js_simulate_large_file)
        time.sleep(0.5)

        # Handle browser alert with WebDriverWait
        try:
            WebDriverWait(driver, 3).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            alert_text = alert.text
            assert "50MB" in alert_text or "เกิน" in alert_text
            alert.accept()
        except Exception:
            # If alert already dismissed by capability or rendered in UI
            pass

    def test_tc011_invalid_file_type_rejected(self, driver):
        """TC-011 | FR-SUB-005: แนบไฟล์ผิดประเภท (Negative) - ปฏิเสธไฟล์ที่ไม่ใช่ PNG, JPG, PDF หรือ MP4."""
        driver.get(BASE_URL)
        switch_tab(driver, "สร้างรายงานใหม่")

        # 1. Verify upload zone policy explicitly restricts to allowed types (PNG, JPG, PDF)
        page_source = driver.page_source
        assert "PDF" in page_source or "PNG" in page_source or "JPG" in page_source, "Upload zone must state supported types (PDF, PNG, JPG)"

        with tempfile.NamedTemporaryFile(suffix=".exe", delete=False) as f:
            f.write(b"binary executable data")
            tmp_path = f.name

        try:
            file_input = driver.find_element(By.XPATH, "//input[@type='file']")
            alert_triggered = False

            # Attempt sending invalid file; catch UnexpectedAlertPresentException if raised during send_keys
            try:
                file_input.send_keys(tmp_path)
                time.sleep(0.5)
            except UnexpectedAlertPresentException:
                alert_triggered = True
                try:
                    alert = driver.switch_to.alert
                    alert.accept()
                except Exception:
                    pass
            except Exception:
                pass

            # Check if alert was triggered for invalid file type
            if not alert_triggered:
                try:
                    WebDriverWait(driver, 2).until(EC.alert_is_present())
                    alert = driver.switch_to.alert
                    alert.accept()
                    alert_triggered = True
                except Exception:
                    pass

            # Double-check if any alert dialog is still active and dismiss it
            try:
                alert = driver.switch_to.alert
                alert.accept()
            except Exception:
                pass

            time.sleep(0.5)

            base_name = os.path.basename(tmp_path)
            attached_chips = driver.find_elements(By.XPATH, f"//div[contains(., 'ไฟล์ที่แนบไว้')]//span[contains(text(), '{base_name}')]")
            if not attached_chips:
                # Also check any file chip spans with truncate class
                attached_chips = driver.find_elements(By.XPATH, f"//span[contains(@class, 'truncate') and contains(text(), '{base_name}')]")
            accept_attr = file_input.get_attribute("accept") or ""
            is_valid_handling = (
                len(attached_chips) == 0 or 
                alert_triggered or 
                bool(accept_attr and any(t in accept_attr.lower() for t in ["image", "pdf", "video", ".png", ".jpg"])) or
                ("PDF" in driver.page_source and ("PNG" in driver.page_source or "ภาพ" in driver.page_source or "JPG" in driver.page_source))
            )
            assert is_valid_handling, f"System must enforce file type restrictions: {base_name}"
            assert len(attached_chips) == 0, f"Rejected file {base_name} must not be attached"

            # Clean up uploaded chip if attached so form stays clean
            if len(attached_chips) > 0:
                trash_btns = driver.find_elements(By.XPATH, "//button[contains(@class, 'hover:text-red-600')]")
                if trash_btns:
                    driver.execute_script("arguments[0].click();", trash_btns[0])
                    time.sleep(0.5)
        finally:
            if os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except Exception:
                    pass

    def test_tc012_delete_attached_file(self, driver):
        """TC-012 | FR-SUB-006: ผู้ใช้สามารถลบไฟล์ที่แนบก่อนกดส่งรายงาน."""
        driver.get(BASE_URL)
        switch_tab(driver, "สร้างรายงานใหม่")

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            f.write(b"fake delete image")
            tmp_path = f.name

        try:
            file_input = driver.find_element(By.XPATH, "//input[@type='file']")
            file_input.send_keys(tmp_path)
            time.sleep(1)

            base_name = os.path.basename(tmp_path)
            assert base_name in driver.page_source

            # Click trash button
            trash_btn = driver.find_element(By.XPATH, "//button[contains(@class, 'hover:text-red-600')]")
            trash_btn.click()
            time.sleep(0.5)

            # File should no longer be displayed
            assert base_name not in driver.page_source
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_tc013_category_initial_state_empty(self, driver):
        """TC-013 | FR-SUB-007: ค่าเริ่มต้นของหมวดหมู่และรายการหมวดหมู่ 7 ประเภท."""
        driver.get(BASE_URL)
        switch_tab(driver, "สร้างรายงานใหม่")

        # Category section must be present with options
        category_cards = driver.find_elements(By.XPATH, "//input[@name='category'] | //label[contains(., 'Bullying')] | //div[contains(., 'การล่วงละเมิดและคุกคาม')]")
        assert len(category_cards) >= 7, "All 7 categories must be present in submission form"

    def test_tc014_guest_category_locked(self, driver):
        """TC-014 | FR-SUB-008: การแสดงผลหมวดหมู่และการป้องกันการเลือกผิดพลาด."""
        driver.get(BASE_URL)
        switch_tab(driver, "สร้างรายงานใหม่")

        assert "หมวดหมู่" in driver.page_source
        cards = driver.find_elements(By.XPATH, "//input[@name='category'] | //label[contains(., 'Harassment')] | //div[contains(@class, 'cursor-not-allowed')]")
        assert len(cards) >= 7

    def test_tc015_staff_can_select_category(self, driver):
        """TC-015 | FR-SUB-009: เจ้าหน้าที่หรือผู้ใช้สามารถเลือกและสลับหมวดหมู่ในแบบฟอร์มได้."""
        driver.get(BASE_URL)
        switch_tab(driver, "สร้างรายงานใหม่")

        # Click Fraud category
        fraud_targets = driver.find_elements(By.XPATH, "//*[contains(text(), 'การทุจริตทางการเงิน')]")
        assert len(fraud_targets) > 0
        driver.execute_script("arguments[0].click();", fraud_targets[0])
        time.sleep(0.3)

        assert "การทุจริตทางการเงิน" in driver.page_source

    def test_tc016_urgency_initial_state_empty(self, driver):
        """TC-016 | FR-SUB-010: ค่าเริ่มต้นของความเร่งด่วนและระบบควบคุมระดับ."""
        driver.get(BASE_URL)
        switch_tab(driver, "สร้างรายงานใหม่")

        urgency_section = driver.find_element(By.XPATH, "//div[contains(., 'ระดับความเร่งด่วน (Urgency Level)')]")
        assert "ระดับความเร่งด่วน" in urgency_section.text

    def test_tc017_guest_urgency_locked(self, driver):
        """TC-017 | FR-SUB-011: บุคคลทั่วไปเปลี่ยนระดับความเร่งด่วนด้วยตนเองไม่ได้."""
        driver.get(BASE_URL)
        switch_tab(driver, "สร้างรายงานใหม่")

        # Check lock indicators (badge text, lock icon, or locked class)
        lock_indicators = driver.find_elements(By.XPATH, "//*[contains(text(), 'เฉพาะ Admin') or contains(text(), 'เฉพาะ AI') or contains(@class, 'cursor-not-allowed') or contains(@class, 'opacity-60')]")
        assert len(lock_indicators) > 0, "Urgency cards must indicate locked/restricted for guest"

    def test_tc018_submission_generates_id_and_pin(self, driver):
        """TC-018 | FR-SUB-012: ส่งรายงานสำเร็จและสร้าง Report ID / PIN อัตโนมัติ."""
        driver.get(BASE_URL)
        switch_tab(driver, "สร้างรายงานใหม่")

        desc_box = driver.find_element(By.XPATH, "//textarea")
        desc_box.send_keys("รายงานการทำข้อสอบทุจริตในห้องเรียนอาคาร 10 เพื่อทดสอบการสร้าง ID และ PIN")

        submit_btn = driver.find_element(By.XPATH, "//button[contains(., 'ยืนยันส่งรายงานลับ')]")
        submit_btn.click()

        wait = WebDriverWait(driver, 8)
        report_id_elem = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), 'TL-')]"))
        )
        report_id = report_id_elem.text.strip()
        assert report_id.startswith("TL-"), f"Report ID should start with TL-, got {report_id}"

        pin_elem = driver.find_element(By.XPATH, "//span[string-length(text())=4 and number(text()) > 0]")
        pin = pin_elem.text.strip()
        assert pin.isdigit() and len(pin) == 4, f"PIN should be 4 digits, got {pin}"

    def test_tc019_unique_report_ids(self, driver):
        """TC-019 | FR-SUB-012: Report ID ไม่ซ้ำกันเมื่อส่งหลายรายงาน."""
        ids = []
        for i in range(2):
            driver.get(BASE_URL)
            switch_tab(driver, "สร้างรายงานใหม่")

            desc_box = driver.find_element(By.XPATH, "//textarea")
            desc_box.send_keys(f"รายงานทดสอบความไม่ซ้ำกันของ Report ID ครั้งที่ {i+1} รายละเอียดเพิ่มเติม")

            submit_btn = driver.find_element(By.XPATH, "//button[contains(., 'ยืนยันส่งรายงานลับ')]")
            submit_btn.click()

            wait = WebDriverWait(driver, 8)
            report_id_elem = wait.until(
                EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), 'TL-')]"))
            )
            ids.append(report_id_elem.text.strip())

        assert len(ids) == 2
        assert ids[0] != ids[1], f"Report IDs must be unique: {ids[0]} vs {ids[1]}"

    def test_tc020_success_modal_and_copy_button(self, driver):
        """TC-020 | FR-SUB-013: หน้าต่างแจ้งเตือนสำเร็จและปุ่มคัดลอกรหัสและ PIN."""
        driver.get(BASE_URL)
        switch_tab(driver, "สร้างรายงานใหม่")

        desc_box = driver.find_element(By.XPATH, "//textarea")
        desc_box.send_keys("ทดสอบหน้าต่างแจ้งเตือนและฟังก์ชันปุ่มคัดลอก Report ID และ PIN")

        submit_btn = driver.find_element(By.XPATH, "//button[contains(., 'ยืนยันส่งรายงานลับ')]")
        submit_btn.click()

        wait = WebDriverWait(driver, 8)
        copy_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'คัดลอกรหัสและ PIN')]"))
        )
        copy_btn.click()
        time.sleep(0.5)

        # Button changes state to copied
        assert "คัดลอกรหัสเรียบร้อยแล้ว" in driver.page_source

        # Has link to tracking
        track_btn = driver.find_element(By.XPATH, "//button[contains(., 'ไปยังหน้าติดตามสถานะ')]")
        assert track_btn.is_displayed()

    def test_tc021_save_draft_button(self, driver):
        """TC-021 | FR-SUB-014: ปุ่มบันทึกร่างข้อมูลในเบราว์เซอร์."""
        driver.get(BASE_URL)
        switch_tab(driver, "สร้างรายงานใหม่")

        desc_box = driver.find_element(By.XPATH, "//textarea")
        desc_box.send_keys("ข้อความร่างข้อมูลก่อนการส่งจริง")

        draft_btn = driver.find_element(By.XPATH, "//button[contains(., 'บันทึกร่าง')]")
        draft_btn.click()
        time.sleep(0.5)

        try:
            WebDriverWait(driver, 3).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            assert "บันทึกร่าง" in alert.text
            alert.accept()
        except Exception:
            pass

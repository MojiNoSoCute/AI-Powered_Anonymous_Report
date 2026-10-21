"""
Automated Test Cases for Module 6: Authentication & Security (FR-SEC)
Tester: สหรัฐ (saharat)
Test Cases: TC-058 through TC-063
Reference: docs/Annonymous-Test-Cases.docx & docs/FUNCTIONAL_REQUIREMENTS.md
"""

import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.conftest import BASE_URL, switch_tab, login_as


class TestAuthSecurityModule:
    """Test suite for Authentication & Security (FR-SEC-001 to FR-SEC-004)."""

    def test_tc058_staff_login_admin(self, driver):
        """TC-058 | FR-SEC-001: เจ้าหน้าที่เข้าสู่ระบบด้วยบัญชี admin (สิทธิ์เต็ม)."""
        driver.get(BASE_URL)
        login_as(driver, "admin", "password123")

        # Navbar should now show admin user info
        assert "เจ้าหน้าที่สืบสวน สมชาย (Admin)" in driver.page_source or "admin" in driver.page_source
        # Admin menu unlocked
        assert "จัดการรายงานทั้งหมด" in driver.page_source
        assert "สถิติ" in driver.page_source

    def test_tc059_investigator_login_officer1(self, driver):
        """TC-059 | FR-SEC-001: เจ้าหน้าที่สืบสวนเข้าสู่ระบบด้วยบัญชี officer1."""
        driver.get(BASE_URL)
        login_as(driver, "officer1", "password123")

        # Navbar shows officer or admin staff info and unlocks case management
        assert "จัดการรายงานทั้งหมด" in driver.page_source
        assert "ออกจากระบบ" in driver.page_source

    def test_tc060_login_failure_wrong_credentials(self, driver):
        """TC-060 | FR-SEC-001: เข้าสู่ระบบด้วยรหัสผ่านหรือบัญชีที่ไม่ถูกต้อง."""
        driver.get(BASE_URL)

        wait = WebDriverWait(driver, 8)
        login_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(., 'เข้าสู่ระบบ') or contains(., 'เจ้าหน้าที่เข้าสู่ระบบ')]")
            )
        )
        driver.execute_script("arguments[0].click();", login_btn)

        user_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='admin']")))
        user_input.clear()
        user_input.send_keys("fake_user")

        pass_input = driver.find_element(By.XPATH, "//input[@type='password' and contains(@placeholder, '•')]")
        pass_input.clear()
        pass_input.send_keys("wrong_pass_999")

        submit_btn = driver.find_element(By.XPATH, "//button[@type='submit' and contains(., 'เข้าสู่ระบบ')]")
        driver.execute_script("arguments[0].click();", submit_btn)
        time.sleep(0.8)

        # Error notification in modal
        assert "ไม่ถูกต้อง" in driver.page_source

    def test_tc061_staff_logout_clears_session(self, logged_in_admin_driver):
        """TC-061 | FR-SEC-002: เจ้าหน้าที่ออกจากระบบและเคลียร์ Session."""
        # Find logout button in navbar
        wait = WebDriverWait(logged_in_admin_driver, 8)
        logout_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@title='ออกจากระบบ']"))
        )
        logged_in_admin_driver.execute_script("arguments[0].click();", logout_btn)
        time.sleep(1)

        # Back to guest mode
        assert "เจ้าหน้าที่เข้าสู่ระบบ" in logged_in_admin_driver.page_source
        assert "จัดการรายงานทั้งหมด" not in logged_in_admin_driver.find_element(By.TAG_NAME, "nav").text

    def test_tc062_anonymity_enforcement(self, driver):
        """TC-062 | FR-SEC-003: ระบบไม่จัดเก็บข้อมูลส่วนบุคคลของผู้แจ้ง (Anonymity Enforcement)."""
        driver.get(BASE_URL)
        switch_tab(driver, "สร้างรายงานใหม่")

        # Submission form must NOT have input for Name, National ID, Phone, Email, Student ID
        forbidden_labels = ["ชื่อ-นามสกุล", "หมายเลขบัตรประชาชน", "เบอร์โทรศัพท์", "อีเมลผู้แจ้ง", "รหัสนักศึกษา"]
        page = driver.page_source
        for label in forbidden_labels:
            assert label not in page, f"Form must not request PII: {label}"

    def test_tc063_audit_trail_logging(self, logged_in_admin_driver):
        """TC-063 | FR-SEC-004: บันทึกประวัติการแก้ไข (Audit Trail Logging)."""
        switch_tab(logged_in_admin_driver, "สถิติ & สรุปผล")

        # Check Audit log table exists
        page = logged_in_admin_driver.page_source
        assert "ประวัติกิจกรรม" in page or "Audit Log" in page or "บันทึก" in page

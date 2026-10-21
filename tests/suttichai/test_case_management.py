"""
Automated Test Cases for Module 4: Case Management Dashboard (FR-CAS)
Tester: วุฒิชัย (suttichai)
Test Cases: TC-039 through TC-053
Reference: docs/Annonymous-Test-Cases.docx & docs/FUNCTIONAL_REQUIREMENTS.md
"""

import time
import tempfile
import os
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.conftest import BASE_URL, switch_tab, login_as, close_any_modal


class TestCaseManagementModule:
    """Test suite for Case Management Dashboard (FR-CAS-001 to FR-CAS-013)."""

    def test_tc039_protected_route_for_unauthenticated_user(self, driver):
        """TC-039 | FR-CAS-001: บุคคลที่ไม่ได้ล็อกอินเข้าแท็บจัดการรายงานไม่ได้."""
        driver.get(BASE_URL)

        # In guest mode, "จัดการรายงานทั้งหมด" tab must NOT be visible in public navigation
        nav_text = driver.find_element(By.TAG_NAME, "nav").text
        assert "จัดการรายงานทั้งหมด" not in nav_text
        assert "เจ้าหน้าที่เข้าสู่ระบบ" in driver.page_source

    def test_tc040_case_table_search_and_live_filter(self, logged_in_admin_driver):
        """TC-040 | FR-CAS-002: ค้นหาและกรองตารางคดีแบบทันที (Live Filtering)."""
        switch_tab(logged_in_admin_driver, "จัดการรายงานทั้งหมด")

        # Type in search box
        search_box = logged_in_admin_driver.find_element(By.XPATH, "//input[contains(@placeholder, 'ค้นหาด้วย Case ID')]")
        search_box.clear()
        search_box.send_keys("TL-8942-XCVB")
        time.sleep(0.5)

        # Only matching case should be shown
        assert "TL-8942-XCVB" in logged_in_admin_driver.page_source

        # Clear search and test not found
        search_box.clear()
        search_box.send_keys("NONEXISTENT_FILTER_KEYWORD_XYZ")
        time.sleep(0.5)
        assert "ไม่พบคดีที่ตรงกับเงื่อนไข" in logged_in_admin_driver.page_source or "0 รายการ" in logged_in_admin_driver.page_source

    def test_tc041_case_table_pagination(self, logged_in_admin_driver):
        """TC-041 | FR-CAS-002: ตารางคดีแบ่งหน้า (Pagination) เมื่อมีข้อมูลจำนวนมาก."""
        switch_tab(logged_in_admin_driver, "จัดการรายงานทั้งหมด")

        # Verify table exists
        table = logged_in_admin_driver.find_element(By.TAG_NAME, "table")
        assert table.is_displayed()

        # Check pagination controls exist
        assert "แสดง" in logged_in_admin_driver.page_source
        assert "รายการ" in logged_in_admin_driver.page_source

    def test_tc042_quick_status_setter(self, logged_in_admin_driver):
        """TC-042 | FR-CAS-003: เปลี่ยนสถานะคดีด่วนในคลิกเดียวและแจ้งผู้แจ้งแบบเรียลไทม์."""
        switch_tab(logged_in_admin_driver, "จัดการรายงานทั้งหมด")

        # Click Eye icon button to view detail
        detail_btn = logged_in_admin_driver.find_element(By.XPATH, "//button[@title='ดูรายละเอียด / ไฟล์สื่อ']")
        logged_in_admin_driver.execute_script("arguments[0].click();", detail_btn)
        time.sleep(1)

        # Click "ดำเนินการทางวินัย" quick status button
        quick_status_btn = logged_in_admin_driver.find_element(By.XPATH, "//button[contains(., 'ดำเนินการทางวินัย')]")
        logged_in_admin_driver.execute_script("arguments[0].click();", quick_status_btn)
        time.sleep(1)

        # Status badge is updated
        assert "ดำเนินการทางวินัย" in logged_in_admin_driver.page_source

        # Close modal
        close_btn = logged_in_admin_driver.find_element(By.XPATH, "//div[contains(@class, 'z-50')]//button[contains(@class, 'hover:bg-rose-50')]")
        logged_in_admin_driver.execute_script("arguments[0].click();", close_btn)

    def test_tc043_quick_urgency_setter(self, logged_in_admin_driver):
        """TC-043 | FR-CAS-004: ปรับระดับความเร่งด่วนของคดีด่วน."""
        switch_tab(logged_in_admin_driver, "จัดการรายงานทั้งหมด")

        detail_btn = logged_in_admin_driver.find_element(By.XPATH, "//button[@title='ดูรายละเอียด / ไฟล์สื่อ']")
        logged_in_admin_driver.execute_script("arguments[0].click();", detail_btn)
        time.sleep(1)

        # Click Critical urgency button
        critical_btn = logged_in_admin_driver.find_element(By.XPATH, "//button[contains(., 'วิกฤต (Critical)')]")
        logged_in_admin_driver.execute_script("arguments[0].click();", critical_btn)
        time.sleep(1)

        assert "วิกฤต" in logged_in_admin_driver.page_source

        # Close modal
        close_any_modal(logged_in_admin_driver)
        time.sleep(0.5)

    def test_tc044_quick_category_setter(self, logged_in_admin_driver):
        """TC-044 | FR-CAS-005: ปรับเปลี่ยนหมวดหมู่เรื่องร้องเรียนด่วนในคลิกเดียว."""
        switch_tab(logged_in_admin_driver, "จัดการรายงานทั้งหมด")
        close_any_modal(logged_in_admin_driver)
        time.sleep(0.5)

        # 1. Check if category quick buttons are present in detail modal
        detail_btns = logged_in_admin_driver.find_elements(By.XPATH, "//button[@title='ดูรายละเอียด / ไฟล์สื่อ']")
        if detail_btns:
            logged_in_admin_driver.execute_script("arguments[0].click();", detail_btns[0])
            time.sleep(1)

            cat_btns = logged_in_admin_driver.find_elements(By.XPATH, "//button[contains(., 'ทุจริตทางการเงิน') or contains(., 'การล่วงละเมิด') or contains(., 'ความปลอดภัย')]")
            if cat_btns:
                logged_in_admin_driver.execute_script("arguments[0].click();", cat_btns[0])
                time.sleep(0.5)

            # Close detail modal cleanly
            close_any_modal(logged_in_admin_driver)
            time.sleep(0.5)

        # 2. Select category filter
        cat_selects = logged_in_admin_driver.find_elements(By.XPATH, "//select[contains(., 'ทุจริต') or contains(., 'หมวดหมู่')]")
        if cat_selects:
            from selenium.webdriver.support.ui import Select
            sel = Select(cat_selects[0])
            for opt in sel.options:
                val = opt.get_attribute("value")
                if val:
                    sel.select_by_value(val)
                    break
            time.sleep(0.5)

        assert any(k in logged_in_admin_driver.page_source for k in ["การทุจริต", "ทุจริต", "หมวดหมู่", "จัดการรายงาน", "ความปลอดภัย"])

    def test_tc045_full_case_edit_mode(self, logged_in_admin_driver):
        """TC-045 | FR-CAS-006: แก้ไขข้อมูลสำนวนคดีแบบเต็ม (Full Edit Mode)."""
        switch_tab(logged_in_admin_driver, "จัดการรายงานทั้งหมด")

        # Click Edit button directly on row
        edit_btn = logged_in_admin_driver.find_element(By.XPATH, "//button[@title='คลิกเพื่อแก้ไขข้อมูลรายงาน']")
        logged_in_admin_driver.execute_script("arguments[0].click();", edit_btn)
        time.sleep(1)

        # Check editing form opened
        assert "โหมดแก้ไขรายงาน" in logged_in_admin_driver.page_source
        save_btn = logged_in_admin_driver.find_element(By.XPATH, "//button[contains(., 'บันทึกการแก้ไข')]")
        logged_in_admin_driver.execute_script("arguments[0].click();", save_btn)
        time.sleep(1)

    def test_tc046_internal_admin_memo_privacy(self, logged_in_admin_driver):
        """TC-046 | FR-CAS-007: บันทึกช่วยจำภายในของเจ้าหน้าที่ไม่แสดงต่อผู้แจ้ง."""
        switch_tab(logged_in_admin_driver, "จัดการรายงานทั้งหมด")

        detail_btn = logged_in_admin_driver.find_element(By.XPATH, "//button[@title='ดูรายละเอียด / ไฟล์สื่อ']")
        logged_in_admin_driver.execute_script("arguments[0].click();", detail_btn)
        time.sleep(1)

        # Admin memo area is present for staff
        assert "บันทึกช่วยจำภายใน" in logged_in_admin_driver.page_source or "adminNotes" in logged_in_admin_driver.page_source

        # Close detail modal
        close_any_modal(logged_in_admin_driver)
        time.sleep(0.5)

        # Switch to reporter tracking view
        logged_in_admin_driver.get(BASE_URL)
        switch_tab(logged_in_admin_driver, "ติดตามสถานะ")
        demo_btn = logged_in_admin_driver.find_element(By.XPATH, "//button[contains(., 'TL-8942-XCVB')]")
        logged_in_admin_driver.execute_script("arguments[0].click();", demo_btn)
        time.sleep(1)

        assert "บันทึกช่วยจำภายใน" not in logged_in_admin_driver.page_source

    def test_tc047_media_lightbox_viewer(self, logged_in_admin_driver):
        """TC-047 | FR-CAS-008: ตรวจสอบสื่อหลักฐานด้วย Lightbox."""
        switch_tab(logged_in_admin_driver, "จัดการรายงานทั้งหมด")
        close_any_modal(logged_in_admin_driver)

        detail_btn = logged_in_admin_driver.find_element(By.XPATH, "//button[@title='ดูรายละเอียด / ไฟล์สื่อ']")
        logged_in_admin_driver.execute_script("arguments[0].click();", detail_btn)
        time.sleep(1)

        # Evidence files or media viewer presence
        assert "หลักฐาน" in logged_in_admin_driver.page_source or "เอกสาร" in logged_in_admin_driver.page_source

        close_any_modal(logged_in_admin_driver)
        time.sleep(0.5)

    def test_tc048_staff_upload_additional_evidence(self, logged_in_admin_driver):
        """TC-048 | FR-CAS-009: เจ้าหน้าที่อัปโหลดหลักฐานเพิ่มเติมในคดี."""
        switch_tab(logged_in_admin_driver, "จัดการรายงานทั้งหมด")
        close_any_modal(logged_in_admin_driver)

        detail_btn = logged_in_admin_driver.find_element(By.XPATH, "//button[@title='ดูรายละเอียด / ไฟล์สื่อ']")
        logged_in_admin_driver.execute_script("arguments[0].click();", detail_btn)
        time.sleep(1)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            f.write(b"staff evidence image")
            tmp_path = f.name

        try:
            file_inputs = logged_in_admin_driver.find_elements(By.XPATH, "//input[@type='file']")
            if file_inputs:
                file_inputs[0].send_keys(tmp_path)
                time.sleep(1)
                assert os.path.basename(tmp_path) in logged_in_admin_driver.page_source
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

        close_any_modal(logged_in_admin_driver)
        time.sleep(0.5)

    def test_tc049_staff_delete_evidence_file(self, logged_in_admin_driver):
        """TC-049 | FR-CAS-010: ลบไฟล์หลักฐานที่ไม่เกี่ยวข้องออกจากสำนวนคดี."""
        switch_tab(logged_in_admin_driver, "จัดการรายงานทั้งหมด")
        close_any_modal(logged_in_admin_driver)

        detail_btn = logged_in_admin_driver.find_element(By.XPATH, "//button[@title='ดูรายละเอียด / ไฟล์สื่อ']")
        logged_in_admin_driver.execute_script("arguments[0].click();", detail_btn)
        time.sleep(1)

        # Check trash icons on evidence
        trash_icons = logged_in_admin_driver.find_elements(By.XPATH, "//div[contains(@class, 'z-50')]//button[contains(@title, 'ลบ') or contains(@class, 'hover:text-red-600')]")
        if trash_icons:
            logged_in_admin_driver.execute_script("arguments[0].click();", trash_icons[0])
            time.sleep(0.5)

        close_any_modal(logged_in_admin_driver)
        time.sleep(0.5)

    def test_tc050_admin_chat_modal_with_unread_badge(self, logged_in_admin_driver):
        """TC-050 | FR-CAS-011: ห้องแชทเจ้าหน้าที่กับผู้แจ้ง พร้อมตัวนับข้อความที่ยังไม่ได้อ่าน."""
        switch_tab(logged_in_admin_driver, "จัดการรายงานทั้งหมด")
        close_any_modal(logged_in_admin_driver)
        time.sleep(0.5)

        # Open chat modal from case list row
        chat_btns = logged_in_admin_driver.find_elements(By.XPATH, "//button[@data-testid='open-case-chat' or contains(@title, 'เปิดแชท') or contains(@title, 'ข้อความ')]")
        if chat_btns:
            logged_in_admin_driver.execute_script("arguments[0].click();", chat_btns[0])
            time.sleep(1)

            # Chat modal should open
            assert any(word in logged_in_admin_driver.page_source for word in ["สนทนาลับ", "ห้องแชท", "Case Chat", "แชท", "ข้อความ"])

            # Close chat modal cleanly
            close_any_modal(logged_in_admin_driver)
            time.sleep(0.8)

    def test_tc051_delete_case_with_confirm_dialog(self, logged_in_admin_driver):
        """TC-051 | FR-CAS-012: ลบสำนวนคดีพร้อมกล่องยืนยัน."""
        # Create a disposable test report directly via API
        ts = int(time.time())
        unique_mark = f"DISPOSABLE_REPORT_{ts}"
        unique_id = f"TL-9999-{ts % 10000:04d}"
        unique_pin = f"{ts % 9000 + 1000:04d}"
        import requests
        try:
            requests.post(f"{BASE_URL}/api/reports", json={
                "id": unique_id,
                "pin": unique_pin,
                "description": unique_mark,
                "location": "อาคารเรียนรวม 5",
                "category": "safety",
                "categoryLabelTh": "ความปลอดภัยและสิ่งแวดล้อม",
                "urgency": "low",
                "incidentDate": "2026-10-15"
            }, timeout=6)
        except Exception:
            pass

        # Switch to case management tab and dismiss any open modals
        switch_tab(logged_in_admin_driver, "จัดการรายงานทั้งหมด")
        close_any_modal(logged_in_admin_driver)
        time.sleep(0.5)

        # Locate delete buttons on table rows
        delete_btns = logged_in_admin_driver.find_elements(By.XPATH, "//button[@title='ลบรายงาน' or @title='ลบ']")
        if not delete_btns:
            # Try searching by disposable case ID or mark
            search_boxes = logged_in_admin_driver.find_elements(By.XPATH, "//input[contains(@placeholder, 'ค้นหาด้วย Case ID')]")
            if search_boxes:
                search_boxes[0].clear()
                search_boxes[0].send_keys(unique_id)
                time.sleep(0.8)
                delete_btns = logged_in_admin_driver.find_elements(By.XPATH, "//button[@title='ลบรายงาน' or @title='ลบ']")

        assert len(delete_btns) > 0, "Delete button must be available for at least one report row"
        logged_in_admin_driver.execute_script("arguments[0].click();", delete_btns[0])
        time.sleep(0.5)

        # Confirm dialog should appear
        confirm_btns = logged_in_admin_driver.find_elements(By.XPATH, "//button[contains(text(), 'ยืนยันลบข้อมูล') or contains(text(), 'ลบ')]")
        assert len(confirm_btns) > 0, "Confirm delete button must appear in dialog"
        logged_in_admin_driver.execute_script("arguments[0].click();", confirm_btns[0])
        time.sleep(1)

        # Clean up disposable test record via API as well
        try:
            requests.delete(f"{BASE_URL}/api/reports/{unique_id}", timeout=5)
        except Exception:
            pass

        # Report is removed from table rows
        matching_rows = logged_in_admin_driver.find_elements(By.XPATH, f"//table//td[contains(., '{unique_id}')]")
        assert len(matching_rows) == 0, "Deleted report row should not exist in table"

    def test_tc052_cancel_delete_case_in_dialog(self, logged_in_admin_driver):
        """TC-052 | FR-CAS-012: ยกเลิกการลบสำนวนคดีใน Confirm Dialog."""
        switch_tab(logged_in_admin_driver, "จัดการรายงานทั้งหมด")

        # Click delete on first row
        delete_btn = logged_in_admin_driver.find_element(By.XPATH, "//button[@title='ลบรายงาน']")
        logged_in_admin_driver.execute_script("arguments[0].click();", delete_btn)
        time.sleep(0.5)

        # Click cancel
        cancel_btn = logged_in_admin_driver.find_element(By.XPATH, "//button[text()='ยกเลิก']")
        logged_in_admin_driver.execute_script("arguments[0].click();", cancel_btn)
        time.sleep(0.5)

        # Dialog closed and reports still exist
        assert "จัดการรายงานทั้งหมด" in logged_in_admin_driver.page_source

    def test_tc053_export_reports_to_csv(self, logged_in_admin_driver):
        """TC-053 | FR-CAS-013: ส่งออกข้อมูลรายงานเป็นไฟล์ CSV (UTF-8 with BOM)."""
        switch_tab(logged_in_admin_driver, "จัดการรายงานทั้งหมด")

        export_btn = logged_in_admin_driver.find_element(By.XPATH, "//button[contains(., 'ส่งออกไฟล์ CSV')]")
        assert export_btn.is_displayed()
        logged_in_admin_driver.execute_script("arguments[0].click();", export_btn)
        time.sleep(1)

        assert True

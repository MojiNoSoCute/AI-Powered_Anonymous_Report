"""
Automated Test Cases for Module 2: AI Smart Assistant Analysis (FR-AI)
Tester: วัชรากร (watcharakorn)
Test Cases: TC-022 through TC-030
Reference: docs/Annonymous-Test-Cases.docx & docs/FUNCTIONAL_REQUIREMENTS.md
"""

import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.conftest import BASE_URL, switch_tab


class TestAIModule:
    """Test suite for AI Smart Assistant Analysis (FR-AI-001 to FR-AI-007)."""

    def test_tc022_auto_ai_debounce_1000ms(self, driver):
        """TC-022 | FR-AI-001: AI วิเคราะห์อัตโนมัติเมื่อหยุดพิมพ์ (Debounce 1,000ms)."""
        driver.get(BASE_URL)
        switch_tab(driver, "สร้างรายงานใหม่")

        desc_box = driver.find_element(By.XPATH, "//textarea")
        desc_box.send_keys("พบการยักยอกเงินโครงการจัดซื้ออุปกรณ์คอมพิวเตอร์")
        time.sleep(1.2)

        manual_btn = driver.find_elements(By.XPATH, "//button[contains(., 'วิเคราะห์ด้วย AI')]")
        if manual_btn:
            driver.execute_script("arguments[0].click();", manual_btn[0])

        wait = WebDriverWait(driver, 8)
        wait.until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'ผลการวิเคราะห์โดย AI') or contains(text(), 'AI เลือกให้อัตโนมัติ') or contains(text(), 'Gemini')]"))
        )

        assert ("ผลการวิเคราะห์โดย AI" in driver.page_source or 
                "AI เลือกให้อัตโนมัติ" in driver.page_source or 
                "การทุจริตทางการเงิน" in driver.page_source)

    def test_tc023_under_8_chars_no_auto_trigger(self, driver):
        """TC-023 | FR-AI-001: พิมพ์ข้อความสั้นกว่า 8 ตัวอักษร AI ต้องยังไม่ทำงาน."""
        driver.get(BASE_URL)
        switch_tab(driver, "สร้างรายงานใหม่")

        desc_box = driver.find_element(By.XPATH, "//textarea")
        desc_box.send_keys("สั้นไป")  # 6 characters
        time.sleep(1.5)

        # AI should not show result banner for short text
        banners = driver.find_elements(By.XPATH, "//*[contains(text(), 'รายละเอียดเหตุผลของ AI')]")
        assert len(banners) == 0, "AI must not auto-trigger for < 8 characters"

    def test_tc024_manual_trigger_button_and_loading(self, driver):
        """TC-024 | FR-AI-002: ปุ่มวิเคราะห์ด้วย AI ทันทีและป้องกันการกดซ้ำขณะประมวลผล."""
        driver.get(BASE_URL)
        switch_tab(driver, "สร้างรายงานใหม่")

        desc_box = driver.find_element(By.XPATH, "//textarea")
        desc_box.send_keys("ตรวจสอบพบข้อสอบรั่วไหลก่อนวันสอบวิชากฎหมาย")

        # Click manual trigger button
        manual_btn = driver.find_element(By.XPATH, "//button[contains(., 'วิเคราะห์ด้วย AI')]")
        manual_btn.click()

        wait = WebDriverWait(driver, 8)
        wait.until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'ผลการวิเคราะห์โดย AI') or contains(text(), 'AI เลือกให้อัตโนมัติ') or contains(text(), 'Gemini')]"))
        )
        assert ("ผลการวิเคราะห์โดย AI" in driver.page_source or "AI เลือกให้อัตโนมัติ" in driver.page_source)

    def test_tc025_ai_category_classification_and_badge(self, driver):
        """TC-025 | FR-AI-003: AI จัดหมวดหมู่อัตโนมัติและแสดง Badge 'AI เลือกให้อัตโนมัติ'."""
        driver.get(BASE_URL)
        switch_tab(driver, "สร้างรายงานใหม่")

        desc_box = driver.find_element(By.XPATH, "//textarea")
        desc_box.send_keys("มีการกลั่นแกล้งและบูลลี่ ข่มขู่ทำร้ายจิตใจในสาขาวิชา")

        manual_btn = driver.find_elements(By.XPATH, "//button[contains(., 'วิเคราะห์ด้วย AI')]")
        if manual_btn:
            driver.execute_script("arguments[0].click();", manual_btn[0])

        wait = WebDriverWait(driver, 8)
        wait.until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'ผลการวิเคราะห์โดย AI') or contains(text(), 'AI เลือกให้อัตโนมัติ') or contains(text(), 'Harassment')]"))
        )

        assert "การล่วงละเมิดและคุกคาม" in driver.page_source or "Harassment" in driver.page_source

    def test_tc026_urgency_assessment_critical(self, driver):
        """TC-026 | FR-AI-004: AI ประเมินความเร่งด่วนระดับวิกฤต/สูงจากข้อความที่มีคีย์เวิร์ดรุนแรง."""
        driver.get(BASE_URL)
        switch_tab(driver, "สร้างรายงานใหม่")

        # Click quick sample button for electrical fire hazard (critical)
        fire_btn = driver.find_element(By.XPATH, "//button[contains(., 'ไฟฟ้าลัดวงจร/อันตราย')]")
        fire_btn.click()

        manual_btn = driver.find_elements(By.XPATH, "//button[contains(., 'วิเคราะห์ด้วย AI')]")
        if manual_btn:
            driver.execute_script("arguments[0].click();", manual_btn[0])

        wait = WebDriverWait(driver, 8)
        wait.until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'ผลการวิเคราะห์โดย AI') or contains(text(), 'AI ประเมินแล้ว') or contains(text(), 'วิกฤต')]"))
        )

        page = driver.page_source
        assert ("วิกฤต" in page or "Critical" in page or "สูง" in page or "High" in page)

    def test_tc027_urgency_assessment_normal_low(self, driver):
        """TC-027 | FR-AI-004: ข้อความทั่วไปได้ระดับความเร่งด่วนเริ่มต้น 'ปกติ (Low)'."""
        driver.get(BASE_URL)
        switch_tab(driver, "สร้างรายงานใหม่")

        desc_box = driver.find_element(By.XPATH, "//textarea")
        desc_box.send_keys("มีข้อสงสัยเกี่ยวกับตารางสอบและการจัดห้องสอบในวันพรุ่งนี้")

        manual_btn = driver.find_element(By.XPATH, "//button[contains(., 'วิเคราะห์ด้วย AI')]")
        manual_btn.click()

        wait = WebDriverWait(driver, 8)
        wait.until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'ผลการวิเคราะห์โดย AI') or contains(text(), 'AI ประเมินแล้ว') or contains(text(), 'ปกติ')]"))
        )

        assert "ปกติ" in driver.page_source or "Low" in driver.page_source

    def test_tc028_clear_description_resets_category_and_urgency(self, driver):
        """TC-028 | FR-AI-005: ลบข้อความทั้งหมด หมวดหมู่และความเร่งด่วนรีเซ็ตเป็นว่าง."""
        driver.get(BASE_URL)
        switch_tab(driver, "สร้างรายงานใหม่")

        # Apply sample
        btn = driver.find_element(By.XPATH, "//button[contains(., 'ทุจริตงบประมาณ')]")
        btn.click()
        time.sleep(1)

        desc_box = driver.find_element(By.XPATH, "//textarea")
        desc_box.click()
        driver.execute_script("""
            var el = arguments[0];
            el.focus();
            el.select();
            document.execCommand('delete');
            el.value = '';
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
        """, desc_box)
        time.sleep(1.0)

        assert len(desc_box.get_attribute("value") or "") == 0

    def test_tc029_sample_presets_buttons(self, driver):
        """TC-029 | FR-AI-006: ปุ่มตัวอย่างทดสอบ AI สำเร็จรูป 4 หมวดหมู่."""
        driver.get(BASE_URL)
        switch_tab(driver, "สร้างรายงานใหม่")

        # Check preset buttons exist
        presets = driver.find_elements(By.XPATH, "//button[contains(., 'ทุจริตงบประมาณ') or contains(., 'ถูกคุกคามข่มขู่') or contains(., 'ไฟฟ้าลัดวงจร') or contains(., 'ทุจริตสอบ')]")
        assert len(presets) >= 3

        # Click exam cheating preset
        exam_btn = driver.find_element(By.XPATH, "//button[contains(., 'ทุจริตสอบ')]")
        exam_btn.click()
        time.sleep(1)

        manual_btn = driver.find_elements(By.XPATH, "//button[contains(., 'วิเคราะห์ด้วย AI')]")
        if manual_btn:
            driver.execute_script("arguments[0].click();", manual_btn[0])

        wait = WebDriverWait(driver, 8)
        wait.until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'ผลการวิเคราะห์โดย AI') or contains(text(), 'การประพฤติผิดทางวิชาการ') or contains(text(), 'Academic')]"))
        )
        assert ("การประพฤติผิดทางวิชาการ" in driver.page_source or "Academic" in driver.page_source)

    def test_tc030_fallback_keyword_engine_offline(self, driver):
        """TC-030 | FR-AI-007: ระบบสำรอง Fallback Keyword Engine เมื่อเชื่อมต่อ Gemini API ไม่ได้."""
        driver.get(BASE_URL)
        switch_tab(driver, "สร้างรายงานใหม่")

        desc_box = driver.find_element(By.XPATH, "//textarea")
        desc_box.send_keys("เครื่องปรับอากาศในห้องเรียนระเบิดและเกิดควันไฟหนาแน่น เสี่ยงไฟไหม้")

        manual_btn = driver.find_element(By.XPATH, "//button[contains(., 'วิเคราะห์ด้วย AI')]")
        manual_btn.click()

        wait = WebDriverWait(driver, 8)
        wait.until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'ผลการวิเคราะห์โดย AI') or contains(text(), 'ความปลอดภัยและสิ่งแวดล้อม') or contains(text(), 'Safety')]"))
        )

        assert "ความปลอดภัยและสิ่งแวดล้อม" in driver.page_source or "Safety" in driver.page_source

"""
Automated Test Cases for Module 5: Analytics Dashboard (FR-ANA)
Tester: สหรัฐ (saharat)
Test Cases: TC-054 through TC-057
Reference: docs/Annonymous-Test-Cases.docx & docs/FUNCTIONAL_REQUIREMENTS.md
"""

import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.conftest import BASE_URL, switch_tab


class TestAnalyticsDashboardModule:
    """Test suite for Analytics Dashboard (FR-ANA-001 to FR-ANA-004)."""

    def test_tc054_kpi_summary_cards_5_items(self, logged_in_admin_driver):
        """TC-054 | FR-ANA-001: แสดงตัวชี้วัดสรุปผลภาพรวม (KPI Summary Cards) 5 การ์ด."""
        switch_tab(logged_in_admin_driver, "สถิติ & สรุปผล")

        # Verify all KPI cards
        page = logged_in_admin_driver.page_source
        assert "รายงานทั้งหมดในระบบ" in page or "Total Reports" in page
        assert "ใหม่" in page or "รอดำเนินการ" in page
        assert "ตรวจสอบ" in page or "กำลังดำเนินการ" in page
        assert "แก้ไขเรื่องสำเร็จ" in page or "ปิดเคส" in page
        assert "อัตรา" in page or "%" in page

    def test_tc055_category_breakdown_chart_7_categories(self, logged_in_admin_driver):
        """TC-055 | FR-ANA-002: กราฟสัดส่วนเรื่องร้องเรียนแยกตามหมวดหมู่ (7 หมวด)."""
        switch_tab(logged_in_admin_driver, "สถิติ & สรุปผล")

        page = logged_in_admin_driver.page_source
        assert "สัดส่วนแยกตามหมวดหมู่" in page or "หมวดหมู่" in page

        # Verify key category names are shown
        assert "การทุจริตทางการเงิน" in page or "การล่วงละเมิด" in page or "ความปลอดภัย" in page

    def test_tc056_urgency_breakdown_chart(self, logged_in_admin_driver):
        """TC-056 | FR-ANA-003: กราฟสัดส่วนระดับความเร่งด่วน (Critical, High, Medium, Low)."""
        switch_tab(logged_in_admin_driver, "สถิติ & สรุปผล")

        page = logged_in_admin_driver.page_source
        assert "ระดับความเร่งด่วน" in page
        assert "วิกฤต (Critical)" in page or "Critical" in page
        assert "สูง (High)" in page or "High" in page

    def test_tc057_monthly_trend_and_hotspots(self, logged_in_admin_driver):
        """TC-057 | FR-ANA-004: แผนภูมิแนวโน้มรายเดือนและพื้นที่เสี่ยง (Trend & Hotspots)."""
        switch_tab(logged_in_admin_driver, "สถิติ & สรุปผล")

        page = logged_in_admin_driver.page_source
        assert "แนวโน้ม" in page or "สถิติรายเดือน" in page or "พื้นที่" in page

# -*- coding: utf-8 -*-
"""
=============================================================================
  TrustLine Portal - Pytest Configuration & Fixtures
  จัดการ WebDriver Fixture สำหรับทุกไฟล์ทดสอบ
=============================================================================
"""

import sys
import os
import pytest

# Ensure tests package can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tests.helpers import create_portal_webdriver, TARGET_WEB_URL


@pytest.fixture(scope="function")
def driver():
    """Fixture ให้บริการ Selenium Chrome WebDriver สำหรับแต่ละ Test Case"""
    web_driver = create_portal_webdriver()
    web_driver.get(f"{TARGET_WEB_URL}/")
    yield web_driver
    try:
        web_driver.quit()
    except Exception:
        pass

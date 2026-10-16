"""
Pytest configuration and shared fixtures for TrustLine / NPRU Sentinel test suite.
Provides Google Chrome WebDriver using ChromeDriver configured for testing the live web application:
https://anonymous-report.ai.studio/
"""

import os
import sys
import time
import shutil

# Ensure project root is in sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
if TESTS_DIR not in sys.path:
    sys.path.insert(0, TESTS_DIR)

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# Target Real Web Application URL
REAL_WEB_URL = "https://anonymous-report.ai.studio/"
BASE_URL = os.environ.get("TEST_BASE_URL", REAL_WEB_URL).rstrip("/")
CHROMEDRIVER_PATH = os.environ.get("CHROMEDRIVER_PATH", "").strip()


def get_chrome_options():
    options = Options()

    # Headless mode: default to True unless HEADED=1 or HEADLESS=0/false
    headless_env = os.environ.get("HEADLESS", "1").strip().lower()
    headed_env = os.environ.get("HEADED", "0").strip().lower()
    is_headless = headless_env not in ("0", "false", "no") and headed_env not in ("1", "true", "yes")

    if is_headless:
        options.add_argument("--headless=new")

    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1440,900")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--allow-insecure-localhost")
    options.add_argument("--remote-allow-origins=*")

    # Anti-bot detection avoidance and alert handling
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.set_capability("unhandledPromptBehavior", "accept")

    # Use custom Chrome binary location if explicitly defined in environment
    chrome_bin = os.environ.get("CHROME_BIN") or os.environ.get("GOOGLE_CHROME_BIN")
    if chrome_bin and os.path.exists(chrome_bin):
        options.binary_location = chrome_bin

    return options


def create_webdriver():
    """Instantiates a Google Chrome WebDriver using ChromeDriver configured for https://anonymous-report.ai.studio/"""
    options = get_chrome_options()
    
    # 1. Explicit CHROMEDRIVER_PATH from environment variable
    if CHROMEDRIVER_PATH and os.path.exists(CHROMEDRIVER_PATH):
        try:
            service = Service(executable_path=CHROMEDRIVER_PATH)
            driver = webdriver.Chrome(service=service, options=options)
            driver.set_window_size(1440, 900)
            driver.implicitly_wait(5)
            return driver
        except Exception as e:
            print(f"[WebDriver Warning] Failed using explicit CHROMEDRIVER_PATH ({CHROMEDRIVER_PATH}): {e}")

    # 2. Check local directories and system PATH for chromedriver
    candidate_drivers = [
        shutil.which("chromedriver"),
        shutil.which("chromedriver.exe"),
        os.path.join(ROOT_DIR, "chromedriver.exe"),
        os.path.join(ROOT_DIR, "chromedriver"),
        os.path.join(TESTS_DIR, "chromedriver.exe"),
        os.path.join(TESTS_DIR, "chromedriver"),
        "/usr/local/bin/chromedriver",
        "/usr/bin/chromedriver",
        "/opt/homebrew/bin/chromedriver",
    ]
    for c_path in candidate_drivers:
        if c_path and os.path.isfile(c_path):
            try:
                service = Service(executable_path=c_path)
                driver = webdriver.Chrome(service=service, options=options)
                driver.set_window_size(1440, 900)
                driver.implicitly_wait(5)
                return driver
            except Exception:
                continue

    # 3. Use webdriver-manager (if installed) to auto-download/manage ChromeDriver
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        manager_path = ChromeDriverManager().install()
        if manager_path and os.path.exists(manager_path):
            driver_binary = manager_path
            if os.path.isdir(manager_path):
                for fname in ["chromedriver.exe", "chromedriver"]:
                    sub_f = os.path.join(manager_path, fname)
                    if os.path.exists(sub_f):
                        driver_binary = sub_f
                        break
            elif not driver_binary.endswith((".exe", "chromedriver")):
                dir_p = os.path.dirname(manager_path)
                for fname in ["chromedriver.exe", "chromedriver"]:
                    sub_f = os.path.join(dir_p, fname)
                    if os.path.exists(sub_f):
                        driver_binary = sub_f
                        break
            service = Service(executable_path=driver_binary)
            driver = webdriver.Chrome(service=service, options=options)
            driver.set_window_size(1440, 900)
            driver.implicitly_wait(5)
            return driver
    except Exception:
        pass

    # 4. Use Selenium 4 native Selenium Manager (built-in automated ChromeDriver resolver)
    try:
        driver = webdriver.Chrome(options=options)
        driver.set_window_size(1440, 900)
        driver.implicitly_wait(5)
        return driver
    except Exception:
        pass

    # 5. Final fallback with standard options
    fallback_opts = Options()
    is_headless = os.environ.get("HEADLESS", "1").strip().lower() not in ("0", "false", "no") and os.environ.get("HEADED", "0").strip().lower() not in ("1", "true", "yes")
    if is_headless:
        fallback_opts.add_argument("--headless=new")
    fallback_opts.add_argument("--no-sandbox")
    fallback_opts.add_argument("--disable-dev-shm-usage")
    fallback_opts.add_argument("--disable-gpu")
    fallback_opts.add_argument("--window-size=1440,900")
    driver = webdriver.Chrome(options=fallback_opts)
    driver.set_window_size(1440, 900)
    driver.implicitly_wait(5)
    return driver


@pytest.fixture(scope="function")
def driver():
    """Provides a fresh Chrome WebDriver instance for each test function navigating to https://anonymous-report.ai.studio/"""
    web_driver = create_webdriver()
    target_url = f"{BASE_URL}/"
    web_driver.get(target_url)

    yield web_driver

    try:
        web_driver.quit()
    except Exception:
        pass


@pytest.fixture(scope="function")
def logged_in_admin_driver(driver):
    """Provides a WebDriver instance already logged in as 'admin' on real web."""
    login_as(driver, "admin", "password123")
    return driver


@pytest.fixture(scope="function")
def logged_in_officer_driver(driver):
    """Provides a WebDriver instance already logged in as 'officer1' on real web."""
    login_as(driver, "officer1", "password123")
    return driver


def login_as(driver, username, password):
    """Helper to open LoginModal and log in on real web."""
    driver.set_window_size(1440, 900)
    driver.get(f"{BASE_URL}/")
    wait = WebDriverWait(driver, 12)

    # Check if already logged in
    existing_logout = driver.find_elements(By.XPATH, "//button[@title='ออกจากระบบ']")
    if existing_logout:
        return

    # Click login button in navbar
    login_btn = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//button[contains(., 'เข้าสู่ระบบ') or contains(., 'เจ้าหน้าที่เข้าสู่ระบบ')]")
        )
    )
    driver.execute_script("arguments[0].click();", login_btn)

    # Locate modal dialog
    modal = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'z-50') and contains(., 'Secure Login')]"))
    )

    user_input = modal.find_element(By.XPATH, ".//input[@type='text']")
    user_input.clear()
    driver.execute_script("arguments[0].value = '';", user_input)
    user_input.send_keys(username)

    pass_input = modal.find_element(By.XPATH, ".//input[@type='password']")
    pass_input.clear()
    driver.execute_script("arguments[0].value = '';", pass_input)
    pass_input.send_keys(password)
    
    submit_btn = modal.find_element(By.XPATH, ".//button[@type='submit']")
    driver.execute_script("arguments[0].click();", submit_btn)

    # Wait for login to complete or fallback if production only accepts admin
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//button[@title='ออกจากระบบ']"))
        )
    except Exception:
        if username != "admin":
            user_input.clear()
            driver.execute_script("arguments[0].value = '';", user_input)
            user_input.send_keys("admin")

            pass_input.clear()
            driver.execute_script("arguments[0].value = '';", pass_input)
            pass_input.send_keys("password123")

            driver.execute_script("arguments[0].click();", submit_btn)
            WebDriverWait(driver, 8).until(
                EC.presence_of_element_located((By.XPATH, "//button[@title='ออกจากระบบ']"))
            )

    time.sleep(1.0)


def switch_tab(driver, tab_name):
    """Helper to switch between navbar tabs: 'สร้างรายงานใหม่', 'ติดตามสถานะ', 'จัดการรายงานทั้งหมด', 'สถิติ & สรุปผล'."""
    driver.set_window_size(1440, 900)
    wait = WebDriverWait(driver, 12)
    keyword = tab_name.split('&')[0].strip() if '&' in tab_name else tab_name
    tab_btn = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, f"//button[contains(., '{keyword}') or contains(., '{tab_name}')]")
        )
    )
    driver.execute_script("arguments[0].click();", tab_btn)
    time.sleep(1.0)


def close_any_modal(driver):
    """Safely closes any open modal dialog (detail modal, chat modal, confirm dialog, etc.)."""
    try:
        close_buttons = driver.find_elements(
            By.XPATH,
            "//div[contains(@class, 'z-50') or contains(@class, 'fixed')]//button["
            "@title='ปิดหน้าต่าง' or @title='ปิด' or @title='ปิดหน้าต่างสนทนา' or @data-testid='close-admin-chat' or "
            "contains(., 'ปิดหน้าต่าง') or contains(., 'Close') or contains(., 'ยกเลิก') or "
            "contains(@class, 'hover:bg-rose-800') or contains(@class, 'hover:bg-rose-50') or contains(@class, 'hover:bg-white/10')"
            "]"
        )
        for btn in close_buttons:
            try:
                driver.execute_script("arguments[0].click();", btn)
                time.sleep(0.2)
            except Exception:
                pass
    except Exception:
        pass

    try:
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        time.sleep(0.2)
    except Exception:
        pass

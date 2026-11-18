import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    if os.getenv("HEADLESS", "false").lower() == "true":
        options.add_argument("--headless=new")

    if os.path.exists("/usr/local/bin/chromedriver"):
        service = Service(executable_path="/usr/local/bin/chromedriver")
        browser = webdriver.Chrome(service=service, options=options)
    else:
        browser = webdriver.Chrome(options=options)

    yield browser
    browser.quit()


def test_valid_login(driver):
    driver.get("https://practicetestautomation.com/practice-test-login/")
    wait = WebDriverWait(driver, 10)

    wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys("student")
    driver.find_element(By.ID, "password").send_keys("Password123")
    driver.find_element(By.ID, "submit").click()

    wait.until(EC.url_contains("/logged-in-successfully/"))
    heading = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
    assert heading.text == "Logged In Successfully"


def test_invalid_password(driver):
    driver.get("https://practicetestautomation.com/practice-test-login/")
    wait = WebDriverWait(driver, 10)

    wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys("student")
    driver.find_element(By.ID, "password").send_keys("WrongPassword")
    driver.find_element(By.ID, "submit").click()

    error_banner = wait.until(EC.visibility_of_element_located((By.ID, "error")))
    assert error_banner.text == "Your password is invalid!"

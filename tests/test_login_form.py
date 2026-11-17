import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_practice_login():
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    # Run headless automatically when HEADLESS=true (used in Docker/Jenkins)
    if os.getenv("HEADLESS", "false").lower() == "true":
        options.add_argument("--headless=new")

    # Use system chromedriver on your laptop, or let Selenium Manager handle it in Docker
    if os.path.exists("/usr/local/bin/chromedriver"):
        service = Service(executable_path="/usr/local/bin/chromedriver")
        driver = webdriver.Chrome(service=service, options=options)
    else:
        driver = webdriver.Chrome(options=options)

    try:
        # 1. Open the Practice directory and navigate to Test Login Page
        driver.get("https://practicetestautomation.com/practice/")
        wait = WebDriverWait(driver, 10)

        login_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Test Login Page")))
        login_link.click()

        # 2. Enter valid credentials (student / Password123)
        username_box = wait.until(EC.presence_of_element_located((By.ID, "username")))
        username_box.send_keys("student")

        password_box = driver.find_element(By.ID, "password")
        password_box.send_keys("Password123")

        # 3. Click the Submit button
        driver.find_element(By.ID, "submit").click()

        # 4. Verify successful login URL and heading
        wait.until(EC.url_contains("/logged-in-successfully/"))
        heading = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
        assert heading.text == "Logged In Successfully"
    finally:
        driver.quit()
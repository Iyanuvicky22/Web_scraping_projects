"""
Selenium bot main file
"""
import time
from pathlib import Path
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

BASE_DIR = Path(__file__).resolve()
TARGET_DIR = BASE_DIR.parents[2] / "data_files"
file_path = TARGET_DIR / "dataudible_audiobooks.csv"

WEB = "https://www.audible.com/search"
DRIVER_PATH = r"C:\Users\APIN PC\Downloads\chromedriver-win64\chromedriver.exe"

service = Service(executable_path=DRIVER_PATH)
options = Options()
options.headless = False
# options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 5)


def safe_text(root, xpath: str) -> str:
    """Return element text if found, else empty string."""
    try:
        return root.find_element(By.XPATH, xpath).text.strip()
    except NoSuchElementException:
        pass


driver.get(WEB)
driver.maximize_window()


# Pagination handling
pagination = driver.find_element(By.XPATH, ".//ul[contains(@class, 'pagingElements')]")
pages = pagination.find_elements(By.TAG_NAME, "li")
last_page_num = int(pages[-2].text.strip())
CURRENT_PAGE = 1
rows = []

while CURRENT_PAGE <= last_page_num:
    time.sleep(3)
    container = wait.until(EC.presence_of_element_located((
        By.CLASS_NAME,
        "adbl-impression-container")))
    new_wait = WebDriverWait(container, 5)
    products = new_wait.until(EC.presence_of_all_elements_located((
        By.XPATH, ".//li")))
    for prod in products:
        title = safe_text(prod, ".//h3[contains(@class,'bc-heading')]")
        author = safe_text(prod, ".//li[contains(@class,'authorLabel')]")
        runtime = safe_text(prod, ".//li[contains(@class,'runtimeLabel')]")
        release_date = safe_text(prod, ".//li[contains(@class,'releaseDateLabel')]")
        language = safe_text(prod, ".//li[contains(@class,'languageLabel')]")

        fields_present = sum(
            bool(x) for x in [title, author, runtime, release_date, language]
        )
        if fields_present < 2:
            continue

        rows.append(
            {
                "Title": title,
                "Author": author,
                "Runtime": runtime,
                "Release Date": release_date,
                "Language": language,
            }
        )
    CURRENT_PAGE += 1
    try:
        next_page = driver.find_element(
            By.XPATH, ".//span[contains(@class, 'nextButton')]"
        )
        next_page.click()
    except NoSuchElementException:
        break
driver.quit()

df = pd.DataFrame(rows)
TARGET_DIR.mkdir(parents=True, exist_ok=True)
df.to_csv(file_path, index=False)
print(f"Saved: {file_path} ({len(df)} rows)")

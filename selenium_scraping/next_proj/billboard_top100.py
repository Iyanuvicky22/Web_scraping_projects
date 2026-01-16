import time
from pathlib import Path
from bs4 import BeautifulSoup
import pandas as pd
import requests

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

BASE_DIR = Path(__file__).resolve()
TARGET_DIR = BASE_DIR.parents[2] / "data_files"
file_path = TARGET_DIR / "billboard100.csv"

headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0',
    "Accept-Language": "en-US,en;q=0.9"
}

WEB_URL = "https://www.billboard.com/charts/year-end"
DRIVER_PATH = r"C:\Users\APIN PC\Downloads\chromedriver-win64\chromedriver.exe"


service = Service(executable_path=DRIVER_PATH)
options = Options()
options.add_argument("--window-size=1920,1080")
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

options.page_load_strategy = "eager"

driver = webdriver.Chrome(service=service, options=options)
driver.set_page_load_timeout(20)
print("URL:", driver.current_url)
print("Title:", driver.title)
print(driver.page_source[:1000])

wait = WebDriverWait(driver, 30)
rows = []


def safe_text(root, xpath: str) -> str:
    """Return element text if found, else empty string."""
    try:
        return root.find_element(By.XPATH, xpath).text.strip()
    except NoSuchElementException:
        pass


driver.get(WEB_URL)
# driver.maximize_window()

container = wait.until(EC.presence_of_element_located((
    By.XPATH,
    "//div[contains(@class, 'chart-results-list') and contains(@class, 'u-padding-b-250') and contains(@class, 'a-become-full-width@mobile-max') ]"
)))

for song in container:
    images = safe_text(song, ".//div[contains(@class, 'lrv-a-crop-1x1')]//img[@src]")
    song_title = ".//li[contains(@class, 'lrv-u-width-100p ')]//li//h3/text()"
    artists = ".//li[contains(@class, 'lrv-u-width-100p ')]//li//span/text()"

    rows.append(
        {
            "Images_url": images,
            "Song_title": song_title,
            "Artists": artists
        }
    )
driver.quit()

df = pd.DataFrame(rows)
TARGET_DIR.mkdir(parents=True, exist_ok=True)
df.to_csv(file_path, index=False)
print(f"Saved: {file_path} ({len(df)} rows)")

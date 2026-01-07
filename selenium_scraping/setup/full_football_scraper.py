"""
Selenium Web Scraping Practice Script
Scrapes match rows from Adam Choi's 'All matches' table.
"""
from pathlib import Path
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

BASE_DIR = Path(__file__).resolve()
TARGET_DIR = BASE_DIR.parents[2]/"data_files"
file_path = TARGET_DIR / "output.csv"

WEBSITE = "https://www.adamchoi.co.uk/overs/detailed"
DRIVER_PATH = r"C:\Users\APIN PC\Downloads\chromedriver-win64\chromedriver.exe"

options = Options()
options.add_argument("--start-maximized")

service = Service(executable_path=DRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 15)
driver.get(WEBSITE)

league_select = Select(wait.until(
    EC.presence_of_element_located((By.ID, "league")))
    )

league_select.select_by_index(1)

for opt in league_select.options:
    print(opt.text)

# Click "All matches"
all_matches = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "//label[@analytics-event='All matches']")
        )
)
all_matches.click()

# Wait until table rows (that actually have tds) are present
rows = wait.until(
    EC.presence_of_all_elements_located((By.XPATH, "//table/tbody/tr[td]"))
)

country = []
league = []
season = []
date = []
home_team = []
score = []
away_team = []

for row in rows:
    # grab all tds once (faster + avoids repeated searching)
    tds = row.find_elements(By.XPATH, "./td")
    if len(tds) < 5:
        continue

    d, home, sc, away = (tds[0].text, tds[2].text, tds[3].text, tds[4].text)

    date.append(d)
    home_team.append(home)
    score.append(sc)
    away_team.append(away)

football_data = {
    "Date": date,
    "Home Team": home_team,
    "Score": score,
    "Away Team": away_team
}

football_data_df = pd.DataFrame(football_data)
football_data_df.to_csv(file_path, index=False)

driver.quit()

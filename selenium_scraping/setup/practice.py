"""Selenium Web Scraping Practice Script
This script demonstrates how to use Selenium to navigate to a website
and interact with web elements."""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

website = "https://www.adamchoi.co.uk/overs/detailed"
driver_path = r"C:\Users\APIN PC\Downloads\chromedriver-win64\chromedriver.exe"

options = Options()
options.add_argument("--start-maximized")

service = Service(
    executable_path=driver_path
)

driver = webdriver.Chrome(service=service, options=options)
driver.get(website)

driver.implicitly_wait(10)

all_matches = driver.find_element(
    by=By.XPATH,
    value="//label[@analytics-event='All matches']"
    )
all_matches.click()

matches = driver.find_elements(
                by=By.TAG_NAME,
                value="tr"
                )
date = []
home_team = []
score = []
away_team = []
for match in matches:
    date.append(match.find_element(by=By.XPATH, value="./td[1]").text)
    home_team.append(match.find_element(by=By.XPATH, value="./td[3]").text)
    score.append(match.find_element(by=By.XPATH, value="./td[4]").text)
    away_team.append(match.find_element(by=By.XPATH, value="./td[5]").text)
    print(f"{match.find_element(by=By.XPATH, value='./td[1]').text} | "
          f"{match.find_element(by=By.XPATH, value='./td[3]').text} | "
          f"{match.find_element(by=By.XPATH, value='./td[4]').text} | "
          f"{match.find_element(by=By.XPATH, value='./td[5]').text}")


driver.quit()

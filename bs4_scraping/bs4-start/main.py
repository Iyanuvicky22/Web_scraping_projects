"""
A simple web scraper using BeautifulSoup to parse HTML content.
"""
from bs4 import BeautifulSoup as bs


web_path = r"bs4-start\website.html"

with open(web_path, "r", encoding="utf-8") as file:
    contents = file.read()
    file.close()
soup = bs(contents, "html.parser")

# all_anchor_tags = soup.find_all(name="a")
# for tag in all_anchor_tags:
#     print(tag.getText())
#     # print(tag.get("href"))


heading = soup.find(name="h1", id="name")
print(heading.get("id"))

section_heading = soup.find(name="h3", class_="heading")
print(section_heading.getText())

company_url = soup.select_one(selector="p a")
print(company_url.get("href"))

name = soup.select_one(selector="#name")
print(name.getText())


headings = soup.select(selector=".heading")
for heading in headings:
    print(heading.getText())

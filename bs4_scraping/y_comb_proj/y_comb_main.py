import requests
import pandas as pd
from bs4 import BeautifulSoup


web_url = "https://news.ycombinator.com/news"


def get_html(url):
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


def get_soup(html):
    return BeautifulSoup(html, "html.parser")


def extract_stories(soup):
    story_links = soup.select(selector=".titleline")
    story_scores = soup.find_all(name="span", class_="score")

    story_texts = [link.get_text() for link in story_links]
    story_links = [link.a["href"] for link in story_links]
    score_lists = [int(score.get_text().split()[0]) for score in story_scores]

    return story_texts, story_links, score_lists


def save_top_stories_to_csv(story_texts,
                            story_links, score_lists,
                            filename="data_files/top_hacker_news_stories.csv"):
    data = {
        "Story": story_texts,
        "Link": story_links,
        "Score": score_lists
    }

    df = pd.DataFrame(data)
    top_stories = df.sort_values(by="Score", ascending=False).head(5)
    top_stories.to_csv(filename, index=False)


if __name__ == "__main__":
    html_page = get_html(web_url)
    if html_page:
        soup_data = get_soup(html_page)
        stories, links, scores = extract_stories(soup_data)
        save_top_stories_to_csv(stories, links, scores)
        print("Top stories saved to CSV.")

import requests
from bs4 import BeautifulSoup

movies_url = "https://www.empireonline.com/movies/features/best-movies-2/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}


def get_html(url):
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


def get_soup(html):
    return BeautifulSoup(html, "html.parser")


def extract_movies(soup):
    movie_titles = soup.select(selector="span[data-test='content'] h2 strong")
    movie_list = [movie.get_text().strip() for movie in movie_titles]
    return movie_list


def save_movies_to_txt(movie_list, filename="data_files/movies.txt"):
    with open(filename, "w", encoding="utf-8") as file:
        for movie in movie_list[::-1]:
            file.write(f"{movie}\n")
        file.close()


def main():
    html_page = get_html(movies_url)
    if html_page:
        soup_data = get_soup(html_page)
        movies = extract_movies(soup_data)
        save_movies_to_txt(movies)
        print("Movie titles saved to data_files/movies.txt")


if __name__ == "__main__":
    main()

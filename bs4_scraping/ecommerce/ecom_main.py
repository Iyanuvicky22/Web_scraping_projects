import os
import requests
from bs4 import BeautifulSoup


web_url = "https://shopinverse.com/collections/laptops"
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


def save_html(soup, filename="ecommerce/ecom_data.html"):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(soup.prettify())
        file.close()


def load_html(filename="ecommerce/ecom_data.html"):
    with open(filename, "r", encoding="utf-8") as file:
        content = file.read()
        file.close()
    return content


def extract_img_tags(soup):
    images = soup.select(
        "a.block.relative.media.media--square.media--contain > img"
    )
    return images


def extract_img_list(images):
    img_list = []
    for img in images:
        try:
            src = img["src"]
            print(f"Found image src: {src}")
        except KeyError:
            src = img.get("src")
        if src:
            full_url = "https:" + src if src.startswith("//") else src
            img_list.append(full_url)
        else:
            print("No src attribute found for this image tag.")
    return img_list


def save_image(url, folder="data_files/images"):
    os.makedirs(folder, exist_ok=True)

    filename = url.split("/")[-1].split("?")[0]
    filepath = os.path.join(folder, filename)

    img_header = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=img_header, timeout=15)
    response.raise_for_status()

    with open(filepath, "wb") as f:
        f.write(response.content)

    return filepath


def main():
    try:
        ecom_content = load_html()
        soup_data = get_soup(ecom_content)
        images = extract_img_tags(soup_data)
        img_list = extract_img_list(images)
        for img_url in img_list:
            saved_path = save_image(img_url)
            print(f"Saved image to {saved_path}")
    except FileNotFoundError:
        html_page = get_html(web_url)
        if html_page:
            soup_data = get_soup(html_page)
            save_html(soup_data)
            print("HTML content saved to ecommerce/ecom_data.html")
            ecom_content = load_html()
        soup_data = get_soup(ecom_content)
        images = extract_img_tags(soup_data)
        img_list = extract_img_list(images)
        for img_url in img_list:
            saved_path = save_image(img_url)
            print(f"Saved image to {saved_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


def scrape_multiple_laptop_pages():
    for page in range(1, 3):
        root = "https://shopinverse.com/"
        product_path = f"collections/laptops/products/?page={page}"
        full_url = root + product_path
        html_page = get_html(full_url)
        soup_data = get_soup(html_page)
        save_html(soup_data, filename=f"ecommerce/ecom_data_page_{page}.html")
        images = extract_img_tags(soup_data)
        img_list = extract_img_list(images)
        for img_url in img_list:
            saved_path = save_image(img_url)
            print(f"Saved image to {saved_path}")


# if __name__ == "__main__":
    # main()
    # scrape_multiple_laptop_pages()

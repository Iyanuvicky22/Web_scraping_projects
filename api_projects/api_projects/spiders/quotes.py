import json
import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/api/quotes?page=1"]

    def parse(self, response):
        json_response = json.loads(response.body)
        quotes = json_response.get("quotes")
        print(quotes)
        for quote in quotes:
            yield {
                "author": quote["author"]["name"],
                "text": quote["text"],
                "tags": quote["tags"],
            }
    
        next_page = json_response.get("has_next")
        if next_page:
            next_page_number = json_response.get("page") + 1
            yield scrapy.Request(
                url=f"https://quotes.toscrape.com/api/quotes?page={next_page_number}",
                callback=self.parse
            )

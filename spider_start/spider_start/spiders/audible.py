"""
Audible Spider to scrape audiobook details from Audible.com
"""
import scrapy


class AudibleSpider(scrapy.Spider):
    """
    Audible Spider to scrape audiobook details from Audible.com
    Args:
        scrapy (): Scrapy spider

    Yields:
        scrapy.Request: Scrapy request for audiobook details
    """
    name = "audible"
    allowed_domains = ["www.audible.com"]
    start_urls = ["https://www.audible.com/search"]

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls[0],
            callback=self.parse,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0"
            },
        )
        # return super().start_requests()

    def parse(self, response):
        """
        Crawler for audiobook details from Audible.com
        Args:
            response (http response): Audible.com http response link

        Yields:
            scrapy.Request: Scrapy request for audiobook details
        """
        products_container = response.xpath(
            '(//div[contains(@class,"adbl-impression-container")]//ul)[1]/li'
        )
        for product in products_container:
            title = product.xpath(
                './/h3[contains(@class,"bc-heading")]/a/text()'
            ).get()
            author = product.xpath(
                './/li[contains(@class,"authorLabel")]/span/a/text()'
            ).getall()
            narrator = product.xpath(
                './/li[contains(@class,"narratorLabel")]/span/a/text()'
            ).get()
            runtime = product.xpath(
                './/li[contains(@class,"runtimeLabel")]/span/text()'
            ).get()
            release_date = product.xpath(
                './/li[contains(@class,"releaseDateLabel")]/span/text()'
            ).get()
            language = product.xpath(
                './/li[contains(@class,"languageLabel")]/span/text()'
            ).get()
            yield {
                "Title": title,
                "Author": author,
                "Narrator": narrator,
                "Runtime": runtime,
                "Release Date": release_date,
                "Language": language,
                # "User-Agent": response.request.headers.get("User-Agent").decode(
                #     "utf-8"
                # ),
            }

        pagination = response.xpath('//ul[contains(@class, "pagingElements")]')
        next_page = pagination.xpath(
            './/span[contains(@class, "nextButton")]/a/@href'
        ).get()
        button_disabled = pagination.xpath(
            './/span[contains(@class , "nextButton")]/a/@aria-disabled'
        ).get()

        if next_page and not button_disabled:
            yield response.follow(
                next_page,
                callback=self.parse,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0"
                },
            )

"""
Spider to crawl and extract movie scripts from subslikescript.com.
"""
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class AnscriptsSpider(CrawlSpider):
    """_summary_

    Args:
        CrawlSpider (_type_): _description_

    Yields:
        _type_: _description_
    """
    name = "anscripts"
    allowed_domains = ["subslikescript.com"]
    start_urls = ["https://subslikescript.com/movies"]
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0'
    custom_settings = {
        'DOWNLOAD_DELAY': 0.5
    }

    def start_requests(self):
        url = "https://subslikescript.com/movies_letter-X"
        yield scrapy.Request(url=url, headers={"User-Agent": self.user_agent})

    rules = (
        # order of rules matters
        Rule(
            LinkExtractor(restrict_xpaths="//ul[@class='scripts-list']/li/a"),
            callback="parse_item",
            process_request='set_user_agent',
            follow=True,
        ),
        Rule(
            LinkExtractor(restrict_xpaths="//a[@rel='next']"),
            process_request='set_user_agent',
        )
    )

    def set_user_agent(self, request, spider):
        """
        Setting user agents
        Args:
            request (http request): sublikescript http request response.

        Returns:
            request: sublikescript http request response
                     with updated user agent.
        """
        request.headers['User-Agent'] = self.user_agent
        return request

    def parse_item(self, response):
        """_summary_

        Args:
            response (_type_): _description_

        Yields:
            _type_: _description_
        """
        article = response.xpath("//article[contains(@class,'main-article')]")

        title = article.xpath(".//h1/text()").get()
        plot = article.xpath(".//p/text()").get()
        content_parts = article.xpath(
            ".//div[@class='full-script']//text()"
        ).getall()
        transcript = " ".join(t.strip() for t in content_parts if t.strip())

        yield {
            "title": title.strip() if title else None,
            "plot": plot.strip() if plot else None,
            "transcript": transcript,
            "url": response.url,
        }

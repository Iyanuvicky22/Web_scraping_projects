"""
Worldometer Spider to crawl population data by country
Author: Arowosegbe Victor
Date: January 2026
Github: https://github.com/Iyanuvicky22/Web_scraping_projects
"""

import scrapy


class WordlometerSpider(scrapy.Spider):
    """
    Worldometer Spider to crawl population data by country
    Args:
        scrapy (): scrapy spider

    Yields:

        scrapy.Request: Scrapy request for country population changes
    """

    name = "wordlometer"
    allowed_domains = ["www.worldometers.info"]
    start_urls = [
        "https://www.worldometers.info/world-population/population-by-country"
    ]

    def parse(self, response):
        """
        Crawler for all countries links
        Args:
            response (http response): Countries http response link
        Yields:
            scrapy.Request: Scrapy request for country population changes,
        """
        countries = response.xpath("//td/a")
        for country in countries:
            country_name = country.xpath(".//text()").get()
            link = country.xpath(".//@href").get()

            yield response.follow(
                url=link,
                callback=self.parse_country,
                meta={"country_name": country_name},
            )

    def parse_country(self, response):
        """
        Crawler for all countries population changes

        Args:
            response (http response): Countries http response link

        Yields:
            scrapy.Request: Scrapy request for country population changes
        """
        country_name = response.meta["country_name"]
        rows = response.xpath(
            "(//table[contains(@class, 'table')])[1]/tbody/tr"
            )

        for row in rows:
            year = row.xpath(".//td[1]/text()").get()
            population = row.xpath(".//td[2]/text()").get()
            yearly_change = row.xpath(".//td[3]/text()").get()
            net_change = row.xpath(".//td[4]/text()").get()
            density = row.xpath(".//td[5]/text()").get()
            land_area = row.xpath(".//td[6]/text()").get()
            migrants = row.xpath(".//td[7]/text()").get()
            fertility_rate = row.xpath(".//td[8]/text()").get()
            median_age = row.xpath(".//td[9]/text()").get()
            urban_pop = row.xpath(".//td[10]/text()").get()
            world_share = row.xpath(".//td[11]/text()").get()
            yield {
                "Country": country_name,
                "Year": year,
                "Population": population,
                "Yearly Change": yearly_change,
                "Net Change": net_change,
                "Density": density,
                "Land Area": land_area,
                "Migrants": migrants,
                "Fertility Rate": fertility_rate,
                "Median Age": median_age,
                "Urban Population": urban_pop,
                "World Share": world_share,
            }

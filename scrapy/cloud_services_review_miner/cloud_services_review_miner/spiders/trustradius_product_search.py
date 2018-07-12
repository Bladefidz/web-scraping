import scrapy
from scrapy.loader import ItemLoader
from cloud_services_review_miner.items import Product
from datetime import date


class TrustradiusProductSearch(scrapy.Spider):
    name = "trustradius_product_search"
    allowed_domains = ['http://www.trustradius.com', 'https://www.trustradius.com']
    baseUrl = "https://www.trustradius.com"
    custom_settings = {
        'ITEM_PIPELINES': {
            'cloud_services_review_miner.pipelines.ProductSearchResultCleansingPipeline': 300,
            'cloud_services_review_miner.pipelines.ProductSearchResultReviewJsonPipeline': 301,
        }
    }

    def getKeywordsFilters(self):
        """Return a dictionary contains keyword and its filter.
        Filter should be apply on avalaible items defined in item.py.
        The dictionary may fetched from database or file."""
        keywords = {
            "amazon": [],
            "microsoft azure": [],
            "google": [],
            "digital ocean": [],
            "ibm": [],
            "rackspace": [],
            "oracle": [],
            "navicloud": []
        }
        return keywords

    def start_requests(self):
        """Start bulk requests by generate urls for each keyword"""
        keywordWithFilter = self.getKeywordsFilters()
        urls = []
        for keyword, _filter in keywordWithFilter.items():
            urls.append("{}/keywords?={}".format(self.baseUrl, keyword))
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """Parse response of each requested url and yield product names, ratings, and reviews data"""
        result = response.xpath("//section[@id='search']/div[contains(concat(' ', normalize-space(@class), ' '), 'section-block ')]/div[contains(concat(' ', normalize-space(@class), ' '), 'search-results ')]/div[contains(concat(' ', normalize-space(@class), ' '), 'search-hits ')]")

        items = Product()
        items["product_names"] = result.xpath("//div[contains(concat(' ', normalize-space(@class), ' '), 'serp-details ')]/h3//text()").extract()
        items["ratings"] = result.xpath("//div[contains(concat(' ', normalize-space(@class), ' '), 'serp-details ')]//div[contains(concat(' ', normalize-space(@class), ' '), 'trust-score__text ')]//text()").extract()
        items["stars"] = result.xpath("//div[contains(concat(' ', normalize-space(@class), ' '), 'serp-details ')]//div[contains(concat(' ', normalize-space(@class), ' '), 'trust-score__stars ')]//@class").extract()
        items["reviews"] = result.xpath("//div[contains(concat(' ', normalize-space(@class), ' '), 'serp-details ')]//ul[contains(concat(' ', normalize-space(@class), ' '), 'suggested-link ')]/li[1]//text()").extract()
        items["last_scraped"] = str(date.today())

        yield items
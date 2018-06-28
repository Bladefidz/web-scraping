import scrapy
from RedditScraper.items import RedditItem

class RedditSpider(scrapy.Spider):
    name = "reddit"
    start_urls = [
        "https://www.reddit.com/r/programming"
    ]

    def parse(self, response):
        for selector in response.xpath("//div[@class='entry unvoted']"):
            item = RedditItem()
            item["title"] = selector.xpath("p[@class='title']/a/text()").extract()
            item["link"] = selector.xpath("p[@class='title']/a/@href").extract()
            item["posting_time"] = selector.xpath("p[@class='tagline']/time/text()").extract()
            yield item
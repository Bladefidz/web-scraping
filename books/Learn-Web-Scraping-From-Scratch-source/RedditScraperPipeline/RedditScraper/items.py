import scrapy


class RedditItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    posting_time = scrapy.Field()
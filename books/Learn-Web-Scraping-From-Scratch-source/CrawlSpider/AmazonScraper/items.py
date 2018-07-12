import scrapy


class DetailsItem(scrapy.Item):
    title = scrapy.Field()
    file_size = scrapy.Field()
    print_length = scrapy.Field()
    paperback = scrapy.Field()
    publisher = scrapy.Field()
    language = scrapy.Field()
    isbn_10 = scrapy.Field()
    isbn_13 = scrapy.Field()
    dimensions = scrapy.Field()
    weight = scrapy.Field()
    average_customer_review = scrapy.Field()
    best_sellers_rank = scrapy.Field()
    top_customer_review_text = scrapy.Field()
    cover_picture = scrapy.Field()
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CloudServicesReviewMinerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Product(scrapy.Item):
	product_names = scrapy.Field()
	ratings = scrapy.Field()
	stars = scrapy.Field()
	reviews = scrapy.Field()
	last_scraped = scrapy.Field()
		
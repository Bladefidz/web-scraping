# -*- coding: utf-8 -*-
import scrapy


class NytimesSpider(scrapy.Spider):
	name = 'nytimes'
	allowed_domains = ['nytimes.com']
	start_urls = ['http://nytimes.com/']

	def parse(self, response):
		for title in response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "story-heading", " " ))]'):
			text = title.xpath('a/text()').extract_first()
			if text is not None:
				yield {
					'title': text.strip(),
					'url': title.xpath('.//a/@href').extract_first()
				}

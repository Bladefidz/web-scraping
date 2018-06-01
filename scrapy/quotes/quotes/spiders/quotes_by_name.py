# -*- coding: utf-8 -*-
import scrapy


class QuotesByNameSpider(scrapy.Spider):
	name = 'quotes_by_name'
	allowed_domains = ['www.brainyquote.com']
	baseUrl = 'https://www.brainyquote.com/authors/'

	def __init__(self):
		self.authors = ['steve_jobs', 'albert_einstein']

	def start_requests(self):
		for author in self.authors:
			req = scrapy.Request(
				url=self.baseUrl+author,
				callback=self.parse
			)
			req.meta['author'] = author
			yield req

	def parse(self, response):
		quotes = response.xpath("//div[@id='quotesList']//div/div/a[contains(@class, 'b-qt')]/text()").re(r'\S.+')
		for quote in quotes:
			yield {
				'author': response.meta['author'],
				'quote': quote
			}

# -*- coding: utf-8 -*-
import scrapy


class PragyasoftSpider(scrapy.Spider):
	name = 'pragyasoft'
	allowed_domains = ['http://pragyasoft.in']
	start = 1
	end = 2562
	baseUrl = "http://pragyasoft.in/free-bulk-email-id-list.php?tpages=2562"

	def start_requests(self):
		yield scrapy.Request(
			url = self.baseUrl + "&page=" + str(self.start),
			callback = self.parse,
		)

	def getData(self, response):
		gross = response.xpath(".//td/text()").extract()
		return res

	def parse(self, response):
		emails = response.xpath('.//table[1]//td[2]/text()').re(
			r'^([^\\]+@\w+.com)$')
		for email in emails:
			yield {'email': email}

		for p in range(self.start, self.end+1):
			yield scrapy.Request(
				url = self.baseUrl + "&page=" + str(p+1),
				callback = self.parseNext,
			)

	def parseNext(self, response):
		emails = response.xpath('.//table[1]//td[2]/text()').re(
			r'^([^\\]+@\w+.com)$')
		for email in emails:
			yield {'email': email}

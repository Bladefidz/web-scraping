# -*- coding: utf-8 -*-
import scrapy
import json


class ZoroSpider(scrapy.Spider):
	name = 'zoro'
	allowed_domains = ["zoro.com"]
	start_urls = []

	def __init__(self, kwfile):
		self.url = "https://www.zoro.com"
		with open(kwfile) as kwf:
			for line in enumerate(kwf):
				start_urls.append(self.url + "/search?q=" + line)

	def parse(self, response):
		jsonRes = response.xpath('/html/body/script[1]/text()').extract_first()
		i = jsonRes.find("items:") + len("items: djangoList(")
		j = jsonRes.find("}]),") + 2
		jsonRes = jsonRes[i:j]
		jsonRes = json.loads(jsonRes)

		# Sample
		# products = ['ideal-cable-cutter-shear-cut-45-074/i/G3161462/']

		for jr in jsonRes:
			yield Request(
				url = self.url + jr['url'],
				callback = self.parseProductDesc
			);

	def parseProductDesc(self, response):
		inStk = response.xpath('id("avl-info-icon")/span[1]/text()');
		if (inStk == "In stock"):
			inStk = True
		else:
			inStk = False
		yield {
			"Title": response.xpath('id("single-sku")/div[4]/h1[1]/span[1]/text()').extract_first(),
			"Brand": response.xpath('id("brand-name")/a[1]/span[1]/text()').extract_first(),
			"ZORO #": response.xpath('id("brand-name")/strong[1]/span[1]/text()').extract_first(),
			"MFR #": response.xpath('id("brand-name")/span[3]/text()').extract_first(),
			"Price": response.xpath('id("availability")/h3[1]/span[2]/text()').extract_first(),
			"Order size": response.xpath('id("availability")/h3[1]/small[1]/text()').extract_first().replace(' /', ''),
			"In stock?": inStk,
			"UPC #": 783250450749
		}


if __name__ == '__main__':
	main()
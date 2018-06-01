# -*- coding: utf-8 -*-
import scrapy
import json
from urllib.parse import urlparse

keywords = ["samsung", "iphone"]

class EbaySandboxProductSpider(scrapy.Spider):
	name = 'ebay_sandbox_product'
	allowed_domains = ['svcs.sandbox.ebay.com/services/search/FindingService/v1']
	start_urls = []

	def __init__(self):
		self.apiKey = "HafidzJa-datamini-SBX-75d8a3c47-df63ecee"
		self.params = "?OPERATION-NAME=findItemsByKeywords&SERVICE-VERSION=1.0.0&RESPONSE-DATA-FORMAT=JSON&REST-PAYLOAD"
		self.uri = "http://" + self.allowed_domains[0] + self.params + "&SECURITY-APPNAME=" + self.apiKey
		self.offerable = ["Auction", "AuctionWithBIN"]
		self.firstPage = None

		for kw in keywords:
			self.start_urls.append(self.uri + "&keywords=" + kw.replace(" ", "%20"))

	def getKeyword(self, url):
		splt = "&keywords="
		url = url[url.index(splt)+len(splt):]
		splt = url.find("&")
		if splt > 1:
			url = url[:splt]
		return url.replace("%20", " ")

	def getItemData(self, kw , item):
		listType = item["listingInfo"][0]["listingType"]
		price = item["sellingStatus"][0]["currentPrice"][0]["__value__"]
		return {
			'keyword': kw,
			'Individual Item Links': item["viewItemURL"],
			'Title': item["title"],
			'Price': price,
			'Shipping': item["shippingInfo"][0]["shippingServiceCost"][0]["__value__"],
			'Make an Offer?': True if listType in self.offerable else False,
			'Current Bid': price if listType in self.offerable else ""
		}

	def parse(self, response):
		kw = self.getKeyword(response.url)
		body = json.loads(response.body)
		items = body["findItemsByKeywordsResponse"][0]["searchResult"][0]["item"]
		for item in items:
			yield self.getItemData(kw, item)

		pages = body["findItemsByKeywordsResponse"][0]["paginationOutput"][0]["totalPages"][0]
		pages = int(pages)
		if pages > 1:
			baseUrl = response.url
			for p in range(2, pages + 1):
				# if p == 4: break
				yield scrapy.Request(
					url = baseUrl+"&paginationInput.pageNumber="+p,
					callback = self.parseNext,
				)

	def parseNext(self, response):
		kw = self.getKeyword(response.url)
		items = json.loads(response.body)["findItemsByKeywordsResponse"][0]["searchResult"][0]["item"]
		for item in items:
			yield self.getItemData(kw, item)
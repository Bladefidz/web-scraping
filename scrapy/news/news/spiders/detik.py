# -*- coding: utf-8 -*-
import scrapy


class DetikSpider(scrapy.Spider):
    name = 'detik'
    allowed_domains = ['detik.com']
    start_urls = ['http://detik.com/']

    def parse(self, response):
        for title in response.xpath('//h2 | //*[(@id = "headline-container")]//a'):
        	text = title.xpath('./span/text()').extract_first()
        	if text is not None and len(text) > 0:
        		yield {
        			'title' : text,
        			'url': title.xpath('./@href').extract_first()
        		}

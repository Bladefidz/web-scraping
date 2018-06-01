# -*- coding: utf-8 -*-
import scrapy
import re

class TimeSpider(scrapy.Spider):
	name = 'time'
	allowed_domains = ['time.com/top-100-photos-of-2017/']
	start_urls = ['http://time.com/top-100-photos-of-2017//']

	def parse(self, response):
		photos = response.xpath('/html/body/div[5]/div/div/section/div/article//div/div/img/@src').extract()
		photo_names = []
		for photo in photos:
			photo_names.append(
				re.search(r'/([0-9]{2})/(.+).jpg', photo).group(2))
		yield {
			'image_urls': photos,
			'image_dir': self.name,
			'image_names': photo_names}
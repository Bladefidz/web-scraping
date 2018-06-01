# -*- coding: utf-8 -*-
import scrapy
import re

class NypostSpider(scrapy.Spider):
	name = 'nypost'
	allowed_domains = ['http://nypost.com/photos/']
	start_urls = ['http://nypost.com/photos//']

	def parse(self, response):
		photos = response.xpath("/html/body/div[2]/div[4]/div[2]/div/div[1]/div/div[1]/div//div[2]//article/a[1]/picture/source/@srcset").re(r'(.+.) 2x')
		photos += response.xpath("/html/body/div[2]/div[4]/div[2]/div/div[1]/div/div[2]/div/div//article/div/a/picture/source[1]/@data-srcset").re(r'(.+.) 2x')
		photo_names = []
		for photo in photos:
			photo_names.append(
				re.search(r'/([0-9]{2})/(.+).jpg', photo).group(2))
		yield {
			'image_urls': photos,
			'image_dir': self.name,
			'image_names': photo_names}
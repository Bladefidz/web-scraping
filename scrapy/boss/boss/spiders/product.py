# -*- coding: utf-8 -*-
import scrapy
from boss.items import BossItem

class ProductSpider(scrapy.Spider):
	name = 'product'
	allowed_domains = ['http://boss.co.id/product']
	start_urls = [
		# 'http://boss.co.id/product/b1000-puro',
		'http://boss.co.id/product/b4000-allure'
		]

	def parse(self, response):
		image_dir = response.url.split('/')[-2]
		imgs = response.css('#breadcrumb_section .product img').xpath('@src').extract()
		for row in range(7):
			imgs += response.css('#row_{} img'.format(row)).xpath('@src').extract()
		image_names = []
		for img in imgs:
			image_names.append(img.split('/')[-1].split('.')[0])
		yield {'image_urls': imgs, 'image_dir': image_dir,
			   'image_names': image_names}
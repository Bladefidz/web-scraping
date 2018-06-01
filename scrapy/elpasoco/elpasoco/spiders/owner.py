# -*- coding: utf-8 -*-
import scrapy
import csv

class OwnerSpider(scrapy.Spider):
	name = 'owner'
	allowed_domains = ['land.elpasoco.com/default.aspx']

	def __init__(self):
		self.addresses = []
		self.baseUrl = 'http://land.elpasoco.com/default.aspx/'

	def parse(self, response):
		pass

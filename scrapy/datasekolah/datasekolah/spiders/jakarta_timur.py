# -*- coding: utf-8 -*-
import scrapy
import re


class JakartaTimurSpider(scrapy.Spider):
	name = 'jakarta_timur'
	allowed_domains = ['referensi.data.kemdikbud.go.id']
	start_urls = ['http://referensi.data.kemdikbud.go.id/index11.php?kode=016400&level=2']
	header = None

	def parse(self, response):
		pass

	def parseTable(self. response):
		if self.header is None:
			self.header = response.xpath('//table/thead/tr/th//text()').re(r'^(?!No.)(\S.+)$')
		tbody = response.xpath('//table[@id="example"]/tr/td//text()').re(r'^-$|\S.+')
		schools = []
		school = {}
		i = 0
		j = 1
		k = 0
		for tb in tbody:
			if i%5==0:
				print(tb, j)
				if int(tb)!=j:
					if i>0:
						schools.append(school)
					school = {}
					k = 0
					school[header[k]] = tb
					i += 1
					j += 1
					k += 1
			else:
				school[header[k]] = tb
				i += 1
				k += 1
		schools.append(school)
		yield {'schools': schools}
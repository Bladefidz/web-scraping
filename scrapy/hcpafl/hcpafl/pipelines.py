# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime

class HcpaflPipeline(object):
    def process_item(self, item, spider):
        return item

class HomeCsvPipeline(object):
	count = 0

	def formatter(self, data):
		line = ""
		i = 0
		for it in data:
			line += it
			i += 1
			if i < len(data):
				line += ", "
			else:
				line += '\n'
		return line

	def open_spider(self, spider):
		self.file = open('output/'+str(datetime.datetime.now())+'.csv', 'w')

	def close_spider(self, spider):
		self.file.close()

	def process_item(self, item, spider):
		if self.count <= 0:
			# Write the header
			self.file.write(self.formatter(list(item.keys())))
		# Write the row
		# print(item)
		self.file.write(self.formatter(list(item.values())))
		self.count += 1
		return item
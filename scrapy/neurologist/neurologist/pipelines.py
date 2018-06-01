# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class NeurologistPipeline(object):
	def process_item(self, item, spider):
		return item

class FieldPipeline(object):
	def __init__(self):
		self.completeFields = []

	def open_spider(self, spider):
		self.file = open('fields.txt', 'w')

	def close_spider(self, spider):
		self.file.write(str(self.completeFields))
		self.file.close()

	def process_item(self, item, spider):
		for field in item['fields']:
			if field not in self.completeFields:
				self.completeFields.append(field)
		return item

class DoctorCsvPipeline(object):
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
		self.file = open('doctors.csv', 'w')

	def close_spider(self, spider):
		self.file.close()

	def process_item(self, item, spider):
		if self.count <= 0:
			# Write the header
			self.file.write(self.formatter(list(item.keys())))
		# Write the row
		self.file.write(self.formatter(list(item.values())))
		self.count += 1
		return item
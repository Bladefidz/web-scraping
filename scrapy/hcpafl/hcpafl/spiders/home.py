# -*- coding: utf-8 -*-
import scrapy
# import pandas as pd
import csv
import re
import json
import os


class HomeSpider(scrapy.Spider):
	'''
		input:
			last_name, first_name
			address
		output:
			First Name, Last Name, Mailing Address, Mail City, Mail State
			Mail Zip Code, Property Address, Property City, Property State,
			Property Zip Code
	'''
	name = 'home'
	# allowed_domains = ['http://gis.hcpafl.org']
	# keywords = []

	custom_settings = {
        'ITEM_PIPELINES': {
            'hcpafl.pipelines.HomeCsvPipeline': 300,
        }
    }

	def start_requests(self):
		# keywords = pd.read_csv('TAMPA_ONLY_TAX_DEFULT_Complete.csv').to_dict(
		# 	orient='records')
		i = 0
		path = os.getcwd()
		with open(path+'/input/TAMPA_ONLY_TAX_DEFULT_Complete.csv') as csvfile:
			csvfile = csv.reader(csvfile)
			for row in csvfile:
				lastName = row[0].strip()
				if lastName == '' or lastName == 'Last name':
					# print(row)
					continue
				# print(row)
				firstName = row[1].strip()
				address = re.sub(r'.\w+\d.$', r'', row[2]);
				address = address.strip()
				yield scrapy.Request(
					url = "http://gis.hcpafl.org/PropertySearch/services/Search/BasicSearch?owner={},+{}&address={}&pagesize=80&page=1".format(lastName, firstName, address),
					callback = self.parse,
					meta = {
						'first_name': firstName,
						'last_name': lastName
					}
				)
				# testing for first 10 requests
				i += 1
				if i == 100:
					break

	def parse(self, response):
		res = json.loads(response.text)
		if len(res) > 0:
			for r in res:
				yield scrapy.Request(
					url = "http://gis.hcpafl.org/PropertySearch/services/Search/ParcelData?pin={}".format(r['pin']),
					callback = self.parseDetail,
					meta = {
						'first_name': response.meta.get("first_name"),
						'last_name': response.meta.get("last_name")
					}
				)

	def parseDetail(self, response):
		res = json.loads(response.text)
		mailingAddress = res["mailingAddress"]
		yield {
			"First Name": response.meta.get("first_name"),
			"Last Name": response.meta.get("last_name"),
			"Mailing Address": mailingAddress['addr1'],
			"Mail City": mailingAddress['city'],
			"Mail State": mailingAddress['state'],
			"Mail Zip Code": mailingAddress['zip'],
			"Property Address": res["siteAddress"],
			"Property City": mailingAddress['city'],
			"Property State": mailingAddress['state'],
			"Property Zip Code": mailingAddress['zip']
		}


def test():
	pass

if __name__ == '__main__':
	test()
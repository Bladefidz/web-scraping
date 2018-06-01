# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.pipelines.images import ImagesPipeline

class ImageminnerPipeline(object):
    def process_item(self, item, spider):
        return item

class ImageDownloadPipeline(ImagesPipeline):
	def get_media_requests(self, item, info):
		folder = item.get("image_dir", "")
		image_urls = item.get('image_urls', False)
		image_names = item.get('image_names', False)
		for i in range(len(image_urls)):
			if image_names:
				yield scrapy.Request(
					image_urls[i],
					meta={'image_dir': folder, 'image_name': image_names[i]})

	def file_path(self, request, response=None, info=None):
		return "{}/{}.jpg".format(
			request.meta.get("image_dir"),
			request.meta.get("image_name"))
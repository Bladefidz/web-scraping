# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from __future__ import print_function
import scrapy
import httplib2
import os
import json
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
from scrapy.exceptions import DropItem
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

class BossPipeline(object):
	def process_item(self, item, spider):
		return item

class ProductImagePipeline(ImagesPipeline):
	"""Upload each downloaded image to Google Drive"""
	SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'
	CLIENT_SECRET_FILE = 'client_secret.json'
	APPLICATION_NAME = 'Image Minning'

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

	def get_credentials():
		"""Gets valid user credentials from storage.

		If nothing has been stored, or if the stored credentials are invalid,
		the OAuth2 flow is completed to obtain the new credentials.

		Returns:
			Credentials, the obtained credential.
		"""
		home_dir = os.path.expanduser('~')
		credential_dir = os.path.join(home_dir, '.credentials')
		if not os.path.exists(credential_dir):
			os.makedirs(credential_dir)
		credential_path = os.path.join(credential_dir,
									   'drive-python-quickstart.json')

		store = Storage(credential_path)
		credentials = store.get()
		if not credentials or credentials.invalid:
			flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
			flow.user_agent = APPLICATION_NAME
			if flags:
				credentials = tools.run_flow(flow, store, flags)
			else: # Needed only for compatibility with Python 2.6
				credentials = tools.run(flow, store)
			print('Storing credentials to ' + credential_path)
		return credentials

	def uploadToGdrive(request):
		folder = request.meta.get("image_dir")
		imageName = "{}.jpg".format(request.meta.get("image_name"))
		localPath = settings['IMAGES_STORE'] + '/' + folder + '/' + imageName;
		file_metadata = {'name': imageName}
		media = MediaFileUpload(path, mimetype='image/jpeg')
		file = drive_service.files().create(body=file_metadata,
											media_body=media,
											fields='id').execute()

	def file_downloaded(self, response, request, info):
		downloaded = self.image_downloaded(response, request, info)
		self.uploadToGdrive(request)
		return downloaded

# class ProductImageJsonPipeline(object):
# 	# def open_spider(self, spider):
# 	# 	pass

# 	# def close_spider(self, spider):
# 	# 	self.file.close()

# 	def process_item(self, item, spider):
# 		line = json.dumps(dict(item)) + "\n"
# 		self.file.write(line)
# 		return item
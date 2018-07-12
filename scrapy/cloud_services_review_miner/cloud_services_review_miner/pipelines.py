# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import re
import json
import datetime
import time
from copy import copy


class CloudServicesReviewMinerPipeline(object):
    def process_item(self, item, spider):
        return item


class ProductSearchResultCleansingPipeline(object):
    """docstring for ProductReviewCleansingPipeline"""
    def process_item(self, item, spider):
        if item['product_names']:
            if item['ratings']:
                for rating, i in zip(list(item['ratings']), range(len(item['ratings']))):
                    ratingStrSpiltted = rating.split(" ")
                    if ratingStrSpiltted[1].lower() == "ratings":
                        item['ratings'][i] = int(ratingStrSpiltted[0])
                    else:
                        item['ratings'][i] = 0
            if item['stars']:
                stars = []
                count = 0
                goNext = True
                star = 0
                for elem, i in zip(item['stars'], range(len(item['stars']))):
                    if goNext:
                        goNext = False
                        continue
                    else:
                        starStr = item['stars'][i]
                        starStrSplitted = starStr.split(" ")
                        if starStrSplitted[1] == "-full":
                            star += 1
                        count += 1
                    if count == 5:
                        stars.append(star)
                        star = 0
                        count = 0
                        goNext = True
                item['stars'] = stars
            if item['reviews']:
                for review, i in zip(list(item['reviews']), range(len(item['reviews']))):
                    reviewStrSplitted = review.split(" ")
                    if reviewStrSplitted[0].lower() == "reviews":
                        item['reviews'][i] = int(reviewStrSplitted[1].replace('(', '').replace(')', ''))
                    else:
                        item['reviews'][i] = 0
            return item
        else:
            raise DropItem("Item product_names is empty")


class ProductSearchResultReviewJsonPipeline(object):
    """docstring for ProductReviewCsvPipeline"""
    def open_spider(self, spider):
        timestamp = time.time()
        timestamp = datetime.datetime.fromtimestamp(timestamp).strftime('%y-%m-%d %H %M %S')
        self.file = open("keyword_search_result_{}.jl".format(timestamp), 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item

class ProductCleansingPipeline(object):
    """docstring for ProductReviewCleansingPipeline"""
    def process_item(self, item, spider):
        if item['product_names']:
            if item['ratings']:
                for rating, i in zip(list(item['ratings']), range(len(item['ratings']))):
                    ratingStrSpiltted = rating.split(" ")
                    if ratingStrSpiltted[1].lower() == "ratings":
                        item['ratings'][i] = int(ratingStrSpiltted[0])
                    else:
                        item['ratings'][i] = 0
            if item['stars']:
                stars = []
                count = 0
                goNext = True
                star = 0
                for elem, i in zip(item['stars'], range(len(item['stars']))):
                    if goNext:
                        goNext = False
                        continue
                    else:
                        starStr = item['stars'][i]
                        starStrSplitted = starStr.split(" ")
                        if starStrSplitted[1] == "-full":
                            star += 1
                        count += 1
                    if count == 5:
                        stars.append(star)
                        star = 0
                        count = 0
                        goNext = True
                item['stars'] = stars
            if item['reviews']:
                for review, i in zip(list(item['reviews']), range(len(item['reviews']))):
                    reviewStrSplitted = review.split(" ")
                    if reviewStrSplitted[0].lower() == "reviews":
                        item['reviews'][i] = int(reviewStrSplitted[1].replace('(', '').replace(')', ''))
                    else:
                        item['reviews'][i] = 0
            return item
        else:
            raise DropItem("Item product_names is empty")


class ProductReviewJsonPipeline(object):
    """docstring for ProductReviewCsvPipeline"""
    def open_spider(self, spider):
        timestamp = time.time()
        timestamp = datetime.datetime.fromtimestamp(timestamp).strftime('%y-%m-%d %H %M %S')
        self.file = open("products_{}.jl".format(timestamp), 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem

class NobelImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        print("item['image_urls']", item['image_urls'])
        for image_url in item['image_urls']:
            print("image_url", image_url)
            yield scrapy.Request(image_url)

    def item_complete(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if image_paths:
            item['bio_image'] = image_paths[0]
        return item

class NobelWinnersPipeline(object):
    def process_item(self, item, spider):
        return item

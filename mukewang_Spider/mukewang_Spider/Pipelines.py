# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json

import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline


class MukewangPipeline(object):
	def __init__(self):
		# 打开文件
		self.file = open('data.json', 'w', encoding='utf-8')

	'''该方法用于处理数据'''

	def process_item(self, item, spider):
		# 读取item中的数据
		line = json.dumps(dict(item), ensure_ascii=False) + '\n'
		# 写入文件
		self.file.write(line)
		return item

	'''该方法在spider被开启时调用'''

	def open_spider(self, spider):
		pass

	'''该方法在spider被关闭时调用'''

	def close_spider(self, spider):
		pass


class ImgPipeline(ImagesPipeline):
	# 通过抓取的图片url获取一个Request用于下载
	def get_media_requests(self, item, info):
		# 返回Request根据图片的url下载
		yield scrapy.Request('https:' + item['image_url'])

	# 当下载请求完成后执行该方法
	def item_completed(self, results, item, info):
		# 获取下载地址
		image_path = [x['path'] for ok, x in results if ok]
		# 判断是否成功
		if not image_path:
			raise DropItem('Item contains no images')
		# 将地址存入item
		item['image_path'] = image_path
		return item

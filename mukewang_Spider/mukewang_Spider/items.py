# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MukewangSpiderItem(scrapy.Item):
	# define the fields for your item here like:
	# name = scrapy.Field()
	title = scrapy.Field()  # 课程标题
	url = scrapy.Field()  # 课程url
	image_url = scrapy.Field()  # 课程标题图片
	introduction = scrapy.Field()  # 课程描述
	student = scrapy.Field()  # 学习人数
	image_path = scrapy.Field() #图片地址

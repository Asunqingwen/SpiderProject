# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from openpyxl import Workbook

class CNKISpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    title_url = scrapy.Field()
    author = scrapy.Field()
    source = scrapy.Field()
    issue_time = scrapy.Field()
    database = scrapy.Field()
    is_cited = scrapy.Field()
    is_downloaded = scrapy.Field()
    abstract = scrapy.Field()
    pass

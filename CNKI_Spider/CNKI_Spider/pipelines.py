# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from openpyxl.reader.excel import load_workbook


class CNKISpiderPipeline(object):
    def __init__(self):
        pass

    '''该方法用于处理数据'''

    def process_item(self, item, spider):
        # 读取item中的数据
        # 写入文件
        row = [item['title'], item['author'], item['source'], item['issue_time'], item['database'],
               item['is_cited'], item['is_downloaded'], item['title_url'], item['abstract']]
        self.ws.append(row)
        return item

    '''该方法在spider被开启时调用'''

    def open_spider(self, spider):
        self.wb = load_workbook("D:/Desktop/组织行为学.xlsx")
        self.ws = self.wb.active
        pass

    '''该方法在spider被关闭时调用'''

    def close_spider(self, spider):
        self.wb.save("D:/Desktop/组织行为学.xlsx")
        pass

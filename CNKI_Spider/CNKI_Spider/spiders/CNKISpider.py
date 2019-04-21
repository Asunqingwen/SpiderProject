import copy

import scrapy
from pyquery import PyQuery as pq

from CNKI_Spider.items import CNKISpiderItem

p = 15


class CNKISpider(scrapy.Spider):
    name = 'CNKISpider'  # 用于区别Spider

    def __init__(self):
        super(CNKISpider, self).__init__()
        # self.key = '职场排斥'
        # self.key = '情绪智力'
        # self.key = '情绪耗竭'
        self.key = '组织公民行为'
        self.type_list = ['qw', 'theme', 'title', 'abstract']
        # self.allowed_domains = ['search.cnki.com.cn']  # 允许访问的域
        self.start_urls = ['http://search.cnki.com.cn/Search.aspx?q={}:{}'.format(self.type_list[1], self.key)]  # 爬取的地址

    # print(self.start_urls)

    '''爬取方法'''

    # 主页
    def parse(self, response):
        # 实例一个容器保存爬取的信息
        item = CNKISpiderItem()
        doc = pq(response.text)
        for wz_content in doc(".wz_content").items():
            item['title'] = wz_content("a").text()
            item['title_url'] = wz_content("a").attr('href')
            title_list = wz_content(".year-count").children().eq(0).text().strip().split('\xa0\xa0')
            if len(title_list) == 3:
                item['source'] = title_list[0]
                item['database'] = title_list[1]
                item['issue_time'] = title_list[2]
            elif len(title_list) == 2:
                item['source'] = title_list[0]
                item['database'] = '非学术论文'
                item['issue_time'] = title_list[1]
            count_list = wz_content(".year-count").children().eq(1).text().strip().split('|')
            item['is_downloaded'] = count_list[0]
            item['is_cited'] = count_list[1]
            # yield scrapy.Request(item['title_url'], meta={'item': item}, callback=self.GetAbstractAndAuthor,dont_filter=True)
            yield scrapy.Request(item['title_url'], meta={'item': copy.deepcopy(item)},
                                 callback=self.GetAbstractAndAuthor,
                                 dont_filter=True)  # 深度复制，不然会出现数据错乱

        # url跟进开始
        # 获取下一页的url信息
        # current_page = int(doc("strong .pc").text())
        # if current_page < 100:
        # url = doc(".n").attr('href')
        # if url:
        #     # 将信息组合成下一页的url
        #     page = 'http://search.cnki.com.cn/' + url
        #     # 返回url
        global p
        if (p <= 1005):
            page = 'http://search.cnki.com.cn/Search.aspx?q=qw%3a%E7%BB%84%E7%BB%87%E8%A1%8C%E4%B8%BA%E5%AD%A6&rank=relevant&cluster=all&val=&p={}'.format(
                p)
            p += 15
            yield scrapy.Request(page, callback=self.parse)

    def GetAbstractAndAuthor(self, response):
        item = response.meta['item']
        doc = pq(response.text)
        item['abstract'] = doc(".xx_font").text().strip('')[5:].split('【')[0].strip()
        item['author'] = ' '.join(doc(".xx_title").parent().siblings().eq(1).text().split())
        yield item

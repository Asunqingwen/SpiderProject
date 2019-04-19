import scrapy
from pyquery import PyQuery as pq

from CNKI_Spider.items import CNKISpiderItem


class CNKISpider(scrapy.Spider):
	name = 'CNKISpider'  # 用于区别Spider

	def __init__(self):
		super(CNKISpider, self).__init__()
		self.key = '组织行为学'
		self.type_list = ['qw', 'theme', 'title', 'abstract']
		# self.allowed_domains = ['search.cnki.com.cn']  # 允许访问的域
		self.start_urls = ['http://search.cnki.com.cn/Search.aspx?q={}:{}'.format(self.type_list[0], self.key)]  # 爬取的地址

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
			yield scrapy.Request(item['title_url'], meta={'item': item}, callback=self.GetAbstractAndAuthor)

	# url跟进开始
	# 获取下一页的url信息
	# url = response.xpath("//a[contains(text(),'下一页')]/@href").extract()
	# if url:
	# 	# 将信息组合成下一页的url
	# 	page = domain_url + url[0]
	# 	# 返回url
	# 	yield scrapy.Request(page, callback=self.parse)

	def GetAbstractAndAuthor(self, response):
		item = response.meta['item']
		doc = pq(response.text)
		item['abstract'] = doc(".xx_font").text().strip('')[5:].split('【')[0].strip()
		item['author'] = ' '.join(doc(".xx_title").parent().siblings().eq(1).text().split())
		return item

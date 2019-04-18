import scrapy
from mukewang_Spider.items import MukewangSpiderItem

domain_url = 'http://www.imooc.com'

class MukewangSpider(scrapy.Spider):
	name = 'MukewangSpider'  # 用于区别Spider
	allowed_domains = ['imooc.com']  # 允许访问的域
	start_urls = ["http://www.imooc.com/course/list"]  # 爬取的地址

	'''爬取方法'''

	def parse(self, response):
		# 实例一个容器保存爬取的信息
		item = MukewangSpiderItem()
		for box in response.xpath('//div[@class="course-card-container"]/a[@target="_blank"]'):
			item['url'] = domain_url + box.xpath('.//@href').extract()[0]
			item['title'] = box.xpath('.//h3/text()').extract()[0].strip()
			item['image_url'] = box.xpath('.//@src').extract()[0]
			item['student'] = box.xpath('.//span/text()').extract()[1]
			item['introduction'] = box.xpath('.//p/text()').extract()[0].strip()
			yield item
		# url跟进开始
		# 获取下一页的url信息
		url = response.xpath("//a[contains(text(),'下一页')]/@href").extract()
		if url:
			# 将信息组合成下一页的url
			page = domain_url + url[0]
			# 返回url
			yield scrapy.Request(page, callback=self.parse)

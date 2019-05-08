from datetime import datetime

from spider_job import get_csv, logger
from zhishu_temperature_job import zhishu_temperature

if __name__ == '__main__':
	start = datetime.now()
	get_csv()
	logger.info("完成数据收集总耗时 {}".format(datetime.now() - start))

	start = datetime.now()
	zhishu_temperature()
	logger.info("完成所有指数的温度计算总耗时 {}".format(datetime.now() - start))

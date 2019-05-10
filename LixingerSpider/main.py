from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler

from sendmail_job import sendCsv
from spider_job import get_csv, logger
from zhishu_temperature_job import zhishu_temperature

scheduler = BlockingScheduler()


@scheduler.scheduled_job("cron",day_of_week=2,hour=15)
def main_job():
	start = datetime.now()
	get_csv()
	logger.info("完成数据收集总耗时 {}".format(datetime.now() - start))

	start = datetime.now()
	zhishu_temperature()
	logger.info("完成所有指数的温度计算总耗时 {}".format(datetime.now() - start))

	sendCsv("./latest_temperature.csv", "./zhishu.jpg")


if __name__ == '__main__':
	try:
		scheduler.start()
	except(KeyboardInterrupt, SystemExit):
		scheduler.shutdown()

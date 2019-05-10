from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from sendmail_job import sendCsv
from spider_job import get_csv, logger
from zhishu_temperature_job import zhishu_temperature


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
		scheduler = BlockingScheduler()
		trigger = CronTrigger(minute=1)
		scheduler.add_job(main_job, trigger)
		scheduler.start()
	except(KeyboardInterrupt, SystemExit):
		scheduler.shutdown()

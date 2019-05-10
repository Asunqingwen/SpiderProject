import logging
from logging import handlers

LOG_LEVEL = logging.INFO  # 日志等级


def get_logger():
	"""
	创建日志实例
	"""
	formatter = logging.Formatter("%(asctime)s - %(message)s")
	logger = logging.getLogger("monitor")
	logger.setLevel(LOG_LEVEL)

	cmd = logging.StreamHandler()
	cmd.setFormatter(formatter)

	file = handlers.TimedRotatingFileHandler(filename="./log", when='D', backupCount=30, encoding='utf-8')
	file.setFormatter(formatter)

	# logger.addHandler(cmd)  #输出到console
	logger.addHandler(file)  # 输出到log文件
	return logger


logger = get_logger()

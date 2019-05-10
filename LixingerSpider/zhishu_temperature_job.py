import csv
import os

import numpy as np
from scipy.stats import norm
from tqdm import tqdm

from logging_job import logger

ROOT_PATH = "CsvFiles"
lastest_temperature = "./latest_temperature.csv"


def normdist(data):
	_temperature = list()
	for idx, val in enumerate(data[1:]):
		use_data = data[:idx + 2]
		mean = np.mean(use_data)
		stdDev = np.std(use_data, ddof=1)
		norm_dist = norm(mean, stdDev).cdf(val) * 100
		_temperature.append(norm_dist)
	return _temperature


def zhishu_temperature():
	logger.info("开始计算所以指数的指数温度........")
	files = os.listdir(ROOT_PATH)
	logger.info("开始计算所以指数的指数温度........")
	latest_temperature = list()
	latest_headers = ["date", "指数", "PE温度", "PB温度", "平均温度"]
	try:
		with tqdm(files) as files:
			for file in files:
				if file.endswith(".csv"):
					zhishu_name = file.split('.')[0]
					files.set_description("%s指数的指数温度正在计算........" % zhishu_name)
					logger.info("{}的指数温度正在计算........".format(zhishu_name))
					headers = list()
					date = list()
					pe_ttm = list()
					pb = list()

					csv_path = os.path.join(ROOT_PATH, file)
					with open(csv_path, "r") as f:
						f_csv = csv.reader(f)
						headers.extend(next(f_csv))
						for row in f_csv:
							date.append(row[0])
							pe_ttm.append(float(row[1]))
							pb.append(float(row[2]))
					pe_ttm_temperature = normdist(pe_ttm)
					pb_temperature = normdist(pb)
					headers.insert(2, "PE温度")
					headers.insert(4, "PB温度")
					headers.insert(5, "平均温度")
				avg_temperature = [(pe + pb) / 2 for pe, pb in zip(pe_ttm_temperature, pb_temperature)]
				latest_temperature.append(dict(zip(latest_headers,
				                                   [date[-1], zhishu_name, pe_ttm_temperature[-1], pb_temperature[-1],
				                                    avg_temperature[-1]])))

			with open(csv_path, "w", encoding="gbk", newline="") as f:
				f_csv = csv.DictWriter(f, headers)
				f_csv.writeheader()
				for d, pe_ttm_d, pe_ttm_t, pb_d, pb_t, avg_t in zip(date[1:], pe_ttm[1:], pe_ttm_temperature,
				                                                    pb[1:],
				                                                    pb_temperature, avg_temperature):
					row = dict(zip(headers, [d, pe_ttm_d, pe_ttm_t, pb_d, pb_t, avg_t]))
					f_csv.writerow(row)
		logger.info("{}的指数温度已完成计算........".format(zhishu_name))
		latest_temperature.sort(key=lambda v: float(v['平均温度']))
		with open("./latest_temperature.csv", "w", encoding="gbk", newline="") as f:
			f_csv = csv.DictWriter(f, latest_headers)
			f_csv.writeheader()
			f_csv.writerows(latest_temperature)

	except Exception as e:
		logger.error(e)
		logger.info("所有指数的指数温度已完成计算........")

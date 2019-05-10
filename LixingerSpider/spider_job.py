import csv
import json

import requests
from tqdm import tqdm

from logging_job import logger

data_list_url = "https://www.lixinger.com/api/analyt/stock-collection/price-metrics/indices/latest"
detail_csv_url = "https://www.lixinger.com/api/analyt/stock-collection/price-metrics/load"
payloadHeader = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
	"Content-Type": "application/json;charset=UTF-8",
	'Cookie': 'jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI1Y2QxMzVhZGMxOTZkYTUyOTAwZTlkYTAiLCJpYXQiOjE1NTcyMTQ2MzcsImV4cCI6MTU1NzgxOTQzN30.4cOWbqtL1nCPZ_TxOBC3bSO8h8LJH3M2MyygucOssxE; Hm_lvt_ec0ee7e5c8bed46d4fdf3f338afc08f5=1557214618,1557214637,1557280317; Hm_lpvt_ec0ee7e5c8bed46d4fdf3f338afc08f5=1557281309',
}
data_list_payloadData = {"metricNames": ["pe_ttm", "pb", "ps_ttm", "dyr"], "granularities": ["y_10"],
                         "metricTypes": ["weightedAvg"]}

pe_ttm_csv_payloadData = {"stockIds": "", "dateFlag": "week", "granularity": "f_s",
                          "metricNames": ["pe_ttm", "cp", "mc", "cmc"], "metricTypes": ["weightedAvg"]}
pb_csv_payloadData = {"stockIds": "", "dateFlag": "week", "granularity": "f_s",
                      "metricNames": ["pb", "cp", "mc", "cmc"], "metricTypes": ["weightedAvg"]}


def get_csv():
	r = requests.post(data_list_url, data=json.dumps(data_list_payloadData), headers=payloadHeader)
	data_list = json.loads(r.text)
	with tqdm(data_list) as data_list:
		for data in data_list:
			zhishu_name = data["cnName"]
			data_list.set_description("%s指数的PE和PB数据正在收集........" % zhishu_name)
			logger.info("{}的PE和PB数据正在收集........".format(zhishu_name))
			pe_ttm_csv_payloadData["stockIds"] = [data["stockId"]]
			pb_csv_payloadData["stockIds"] = [data["stockId"]]
			try:
				pe_ttm_csv = requests.post(detail_csv_url, data=json.dumps(pe_ttm_csv_payloadData),
				                           headers=payloadHeader)
				pb_csv = requests.post(detail_csv_url, data=json.dumps(pb_csv_payloadData), headers=payloadHeader)
				pe_ttm_csv_data = json.loads(pe_ttm_csv.text)
				pb_csv_data = json.loads(pb_csv.text)

				pe_ttm_csv_data = reversed(pe_ttm_csv_data)
				pb_csv_data = reversed(pb_csv_data)

				headers = ['date', 'pe_ttm', "pb"]
				with open("./CsvFiles/{}.csv".format(zhishu_name), "w", newline="") as f:
					f_csv = csv.DictWriter(f, headers)
					f_csv.writeheader()
					if zhishu_name != "恒生指数":
						for pe_ttm_data, pb_data in zip(pe_ttm_csv_data, pb_csv_data):
							row = dict(
								zip(headers, [pe_ttm_data['date'].split("T")[0], pe_ttm_data["pe_ttm"]["weightedAvg"],
								              pb_data["pb"]["weightedAvg"]]))
							f_csv.writerow(row)
					else:
						for pe_ttm_data, pb_data in zip(pe_ttm_csv_data, pb_csv_data):
							if pe_ttm_data["pe_ttm"]:
								row = dict(
									zip(headers,
									    [pe_ttm_data['date'].split("T")[0], pe_ttm_data["pe_ttm"]["weightedAvg"],
									     pb_data["pb"]["weightedAvg"]]))
								f_csv.writerow(row)
			except Exception as e:
				logger.error(e)
			logger.info("{}的PE和PB数据已完成收集........".format(zhishu_name))

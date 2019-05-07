import json

import requests

url = "https://www.lixinger.com/api/analyt/stock-collection/price-metrics/indices/latest"
payloadHeader = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
	'Cookie': 'jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI1Y2QxMzVhZGMxOTZkYTUyOTAwZTlkYTAiLCJpYXQiOjE1NTcyMTQ2MzcsImV4cCI6MTU1NzgxOTQzN30.4cOWbqtL1nCPZ_TxOBC3bSO8h8LJH3M2MyygucOssxE; Hm_lvt_ec0ee7e5c8bed46d4fdf3f338afc08f5=1557214618,1557214637; Hm_lpvt_ec0ee7e5c8bed46d4fdf3f338afc08f5=1557219702',
}
payloadData = {"metricNames": ["pe_ttm", "pb", "ps_ttm", "dyr"], "granularities": ["y_10"],
               "metricTypes": ["weightedAvg"]}
r = requests.post(url, data=json.dumps(payloadData), headers=payloadHeader)
data_list = json.loads(r.text)
getHeader = {
	"Cookie": "jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI1Y2QxMzVhZGMxOTZkYTUyOTAwZTlkYTAiLCJpYXQiOjE1NTcyMTQ2MzcsImV4cCI6MTU1NzgxOTQzN30.4cOWbqtL1nCPZ_TxOBC3bSO8h8LJH3M2MyygucOssxE; Hm_lvt_ec0ee7e5c8bed46d4fdf3f338afc08f5=1557214618,1557214637; Hm_lpvt_ec0ee7e5c8bed46d4fdf3f338afc08f5=1557221422",
	"User-Agent": " Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
}
base_url = "https://www.lixinger.com/analytics/indice/sh/{}/detail/value?metric-name={}&metric-type=weightedAvg&granularity=f_s"
csv_url = "https://www.lixinger.com/api/analyt/stock-collection/price-metrics/load"
csv_payloadHeader = {
"Cookie": "jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI1Y2QxMzVhZGMxOTZkYTUyOTAwZTlkYTAiLCJpYXQiOjE1NTcyMTQ2MzcsImV4cCI6MTU1NzgxOTQzN30.4cOWbqtL1nCPZ_TxOBC3bSO8h8LJH3M2MyygucOssxE; Hm_lvt_ec0ee7e5c8bed46d4fdf3f338afc08f5=1557214618,1557214637; Hm_lpvt_ec0ee7e5c8bed46d4fdf3f338afc08f5={}",
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
}
pe_ttm_csv_payloadData = {"stockIds": [10000000009], "dateFlag": "week", "granularity": "f_s",
                          "metricNames": ["pe_ttm", "cp", "mc", "cmc"], "metricTypes": ["weightedAvg"]}
pb_csv_payloadData = {"stockIds": [10000000009], "dateFlag": "week", "granularity": "f_s",
                      "metricNames": ["pb", "cp", "mc", "cmc"], "metricTypes": ["weightedAvg"]}

r_csv = requests.post(csv_url, data=json.dumps(pe_ttm_csv_payloadData), headers=csv_payloadHeader)
# data_list = json.loads(r_csv.text)
pe_ttm_url = base_url.format(data_list[0]["stockCode"],'pe_ttm')
cookies_url = "https://www.lixinger.com/api/analyt/stock-collection/price-metrics/get-price-metrics-chart-info"
r = requests.get(cookies_url)
print(r.cookies.get_dict())
# for data in data_list:
# 	get_url = base_url.format(data["stockCode"])
# 	pe_ttm_url = base_url.format(data["stockCode"], 'pe_ttm')
# 	pb_url = base_url.format(data["stockCode"], 'pb')
# 	print(get_url)

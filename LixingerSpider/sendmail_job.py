from datetime import datetime

import zmail

emailName = '*****@sina.com'
password = '*********'

send_mail = ['*****@sina.com']


def sendCsv(csv_path):
	mail_content = {
		'subject': "{0:%Y-%m-%d %H:%M:%S} 指数温度的csv文件".format(datetime.now()),
		'content_text': "Allen，下午好！\n\t这是最新的指数温度csv文件，请查收！",
		'attachments': csv_path
	}

	server = zmail.server(emailName, password)
	server.send_mail(send_mail, mail_content)

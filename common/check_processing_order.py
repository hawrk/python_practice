__author__ = 'hawrk'
__date__ = '2016.12.06'

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.header import Header
from email.utils import parseaddr,formataddr

#from __future__ import with_statement

import pymysql
import time
import smtplib
import logging


def _format_addr_(s):
    name,addr = parseaddr(s)
    return formataddr((Header(name,'utf-8').encode(),addr))

from_addr = 'hawrk2012@163.com'
to_addr = ['hawrk@tfb8.com','longgz@tfb8.com','lidb@tfb8.com']
passwd = 'sk193752szu'     #w个人邮箱没什么好看的哈～
smtp_server = 'smtp.163.com'

def send_mail(order_list =[]):
    #print ("send mail:")
    logging.info("sending mail......")
    #msg = MIMEMultipart()
    msg = ""
    for list in order_lsit:
        msg += list + ","
    notice  ='''
        警告:
            昨日还有银行处理中的单号未处理，请尽快处理！
            订单列表如下：
    '''
    send_msg = notice + msg
    msg = MIMEText(send_msg,'plain','utf-8')
    msg['From'] = _format_addr_('hawrk<%s>' % from_addr)
    msg['To'] = _format_addr_('stupid_boy<%s>' % to_addr)       #收件人
    msg['Subject'] = Header('[Warning]昨日还有未终态的代付单号!!','utf-8').encode()    #消息的标题

    try:
        server = smtplib.SMTP(smtp_server,25)
        #server.set_debuglevel(1)
        server.login(from_addr,passwd)
        server.sendmail(from_addr,to_addr,msg.as_string())
        print ('send mail success')
        server.quit()

    except smtplib.SMTPException:
        print("error:send fail")

def check_process_order():
    try:
        conn = pymysql.connect(host='192.168.1.63', port=3306, user='readuser', passwd='readuser', db='order_db',
                               charset='utf8mb4')
        cur = conn.cursor()
        start_time = time.strftime('%Y-%m-%d', time.localtime(time.time()- 24*60*60)) + ' 00:00:00'
        end_time = time.strftime('%Y-%m-%d', time.localtime(time.time()- 24*60*60)) + ' 23:59:59'
        sql = "select Flistid from t_agent_pay_detail where " \
              " Fcreate_time BETWEEN '" + start_time + "' AND '" + end_time + "' and Fstate=6"    #处理中
        logging.info('execute sql:[%s]', sql)
        cur.execute(sql)

        result = cur.fetchall()
        file_row = []
        for row in result:
            file_row.append(row[0])
        conn.commit()
        return file_row
    finally:
        conn.close()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s [line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%d %b %Y %H:%M:%S',
                        filename='/home/gctest/hawrk/check_order.log',
                        filemode='a')
    logging.info('*************begin*******************')
    curdate = time.strftime('%Y%m%d', time.localtime(time.time()))
    logging.info("curdate=%s",curdate)
    order_lsit = check_process_order()
    if len(order_lsit) != 0:
        send_mail(order_lsit)
    else:
        logging.info("no data")
    logging.info("############## process end#######################")
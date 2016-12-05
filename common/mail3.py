from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.header import Header
from email.utils import parseaddr,formataddr

import pymysql
import time
import smtplib

def _format_addr_(s):
    name,addr = parseaddr(s)
    return formataddr((Header(name,'utf-8').encode(),addr))

from_addr = 'hawrk2012@163.com'
to_addr = ['hawrk@tfb8.com']
passwd = 'sk193752szu'     #w个人邮箱没什么好看的哈～
smtp_server = 'smtp.163.com'

def send_mail():
    msg = MIMEMultipart()
    msg = MIMEText('''
        地球人你好:
            这是一封来自星际空间站的系统检测报告:
            目前代付系统垫资额度已经超过了 95%，请及时发出公告通知各代付商户，
            敬请配合！
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

            ''','plain','utf-8')
    msg['From'] = _format_addr_('来自星际的穿越者<%s>' % from_addr)
    msg['To'] = _format_addr_('愚蠢的地球人<%s>' % to_addr)       #收件人
    msg['Subject'] = Header('[Warning]来自火星的系统警报','utf-8').encode()    #消息的标题

    try:

        server = smtplib.SMTP(smtp_server,25)
        server.set_debuglevel(1)
        server.login(from_addr,passwd)
        server.sendmail(from_addr,to_addr,msg.as_string())
        print ('send mail success')
        server.quit()

    except smtplib.SMTPException:
        print("error:send fail")

def get_used_amount():
    try:
        conn = pymysql.connect(host='192.168.1.63', port=3306, user='readuser', passwd='readuser', db='order_db', \
                               charset='utf8mb4')
        cur = conn.cursor()
        curtime = time.strftime('%Y%m%d',time.localtime(time.time()))
        sql = "select Famount from t_advance_payment_sum where Frecord_date ='" + curtime +"'"
        cur.execute(sql)
        result = cur.fetchall()
        used = 0
        for row in result:
            used += int(row[0])
        return used

    finally:
        conn.close()

def get_total_amount():
    try:
        conn = pymysql.connect(host='192.168.1.63', port=3306, user='readuser', passwd='readuser', db='config_db', \
                               charset='utf8mb4')
        cur = conn.cursor()
        sql = "select Fday_amount_ceiling from t_channel_withdraw_account where Fstate=1 and Fpay_type=3"
        cur.execute(sql)
        result = cur.fetchall()
        total = 0
        for row in result:
            total += int(row[0])
        return total

    finally:
        conn.close()

if __name__ == '__main__':
    channel_used = get_used_amount()
    channel_total = get_total_amount()
    if(channel_used/channel_total > 0.95):
        send_mail()
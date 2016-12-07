from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.header import Header
from email.utils import parseaddr,formataddr

import pymysql
import time
import smtplib
import logging
import configparser

def _format_addr_(s):
    name,addr = parseaddr(s)
    return formataddr((Header(name,'utf-8').encode(),addr))

from_addr = 'hawrk2012@163.com'
to_addr = ['hawrk@tfb8.com','kefu@tfb8.com','zhangrj@cpp-pay.com','lisq@cpp-pay.com']
passwd = 'sk193752szu'     #w个人邮箱没什么好看的哈～
smtp_server = 'smtp.163.com'

def send_mail(used,total):
    #print ("send mail:")
    logging.info("sending mail......")
    cal_msg = "当前已用：" + str(used) + ",渠道额度:"+ str(total)
    notice_1 = '''
        通知:

            国采支付垫资代付当天的渠道额度即将用尽，请尽快通知各垫资代付商户做好渠道切换工作！

            '''
    notice_2 = '''

            敬请配合，谢谢！

            (该邮件为系统自动发出，请勿回复！）

        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            我是最萌的拖尾君~-~
            '''
    send_msg = notice_1 + cal_msg + notice_2
    msg = MIMEText(send_msg,'plain','utf-8')
    msg['From'] = _format_addr_('国采技术<%s>' % from_addr)
    msg['To'] = _format_addr_('愚蠢的地球人<%s>' % to_addr)  # 收件人
    msg['Subject'] = Header('[Warning]国采支付垫资代付渠道额度即将用尽!!', 'utf-8').encode()  # 消息的标题

    try:

        server = smtplib.SMTP(smtp_server,25)
        #server.set_debuglevel(1)
        server.login(from_addr,passwd)
        server.sendmail(from_addr,to_addr,msg.as_string())
        print ('send mail success')
        server.quit()

    except smtplib.SMTPException:
        print("error:send fail")

def get_used_amount(curdate):
    try:
        conn = pymysql.connect(host='192.168.1.63', port=3306, user='readuser', passwd='readuser', db='order_db', \
                               charset='utf8mb4')
        cur = conn.cursor()
        sql = "select Famount from t_advance_payment_sum where Frecord_date ='" + curdate +"'"
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


def read_conf():
    cf = configparser.ConfigParser()
    cf.read('/home/gctest/hawrk/mail.conf')

    cf.sections()
    #option = cf.options("mail")
    date = cf.get("mail","date")
    send_flag = cf.getint("mail","send_flag")

    #print ('date =%s' %date)
    #print ('send_flag = %d' %send_flag)
    return date,send_flag

#初始化当天的配置信息
def set_conf(curdate):
    cf = configparser.ConfigParser()
    cf.read('/home/gctest/hawrk/mail.conf')

    cf.set("mail","date",curdate)
    cf.set("mail","send_flag","0")
    cf.write(open("/home/gctest/hawrk/mail.conf","w"))

#设置发送标志为已读
def set_send_flag():
    cf = configparser.ConfigParser()
    cf.read('/home/gctest/hawrk/mail.conf')

    cf.set("mail", "send_flag", "1")
    cf.write(open("/home/gctest/hawrk/mail.conf", "w"))

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s [line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%d %b %Y %H:%M:%S',
                        filename='/home/gctest/hawrk/sendmail.log',
                        filemode='a')
    logging.info('*************begin*******************')
    curdate = time.strftime('%Y%m%d', time.localtime(time.time()))
    logging.info("curdate=%s",curdate)
    #先读取配置文件，如日期不是当天，则初始化当前日期
    confdate, send_flag = read_conf()
    if curdate != confdate:
        set_conf(curdate)
    channel_used = get_used_amount(curdate)
    channel_total = get_total_amount()
    logging.info("used = %d,total=%d",channel_used,channel_total)
    #print ('used = %d,total=%d' %(channel_used,channel_total))
    if(channel_used/channel_total > 0.95 and send_flag == 0):
        send_mail(channel_used,channel_total)
        set_send_flag()
    #logging.info("############## process end#######################")
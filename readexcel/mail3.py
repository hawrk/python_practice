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
to_addr = ['hawrk@tfb8.com','kefu@tfb8.com','zhangrj@cpp-pay.com','lisq@cpp-pay.com','pangye@tfb8.com','taotao@cpp-pay.com','lidb@tfb8.com']
#to_addr = ['hawrk@tfb8.com']
passwd = 'sk193752szu'     #w个人邮箱没什么好看的哈～
smtp_server = 'smtp.163.com'

def send_mail(used,total,book_usd,book_total):
    #print ("send mail:")
    logging.info("sending mail......")
    no_book_used = used - book_usd

    no_book_avail = total - book_total - no_book_used
    cal_msg = "当前渠道已用：" + str(used) + ",   渠道总额度:"+ str(total) + '\n'
    book_msg = "            当前预约已用：" + str(book_usd) + ",   预约总额度：" +str(book_total) + '\n'
    no_book_msg = "            非预约已用：" + str(no_book_used) + ",   非预约可用："  + str(no_book_avail)
    notice_1 = '''
        通知:
            国采支付垫资代付当天的渠道额度即将用尽，请尽快通知各垫资代付商户做好渠道切换工作！

            '''
    notice_2 = '''

            敬请配合，谢谢！

            (该邮件为系统自动发出，请勿回复！）

        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            我是最萌的拖尾君╮(~▽~)╭
            '''
    send_msg = notice_1 + cal_msg + book_msg + no_book_msg +  notice_2
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

#渠道总额度
def get_total_amount():
    try:
        conn = pymysql.connect(host='192.168.1.63', port=3306, user='readuser', passwd='readuser', db='', \
                               charset='utf8mb4')
        cur = conn.cursor()
        #渠道总额度
        sql = "select Fday_amount_ceiling from config_db.t_channel_withdraw_account where Fstate=1 and Fpay_type=3"
        cur.execute(sql)
        result = cur.fetchall()
        chanl_total = 0
        for row in result:
            chanl_total += int(row[0])
        logging.info("channel_total_amount:[%d]",chanl_total)

        #渠道已用额度
        sql = "select Famount from order_db.t_advance_payment_sum where Frecord_date ='" + curdate +"'"
        cur.execute(sql)
        result = cur.fetchall()
        chanl_used = 0
        for row in result:
            chanl_used += int(row[0])

        logging.info("channel_used_amount:[%d]", chanl_used)

        # 预约总额度和预约已用额度
        sql = "select Fused_amount, Fbook_amount from order_db.t_advance_payment where Frecord_date = '" + curdate +"' and Fbook_flag = 1"

        cur.execute(sql)
        result = cur.fetchall()
        book_total = 0
        book_used = 0
        for row in result:
            book_used += int(row[0])
            book_total += int(row[1])

        logging.info("book total:[%d],book used =%d", book_total,book_used)
        return chanl_used,chanl_total,book_used,book_total
        #return chanl_total

    finally:
        logging.info("close connection")
        cur.close()
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
                        filename='/home/gctest/hawrk/log/sendmail.log',
                        filemode='a')
    #logging.info('*************begin*******************')
    curdate = time.strftime('%Y%m%d', time.localtime(time.time()))
    logging.info("curdate=%s",curdate)
    #先读取配置文件，如日期不是当天，则初始化当前日期
    confdate, send_flag = read_conf()
    if curdate != confdate:
        set_conf(curdate)

    channel_used,channel_total,booked_used,booked_total = get_total_amount()
    logging.info("channel_used = %d,channel_total=%d,book_used=%d,book_total=%d",channel_used,channel_total,booked_used,booked_total)
    #print ('used = %d,total=%d' %(channel_used,channel_total))
    if((channel_used-booked_used)/(channel_total-booked_total) > 0.90 and send_flag == 0):
    #if(channel_used/channel_total > 0.96 and send_flag == 0):
        send_mail(channel_used,channel_total,booked_used,booked_total)
        set_send_flag()
    logging.info("############## process end#######################")
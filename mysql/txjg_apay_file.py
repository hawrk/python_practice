__author__ = 'hawrk'
__date__ = '2016.09.19'

import os
import pymysql
import logging
import time
from ftplib import FTP

SPID = "1800594826"
#SPID = "1000000068"

def save_to_file(filename):
        try:
                conn = pymysql.connect(host ='192.168.0.115',port = 3306,user = 'depuser',passwd = 'depuser',db = 'order_db',charset='utf8mb4')
                logging.info("save to :[%s] begin...",filename)
                f = open(filename,'w+')

                cur = conn.cursor()
                start_time = time.strftime('%Y-%m-%d', time.localtime(time.time())) + ' 00:00:00'
                end_time = time.strftime('%Y-%m-%d', time.localtime(time.time())) + ' 23:59:59'
                sql = "select Flistid,Fspid,Fsp_listid,Fpay_type,Fpay_money,Fpayee_name,Fpayee_cardno,Fstate,Fprocode,Fproinfo,Fmemo,Fcreate_time from t_agent_pay_detail where Fspid ='" + SPID \
                      +"' and Fcreate_time BETWEEN '" + start_time + "' AND '" + end_time + "'"
                logging.info('execute sql:[%s]',sql)
                cur.execute(sql)

                result = cur.fetchall()

                for row in result:
                    file_row = str(row[0]) + "|" + str(row[1]) + "|" + str(row[2]) + "|" + str(row[3]) + "|" + str(row[4]) + "|" + str(row[5]) + "|" + \
                               str(row[6]) + "|" + str(row[7]) + "|" + str(row[8]) + "|" + str(row[9]) + "|" + str(row[10]) + "|" + str(row[11]) + "\n"
                    print ("file_row = [%s]" %(file_row))
                    f.write(file_row)
                conn.commit()
                logging.info("save file:[%s] OK!",filename)
        finally:
            f.close()
            conn.close()

def send_to_ftp(file_name):
    logging.info("send to ftp server begin")
    ftp = FTP()
    ftp.set_debuglevel(2)
    ftp.connect('192.168.0.40')
    ftp.login('qrpos_df','qrpos_df123')
    print (ftp.getwelcome())

    buf_size = 4096
    file_handler = open(file_name,'rb')
    ftp.storbinary('STOR %s' %os.path.basename(file_name),file_handler,buf_size)
    ftp.set_debuglevel(0)
    file_handler.close()
    ftp.quit()
    logging.info("save to ftp server end")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s [line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%d %b %Y %H:%M:%S',
                        filename='reconciliation_file.log',
                        filemode='a')
    logging.info('*************begin*******************')
    interval = 1
    curtime = time.strftime('%Y%m%d', time.localtime(time.time()))
    filename = SPID + "_" + curtime + ".txt"
    save_to_file(filename)
    send_to_ftp(filename)
    logging.info("############## process end#######################")
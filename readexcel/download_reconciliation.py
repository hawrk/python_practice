# -*- coding: utf-8 -*-

__author__ = 'hawrk'
__date__  = '2016.12.20'

'''
从ftp 服务器上下载昨天的垫资代付和普通代付的对账单，
保存到/home/gctest/hawrk/dfwj/ 下
'''
import os
import time
import datetime
import os.path
import codecs
import requests
import paramiko
import logging

CONST_HOST = "192.168.1.7"
CONST_USERNAME = "gczfth"
CONST_PWD = "89mfP2YY"
CONST_PORT = 40122
cmbc_dir_b_s = "/CMBC/"
cmbc_file_p_DK_CCDZ = "DF_GCZF_THWJ_"    #退汇文件
cmbc_file_DZWJ = "DF_GCZF_DK_DZWJ_"     #对账文件 垫资
cmbc_file_DZWJ_PAY = "DF_GCZF_DZWJ_"    #普通代付
#change in product enveriment
cmbc_dir_t_l = "/home/gctest/hawrk/dfwj/"

cmbc_file_t = ".txt"
#change in product enveriment
apiurl = 'http://api.tfb8.com/cgi-bin/v2.0/api_pay_reexchange.cgi?'

def sftp_get(date):

    #file = cmbc_dir_b_s+date+'/'+cmbc_file_p_DK_CCDZ + date + cmbc_file_t
    file_dz = cmbc_dir_b_s+date+'/'+cmbc_file_DZWJ + date + cmbc_file_t
    file_dz_pay = cmbc_dir_b_s+date+'/'+cmbc_file_DZWJ_PAY + date + cmbc_file_t
    des_dz = cmbc_dir_t_l + cmbc_file_DZWJ + date + cmbc_file_t
    des_pay = cmbc_dir_t_l + cmbc_file_DZWJ_PAY + date + cmbc_file_t
    try:
        t = paramiko.Transport((CONST_HOST, CONST_PORT))
        t.connect(username=CONST_USERNAME, password=CONST_PWD)
        sftp = paramiko.SFTPClient.from_transport(t)
        #垫资对账文件
        logging.info('src file [%s] dest file [%s]', file_dz,des_dz)
        sftp.get(file_dz, des_dz)
        logging.info("download file:[%s] OK!", file_dz)

        #普通对账文件
        logging.info('src file [%s] dest file [%s]', file_dz_pay, des_pay)
        sftp.get(file_dz_pay,des_pay)
        logging.info("download file:[%s] OK!", file_dz_pay)

        t.close()

    except Exception as e:
        logging.info("exception:%s" ,e)
        raise

def doWork(readfile,date):
    print ('readfie '+readfile)
    file = codecs.open(readfile,'r','utf-8')
    msg_data =file.read().strip('\r\n')

    print("file data = [" + msg_data +"]")
    logging.info("file data:[%s]",msg_data)
    logging.info("send to :[%s]",apiurl)
    r = requests.get(apiurl + 'filename=' + cmbc_file_p_DK_CCDZ+date + cmbc_file_t +'&msg_data=' + msg_data )
    print(r.url)
    print(r.encoding)
    print(r.content)

    ret_pos = r.content.find('<retcode>') + 9
    print(ret_pos)
    if ret_pos <= 0:
        print('process error!')
    else:
        ret_msg = r.content[ret_pos:ret_pos + 2]
        print('ret_msg=' + ret_msg)
        if ret_msg != "00":
            print('process fail!!')
        else:
            print('process succcess!!')
            # shutil.move(scandir+'/'+filename,bakdir+'/'+filename)

def run(interval):
    try:
        time_remaining = interval - time.time()%interval
        time.sleep(time_remaining)
        #下昨天的对账单
        curtime = time.strftime('%Y%m%d', time.localtime(time.time() - 24*60*60))
        logging.info('processing date=[%s]' , curtime)

        sftp_get(curtime)


        #doWork(read_file,curtime)
    except Exception  as e:
        print("exception:%s" % e)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s [line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%d %b %Y %H:%M:%S',
                        filename='/home/gctest/hawrk/log/download_reconciliation.log',
                        filemode='a')
    logging.info('*************begin*******************')
    interval = 1
    run(interval)
    logging.info("############## process end#######################")

'批量查找表中银行处理中的记录，查询银行状态，然后修改状态'
# 用法： 1.修改DB：mysql_host，mysql_port，mysql_user，mysql_passwd 数据库连接配置
#        2.修改查询条件： SPID，end_time，end_time
#        3.修改生产的URL query_api_url
#
__author__= 'hawrk'
__date__ = '2016.11.14'

import requests
import urllib.request
import pymysql
import time
import sys

mysql_host = '192.168.0.115'
mysql_port = 3306
mysql_user = 'depuser'
mysql_passwd = 'depuser'

SPID = '1000000068'
start_time  ='2016-07-04 00:00:00'
end_time = '2016-11-10 00:00:00'

query_api_url = 'http://api.gcdev.tfb8.com/cgi-bin/v2.0/api_pay_single_query_asyn.cgi?'
#query_api_url = 'http://api.tfb8.com/cgi-bin/v2.0/api_pay_single_query_asyn_hawrk.cgi?'

def send_query_requset(spid):
    try:
        conn = pymysql.connect(host=mysql_host, port=mysql_port, user=mysql_user, passwd=mysql_passwd, db='order_db',
                               charset='utf8mb4')
        cur = conn.cursor()
        sql = "select Flistid,Fspid from t_agent_pay_detail where Fcreate_time > '" + start_time + "' and Fcreate_time <'" + end_time+ "' and Fspid ='"+ spid + "' and Fstate =6"
        print ("sql = [%s]" %sql)

        cur.execute(sql)
        result = cur.fetchall()
        num = 1
        for row in result:
            print ("-----第 %d 笔处理开始---------" %num)
            data = {}
            data['sign_type'] = 'MD5'
            data['version'] = '1.0'
            data['tfb_serialno'] = str(row[0])
            data['spid'] = str(row[1])
            print("listid = [%s],spid = [%s]" %(data['tfb_serialno'],data['spid']))
            url_encode = urllib.parse.urlencode(data)
            send_url = query_api_url + url_encode
            print ('send_url = [%s]' %send_url)
            res = requests.get(send_url)
            print(res.url)
            print (res.content)
            print("#######第 %d 笔处理完成########" %num)
            print ('\n')
            num +=1
            #休眠一秒
            time.sleep(1)

        conn.commit()
    finally:
        conn.close()


if __name__ == '__main__':
    #if len(sys.argv) != 2:
        #print ('useage: python3 <python_file> spid')
        #exit(1)
    #spid = sys.argv[1]
    send_query_requset(SPID)

__author__ = 'hawrk'
__date__ = '2016.10.27'

import time
import requests
import urllib.request

from openpyxl import load_workbook

path = '/home/hawrk/doc/aa.xlsx'
encrypt_url = 'http://apitest.tfb8.com/cgi-bin/credit/api_txfq_for_testcgi.cgi?'
api_url = 'http://apitest.tfb8.com/cgi-bin/v2.0/api_pay_single.cgi?'

def read_07_excel(path):
    wb2 =  load_workbook(path)

    print (wb2.get_sheet_names())
    ws = wb2.get_sheet_by_name("Sheet4")


    for i in ws.rows:      #逐行读取数据
        print ('\n')

        list = []
        data = {}
        data['version'] = '1.0'
        data['sp_reqtime'] = '20161027121230'
        data['cur_type'] = '1'
        data['pay_type'] = '1'
        data['business_type'] = '20101'

        for cell in i:    #读取行中每列的数据
            list.append(cell.value)

        data['spid'] = list[0]
        data['sp_serialno'] = list[1]
        data['acct_id'] = list[2]
        data['acct_name'] = list[3]
        data['tran_amt'] = list[4]
        data['memo'] = list[5]

        url_values = urllib.parse.urlencode(data)
        encry_url = encrypt_url + url_values
        r = requests.get(encry_url)
        #print (r.url)
        #print (r.encoding)
        #print (r.content)

        #解析返回报文 ，得到加密串
        res_begin = r.content.find(b'<cipher_data>')
        res_end = r.content.find(b'</cipher_data>')
        #res_begin = r.content.find(b'<retcode>')
        #res_end = r.content.find(b'</retcode>')
        cipher_data = r.content[res_begin+13:res_end].decode()
        #print ("cipher_data = [%s]" %cipher_data)

        send_url = api_url + "cipher_data=" + cipher_data
        res = requests.post(send_url)
        print (res.url)
        print (res.content)

        #休眠2秒一笔
        time.sleep(2)


if __name__ == '__main__':
    read_07_excel(path)
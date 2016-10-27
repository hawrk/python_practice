__author__ = 'hawrk'
__date__ = '2016.09.19'

import pymysql

conn = pymysql.connect(host ='127.0.0.1',port = 3306,user = 'root',passwd = 'root.123',db = 'payment')

cur = conn.cursor()

cur.execute("select * from user")

for r in cur.fetchall():
    print (r[0])
    print (r[1])
    print (r[2])
conn.close()

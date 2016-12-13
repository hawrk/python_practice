__author__ = 'hawrk'
__date__ = '2016.10.20'

import urllib
import urllib.request

import collections


def py_deque():
    queue = collections.deque(["Eric","Jone","Michale"])
    queue.append("Terry")
    queue.append("Graham")

    queue.popleft()  #弹出Eric
    



url = "http://www.baidu.com/s?"

data = {}
data['word'] = 'Jecvay Notes'
url_values = urllib.parse.urlencode(data)   #将map格式 转化为 key1=value1&key2=value2的格式
full_url = url + url_values

print ("full_url = %s" %(full_url))


response = urllib.request.urlopen(full_url).read()

response = response.decode('UTF-8')

print (response)
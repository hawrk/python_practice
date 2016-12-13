import urllib.request
import os
import re

tar_path = 'douban_pic2'

def save_file(path):

    if not os.path.isdir(tar_path):
        os.mkdir(tar_path)
    pos = path.rindex('/')
    t = os.path.join(tar_path,path[pos+1:])
    return t

dou_url = 'https://www.douban.com/'
#伪装浏览器的方式
dou_headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',}

req = urllib.request.Request(url = dou_url,headers=dou_headers)
res = urllib.request.urlopen(req)

data = res.read()
#print (data.decode('UTF-8'))

for link,t in set(re.findall(r'(http.*?(jpg|png|gif))',str(data))):
    print (link)
    try:
        #直接将远程数据下载到本地   save_file为回调函数
        urllib.request.urlretrieve(link,save_file(link))
    except:
        print ('fail')
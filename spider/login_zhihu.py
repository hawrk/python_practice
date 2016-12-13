import urllib.request
import gzip
import re
import http.cookiejar
import urllib.parse
import sys

#unzip data
def ungzip(data):
    try:
        print('unzip begin...')
        data = gzip.decompress(data)
        print ('unzip end...')

    except:
        print ('no data to unzip...')

    return data

def get_opener(header):
    cookie_jar = http.cookiejar.CookieJar()
    cookie_process = urllib.request.HTTPCookieProcessor(cookie_jar)
    opener = urllib.request.build_opener(cookie_process)
    headers = []
    for key,value in header.items():
        elem = (key,value)
        headers.append(elem)
    opener.addheaders = headers
    return opener

def get_xsrf(data):
    cer = re.compile('name=\"_xsrf\" value=\"(.*)\"',flags = 0)
    strlist = cer.findall(data)
    return strlist[0]

headers = {
    'Connection': 'Keep-Alive',
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate,br',
    'Host': 'www.zhihu.com',
    'DNT': '1'
}

url = 'https://www.zhihu.com/'
req = urllib.request.Request(url,headers=headers)
res = urllib.request.urlopen(req)

data = res.read()
data = ungzip(data)
_xsrf = get_xsrf(data.decode('UTF-8'))

opener = get_opener(headers)

url += 'login/email'
name = '13424300536'
passwd = 'sk193752szu'

post_dict = {
    '_xsrf':_xsrf,
    'email':name,
    'password':passwd,
    'remeber_me':'true'
}

post_data = urllib.parse.urlencode(post_dict).encode()

res = opener.open(url,post_data)
data = res.read()

data = ungzip(data)
print (data.decode())


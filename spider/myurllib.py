
import urllib.parse
import urllib.request
import requests

zhihu_headers = {
    'Cookie':'d_c0="AIBA7w7Y0AqPTu8XTWsISJO3mO5asukYBiw=|1478593973"; '
             'q_c1=77ac3ead8b304737ac71cd1492a370b2|1478593974000|1478593974000; '
             'l_cap_id="NjM3ZWUwYzI5ZTZlNGYzMWFkODhlYzAxYWY1YjFlMzI=|1478593973|3e50e7cb472f31636ef073400d6cb9f4eaeab7f6"; '
             'cap_id="OTI5N2FlYmYzODE4NDg0OGE4M2U5YmQ3NTYxYzRlOGU=|1478593973|aacce24311ee4eb6b083a627bbbbba87ab7ac3e4"; '
             '_zap=820a395d-62c0-402a-9906-6654590e7ae2; '
             'login="ZWQ1NjFmMjkwNzkyNDI4Yzg5ODI4NTAxYTJkYWVmOGQ=|1478594349|813ef23388b0cf7d2543b5987ee89422630a3694";'
             ' _xsrf=a51d231d8ef6e8c9e12f27fbc10e4acc; n_c=1; __utma=51854390.873630118.1478593974.1478593974.1478593974.1;'
             ' __utmb=51854390.6.10.1478593974; __utmc=51854390; __utmz=51854390.1478593974.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); '
             '__utmv=51854390.100-1|2=registration_date=20140826=1^3=entry_date=20140826=1; '
             'a_t="2.0AAAAsMw1AAAXAAAAFx1JWAAAALDMNQAAAIBA7w7Y0AoXAAAAYQJVTUscSVgAWh0Biw8nXVP7CLjIL155JYwIqGbshnSp85OjR71bxrnGEz_KIFghKA=="; '
             'z_c0=Mi4wQUFBQXNNdzFBQUFBZ0VEdkR0alFDaGNBQUFCaEFsVk5TeHhKV0FCYUhRR0xEeWRkVV9zSXVNZ3ZYbmtsakFpb1pn|1478594583|c23b297c439430a2f7914a043e2dedd47bbf8b72',
    'Host':'www.zhihu.com',
    'User-Agent':'Mozilla/5.0	(Macintosh;	Intel	Mac	OS	X	10_11_4)	AppleWebKit/537.36	(KHTML,	like	Gecko)	Chrome/53.0.2785.116	Safari/537.36',

}

r = requests.get('https://www.zhihu.com/explore',headers = zhihu_headers)
print (r.text)


#result = urllib.parse.urlparse('http://www.baidu.com/index.html:user?id=5#comment')

#print (type(result),result)





import urllib
import urllib.request
#python3

sock = urllib.request.urlopen('http://www.baidu.com')

bytes = sock.read()
mystr = bytes.decode('utf-8')

print ('str =' + mystr)

urlobj = urllib.request.urlretrieve('http://www.hao123.com.cn','hao123')


sock.close()

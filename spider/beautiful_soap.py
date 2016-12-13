html = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

from bs4 import BeautifulSoup

soup = BeautifulSoup(html,'html5lib')

print (soup.prettify())


#print ("title:",soup.title)
#print ("name:",soup.title.name)
#print ("text:",soup.title.text)
#print ("body:",soup.body)

#get <a> text

print ('#######')
for link in soup.find_all('a'):
    print(link.get('href'))

print ("----------")
print (soup.get_text())
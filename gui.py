from urllib.request import urlopen
html = urlopen("http://onet.pl")
print(html.read())
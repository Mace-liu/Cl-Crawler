#coding=utf-8
import urllib  
import urllib2  
import re


def getUrlRespHtml(url):
    heads = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
            'Accept-Charset':'GB2312,utf-8;q=0.7,*;q=0.7', 
            'Accept-Language':'zh-cn,zh;q=0.5', 
            'Cache-Control':'max-age=0', 
            'Connection':'keep-alive', 
            'Host':'John', 
            'Keep-Alive':'115', 
            'Referer':url, 
            'User-Agent':'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.14) Gecko/20110221 Ubuntu/10.10 (maverick) Firefox/3.6.14'}
 
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    urllib2.install_opener(opener) 
    req = urllib2.Request(url)
    opener.addheaders = heads.items()
    respHtml = opener.open(req).read()
    return respHtml

def getref(html):#从HTML中获取ref
    reg = r'value=".+?"'
    urlre = re.compile(reg)
    rmdown = re.findall(urlre,html)
    return rmdown   
        

url_xunfs = 'http://www.xunfs.com/down.php?fc=152d9174ada074a7d34c04ea85cb915d76051e73c3e'#种子下载页地址

html = getUrlRespHtml(url_xunfs)
result = getref(html)

ref = result[0]
ref = ref[7:-1]
reff = result[1]
reff = reff[7:-1]

url_download = "http://www.xunfs.com/download.php" 
values = { 
	'ref' : ref,
	'reff' : reff,
	'submit' : 'Download',
}
postdata = urllib.urlencode(values) 
req = urllib2.Request(url_download, postdata) 
response = urllib2.urlopen(req)
the_page = response.read()
with open(ref+".torrent", "wb") as code:     
    code.write(the_page)

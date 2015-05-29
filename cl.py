#coding=utf-8

import urllib
import urllib2
import re
import time
import os
import socket
from color import Color
socket.setdefaulttimeout(30)#  设置加载页面超时时间

clr = Color()

urlpre = 'http://cl.bearhk.info/'  #设置网址前缀


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

def getHtml(url):#根据URL获取HTML源码
    page = urllib.urlopen(url)
    clr.print_yellow_text('url opening!')
    html = page.read()
    clr.print_green_text('url open ok!')
    return html

def getLable(html):#获取Lable
    r = []
    reg = r'<h3>.*?</h3>'
    urlre = re.compile(reg)
    urllist = re.findall(urlre,html)
    x = 0
    for allurl in urllist:
        r.append(allurl)
        print x,'url saved'
        x+=1
    return r

def getUrl(lable):#从Lable中获取连接 用于获取下一级HTML源码 以存储图片
    reg = r'htm_.+?\.html'
    urlre = re.compile(reg)
    urllist = re.findall(urlre,lable)
    return urllist

def getTitle(lable):#从Lable中获取标题用于创建文件夹的名称
    reg = r'id="">(.+?)</a>'
    urlre = re.compile(reg)
    titlelist = re.findall(urlre,lable)
    return titlelist

def getImg(html):#从HTML中获取图片
    reg = r"<img src='(.+?)'"
    imgre = re.compile(reg)
    imglist = re.findall(imgre,html)
    listlong = len(imglist)
    x = 0
    for imgurl in imglist:
        try:
            urllib.urlretrieve(imgurl,mkpath+'%s.jpg' % x) 
            x+=1
            print x,'/',listlong,'img saved'
        except socket.timeout:#如果超时 报错 并跳过继续执行
            clr.print_red_text('timeout')
    
def getrmdown(html):#从HTML中获取RMDOWN地址
    reg = r'hash=.+?">'
    urlre = re.compile(reg)
    rmdown = re.findall(urlre,html)
    return rmdown   

def getref(html):#从HTML中获取ref
    reg = r'value=".+?"'
    urlre = re.compile(reg)
    rmdown = re.findall(urlre,html)
    return rmdown   
        

def mkdir(path):
    
    # 去除首位空格
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")
 
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)
 
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        print path+' creat ok'
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print path+' Already exists'
        return False
 

lasturl = "thread0806.php?fid=2"
    
firsturl = urlpre+lasturl

html = getUrlRespHtml(firsturl)#设置要爬的页面地址！

a = getLable(html)

now = time.strftime('%Y-%m-%d-%H-%M',time.localtime(time.time()))#获取当前系统时间

for x in range(6,len(a)):
    try:
        print x,'/',len(a),'url opened'
        lable =  a[x] 

        title  = getTitle(lable)

        urlsuf = getUrl(lable)

        url = urlpre+urlsuf[0]  #合成URL

        imghtml = getUrlRespHtml(url)

        print 'open all page'

        title =title[0].replace('/','');# 去掉/符号  因为会导致路径创建错误

        filename = now

        mkpath="d:\\cl\\"+filename+"\\"+title+"\\"#设置存储路径

        mkdir(mkpath)  # 调用路径创建函数

        print 'root over'

        rmdown = getrmdown(imghtml)
        torrenturl = rmdown[0]
        torrenturl = torrenturl[5:-4]
        torrenturl = 'http://www.xunfs.com/down.php?fc='+torrenturl


        f = open(mkpath+'page.txt', 'w')

        f.write(url+'\n'+torrenturl)

        f.close()

        clr.print_green_text('url saved ')

        print getImg(imghtml)

        url_xunfs = torrenturl#种子下载页地址
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
        with open(mkpath+ref+".torrent", "wb") as code:     
            code.write(the_page)


        clr.print_green_text('this page over')

    except Exception, e:#如果出错 则报错 并跳过

        clr.print_red_text('error')


raw_input('over')
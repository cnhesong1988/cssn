#coding=utf-8
import urllib2
from lxml import etree
import random
import threading
import time

class WebProxy():    
    
    def __init__(self,ip,port):

        self.header = {'Accept-Charset':'GBK,utf-8;q=0.7,*;q=0.3','User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.151 Safari/534.16'}
        self.ip = ip
        self.port = port


    def isAlive(self):
        proxy={'http':self.ip+':'+self.port}
        print "isAlive"
        print proxy

        #使用这个方式是全局方法。
        proxy_support=urllib2.ProxyHandler(proxy)
        opener=urllib2.build_opener(proxy_support)
        urllib2.install_opener(opener)
        #使用代理访问腾讯官网，进行验证代理是否有效
        test_url="http://www.qq.com"
        try:
            req=urllib2.Request(test_url,headers=self.header)
            #timeout 设置为10，如果你不能忍受你的代理延时超过10，就修改timeout的数字
            resp=urllib2.urlopen(req,timeout=10)

            if resp.code==200:
                print "work"
                return True
            else:
                print "not work"
                return False
        except Exception, e:
            print "isAlive Exception....."
            print e
            return False

class WebProxyReader():

    def __init__(self):
        self.header = {'Accept-Charset':'GBK,utf-8;q=0.7,*;q=0.3','User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.151 Safari/534.16'}
        self.ip_portList = []
    
    def getConent(self):
        nn_url = "http://tvp.daxiangdaili.com/ip/?tid=556615738536308&filter=on&num=10&ports=80,8080,3128"
        
        #国内高匿
        try:
            req = urllib2.Request(nn_url, headers=self.header)
            resp = urllib2.urlopen(req, timeout=10)
            content = resp.read()
            self.ip_portList = content.split("\r\n")
            print self.ip_portList
        except Exception, e:
            print "findAProxy Exception...."
            print e 
            return
    
    def findAWebProxy(self):
        while(True):
            if len(self.ip_portList)<>0:
                ip_port = self.ip_portList.pop()
                webProxy = WebProxy(ip_port.split(":")[0],ip_port.split(":")[1])
                if webProxy.isAlive():
                    return webProxy
            else:
                self.getConent()


#class CSSN(threading.Thread):
class CSSN():

    def __init__(self,no,url1,url2,webProxy):
        #threading.Thread.__init__(self) 
        self.no=no
        self.url1=url1
        self.url2=url2
        self.webProxy=webProxy

    def run(self):
        proxy={'http':self.webProxy.ip+':'+self.webProxy.port}
        print "visitWeb"+" NO:"+str(self.no)
        print proxy

        #使用这个方式是全局方法。
        proxy_support=urllib2.ProxyHandler(proxy)
        opener=urllib2.build_opener(proxy_support)
        opener=urllib2.build_opener()
        urllib2.install_opener(opener)

        try:
            urlArray=[]
            req=urllib2.Request(self.url1, headers=self.webProxy.header)
            resp = urllib2.urlopen(req, timeout=10)
            content = resp.read()
            page = etree.HTML(content.decode('utf-8'))
            result=page.xpath("//section/p/a")
            urlArray.append(url1+result[0].attrib['href'][2:])
            result=page.xpath("//section/ul/li/a")
            i=0
            while i<20:
                urlArray.append(url1+result[i].attrib['href'][2:])
                i+=1

            i=0
            while i<10:
                i+=1
                cnt = random.randint(0, 20)
                urlE = urlArray[cnt]
                print "Ready to visit "+str(cnt)+" "+urlE+" NO:"+str(self.no)
                try:
                    req=urllib2.Request(urlE, headers=webProxy.header)
                    resp = urllib2.urlopen(req, timeout=10)
                    content = resp.read()

                except Exception, e:
                    print "visit ERROR"+" NO:"+str(self.no)
                    print e
                else:
                    print "visit over"+" NO:"+str(self.no)

        except Exception, e:
            print "url1 failed"+" NO:"+str(self.no)
            print "run Exception...."
            print e
            pass
        
        try:
            urlArray=[]
            req=urllib2.Request(self.url2, headers=self.webProxy.header)
            resp = urllib2.urlopen(req, timeout=10)
            content = resp.read()
            page = etree.HTML(content.decode('utf-8'))
            result=page.xpath("//section/p/a")
            urlArray.append(url2+result[0].attrib['href'][2:])
            result=page.xpath("//section/ul/li/a")
            i=0
            while i<20:
                urlArray.append(url2+result[i].attrib['href'][2:])
                i+=1

            i=0
            while i<12:
                i+=1
                cnt = random.randint(0, 20)
                urlE = urlArray[cnt]
                print "Ready to visit "+str(cnt)+" "+urlE+" NO:"+str(self.no)
                try:
                    req=urllib2.Request(urlE, headers=webProxy.header)
                    resp = urllib2.urlopen(req, timeout=10)
                    content = resp.read()

                except Exception, e:
                    print "visit ERROR"+" NO:"+str(self.no)
                    print e
                else:
                    print "visit over"+" NO:"+str(self.no)
        except Exception, e:
            print "url2 failed"+" NO:"+str(self.no)
            pass

    def stop(self):
        print "Stop"+" NO:"+str(self.no)
        self.thread_stop = True


if __name__ == "__main__":
    webProxyReader = WebProxyReader()
    url1="http://m.cssn.cn/gxx/"
    url2="http://m.cssn.cn/skysklx/"
    webProxyReader = WebProxyReader()
    i = 0
    while i<40:
        webProxy = webProxyReader.findAWebProxy()
        time.sleep(5)
        print "Try to Work..........."
        if webProxy != None:
            i+=1;
            cssn = CSSN(i,url1,url2,webProxy)
            cssn.run()
            #cssn.setDaemon(True)
            #cssn.start()




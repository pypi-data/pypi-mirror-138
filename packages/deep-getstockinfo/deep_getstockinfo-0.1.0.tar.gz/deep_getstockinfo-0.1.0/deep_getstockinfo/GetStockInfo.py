#此类实现利用不同的行情接口获取行情信息
#2022/02/10         1. 实现腾讯接口，新浪待修复
#                   2. 增加获取名称，昨天收盘价等方法
#                   3. 调用获取具体信息方法前，必须先调用getStockInfo方法


import re
import requests
import time

class GetStockInfo():
    def __init__(self,API = 'tencent'):
        self.api = API
        self.si = []
        
    def getHtmlText(self,url):
   
        try:
            r = requests.get(url, timeout = 30)
            r.raise_for_status()
        #r.encoding = r.apparent_encoding

            return r.text
        except:
            return ""

    def getStockInfo(self,code):									#修改为用腾讯API, 2022/1/21

        if self.api == 'tencent':
           
            url = "http://qt.gtimg.cn/q=" + code					# 腾讯URL
            stock = self.getHtmlText(url)
            time.sleep(1)
            self.si = stock.split('~') 
        elif self.api == 'sina':                                    # 新浪待修复
            url = "http://hq.sinajs.cn/list=" + code
            stock = self.getHtmlText(url)
            time.sleep(1)
            stockInfo =  re.findall(r'"(.+?)"', stock)	
            self.si = stockInfo[0].split(',')

    def getStockClosePrice(self):                                   #用收盘后当前价代替当日收盘价

        if self.si == []:
            return "Stock Info Not Initialized"

        if self.api == 'tencent':
            return self.si[3]	
        elif self.api == 'sina':
            return self.si[3]

    def getStockCurrentPrice(self):                                   

        if self.si == []:
            return "Stock Info Not Initialized"

        if self.api == 'tencent':
            return self.si[3]   
        elif self.api == 'sina':
            return self.si[3]

    def getStockName(self):                                    

        if self.si == []:
            return "Stock Info Not Initialized"

        if self.api == 'tencent':
            return self.si[1]    
        elif self.api == 'sina':
            return self.si[0]

    def getStockYesterdayClosePrice(self):                           

        if self.si == []:
            return "Stock Info Not Initialized"

        if self.api == 'tencent':
            return self.si[4]    
        elif self.api == 'sina':
            return self.si[2]
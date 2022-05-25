from requests_html import HTMLSession
from requests import exceptions 
import json
from threading import Thread, Lock
from time import sleep

Bee_URL = "https://www.beesproxy.com/free/page/{}"
Cloud_URL = "http://www.ip3366.net/?stype=1&page={}"
Kuaidaili_URL = "https://free.kuaidaili.com/free/inha/{}"

class Proxy():
    """
        多线程共享变量balance
        引入lock锁
    """
    def __init__(self):
        self.session = HTMLSession()
        self.proxy_lists = []; # 共享变量proxy_lists
        self._lock = Lock()
        
    def Get_html(self, URL , n):
        """_summary_

        Args:
            URL (str): 模板URL
            n (int): 爬取页数 

        Returns:
            _type_: 返回html
        """
        html_list = []
        for i in range(1, n+1):
            url = URL.format(i)
            try:
                response = self.session.get(url)
            except exceptions.ConnectionError:
                print('[+]代理爬取失败...')
                continue
            except exceptions.Timeout:
                print('[+]代理爬取超时...')
                continue
            except:
                print('[+]未知错误')
                continue
            html_list.append(response.html)
        return html_list
    
    def Bee(self):
        print("[+]正在爬取Bee")
        for html in self.Get_html(Bee_URL, 3):
            tmp = []
            for tr in html.xpath('''//tbody/tr'''):
                dicts = {}
                ip = tr.text.split("\n")[0]
                port = tr.text.split("\n")[1]
                url = "http://" + ip + ":" + port
                dicts['http'] = url
                tmp.append(dicts)
            self._lock.acquire()   
            try:
                sleep(0.01)
                self.proxy_lists.extend(tmp)
            finally:
                self._lock.release()
    
    def Cloud(self):
        print("[+]正在爬取Cloud")
        for html in self.Get_html(Cloud_URL, 3):
            tmp = []
            for tr in html.xpath('''//tbody/tr'''):
                dicts = {}
                ip = tr.text.split("\n")[0]
                port = tr.text.split("\n")[1]
                type = tr.text.split("\n")[3].lower()
                url = type + "://" + ip + ":" + port
                dicts[type] = url   
                tmp.append(dicts)
            self._lock.acquire()   
            try:
                sleep(0.01)     
                self.proxy_lists.extend(tmp)
            finally:
                self._lock.release()
    
    def Kuaidaili(self):
        print("[+]正在爬取Kuaidaili")
        for html in self.Get_html(Kuaidaili_URL, 3):
            tmp = []
            for tr in html.xpath('''//tr''')[1:]:
                dicts = {}
                ip = tr.text.split("\n")[0]
                port = tr.text.split("\n")[1]
                type = tr.text.split("\n")[3].lower()
                url = type + "://" + ip + ":" + port
                dicts[type] = url   
                tmp.append(dicts)
            self._lock.acquire()   
            try:
                sleep(0.01)     
                self.proxy_lists.extend(tmp)
            finally:
                self._lock.release()

    def get_lists(self):
        t1 = Thread(target = self.Bee())
        t2 = Thread(target = self.Cloud())
        t3 = Thread(target= self.Kuaidaili())
        t1.start()
        t2.start()
        t3.start()
        t1.join()
        t2.join()
        t3.join()
        return self.proxy_lists
            

def get_proxy():
    proxy = Proxy()
    proxylist = proxy.get_lists()
    with open('ip.json','w+',encoding='utf8') as f:
        json.dump(proxylist,f)
        f.close()
    return len(proxylist)

if __name__ == "__main__":
    proxy = Proxy()
    proxylist = proxy.get_lists()
    print("共爬取: "+ str(len(proxylist)))
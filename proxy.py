from requests_html import HTMLSession
from requests import exceptions 
import json
BASE_URL = "https://www.beesproxy.com/free/page/{}"
class Proxy():
    def __init__(self):
        self.session = HTMLSession()
        self.proxy_lists = [];
    
    def get_lists(self):
        url = BASE_URL.format(1)
        try:
            response = self.session.get(url)
        except exceptions.ConnectionError:
            print('[+]代理爬取失败...')
            return -1
        except exceptions.Timeout:
            print('[+]代理爬取超时...')  
            return -1
        except:
            print('[+]未知错误')
            return -1
        html = response.html
        for tr in html.xpath('''//tbody/tr'''):
            dicts = {}
            ip = tr.text.split("\n")[0]
            port = tr.text.split("\n")[1]
            url = "http://" + ip + ":" + port
            dicts['http'] = url
            self.proxy_lists.append(dicts)
        return self.proxy_lists
            

def get_proxy():
    proxy = Proxy()
    proxylist = proxy.get_lists()
    if (proxylist==-1):
        return -1
    else:
        with open('ip.json','w+',encoding='utf8') as f:
            json.dump(proxylist,f)
            f.close()
        return 1

if __name__ == "__main__":
    proxy = Proxy()
    proxylist = proxy.get_lists()
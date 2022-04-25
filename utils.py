import msvcrt
from time import sleep
from random import choice
from requests import exceptions 
from requests_html import HTMLSession

agentlist = list()
with open('useragent.txt', 'r', encoding='utf-8') as f:
    for line in f:
        agentlist.append(str(line).rstrip('\n'))
        
class Spider(object):
    """爬虫类, 内置post, get, get_json方法
    """
    def __init__(self, Cookie):
        self._session = HTMLSession()
        self._headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.44",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Referer": "https://s.weibo.com/",
            "Accept-Encoding": "deflate, br",
            "Accept-Language": "en-GB,en;q=0.8,zh-CN;q=0.6,zh;q=0.4"           
        }
        self._cookie = Cookie
        
    def get(self, url):
        try :
            req = self._session.get(url, headers=self.change_agent(), cookies=self._cookie)
        except exceptions.Timeout as e:
            print('请求超时：'+str(e.message))
        except exceptions.HTTPError as e:
            print('http请求错误:'+str(e.message))
        return req
    
    def get_json(self,url):
        flag = True
        while flag:
            try:
                flag = False
                json_dict = self.get(url).json()
            except exceptions.JSONDecodeError:
                print("[+]请求失败,正在重新请求...")
                sleep(1)
                flag = True
        return json_dict

    def change_agent(self):
        global agentlist
        self._headers['User-Agent'] = choice(agentlist)
        return self._headers
    
class bcolors: #终端文本颜色设置
    OKBLUE = '\033[1;94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[5;94m'
    FAIL = '\033[91m'
    BLUE = '\033[1;36m'
    ENDC = '\033[0;36m'
    BOLD = '\033[1m'
    RED = '\033[1;31m'
    RED1 = '\033[0;31m'
    
def pwd_input():
    """实现密码隐藏输入
    """
    chars = []
    while True:
        newChar = msvcrt.getch().decode(encoding="utf-8")
        if newChar in '\r\n':  # 如果是换行，则输入结束
            break
        elif newChar == '\b':  # 如果是退格，则删除密码末尾一位并且删除一个星号
            if chars:
                del chars[-1]
                msvcrt.putch('\b'.encode(encoding='utf-8'))  # 光标回退一格
                msvcrt.putch(' '.encode(encoding='utf-8'))  # 输出一个空格覆盖原来的星号
                msvcrt.putch('\b'.encode(encoding='utf-8'))  # 光标回退一格准备接受新的输入
        else:
            chars.append(newChar)
            msvcrt.putch('*'.encode(encoding='utf-8'))  # 显示为星号
    return (''.join(chars))

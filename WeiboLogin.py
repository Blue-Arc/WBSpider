import base64
import binascii
import json
import re
import ssl
import time
import urllib
from http import cookiejar

import requests
import rsa

ssl._create_default_https_context = ssl._create_unverified_context


def get_ticket(html):
    pattern = r'ticket=.+?&'
    ticket = re.search(pattern, html).group()[7:-1]

    return ticket


def get_ssosavestate(html):
    pattern = r'ssosavestate=\d+'
    ssosavestate = re.search(pattern, html).group()[13:]

    return ssosavestate


class loginClient(object):

    def __init__(self, debug=False):
        """客户端登录

        Args:
            debug (bool, optional): debug选项. Defaults to False.
        """
        self.cookiejar = cookiejar.CookieJar()
        self.handler = urllib.request.HTTPCookieProcessor(self.cookiejar)
        self.openner = urllib.request.build_opener(self.handler)
        self.headers = {
            "Origin": "https://login.sina.com.cn",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Referer": "https://login.sina.com.cn/signup/signin.php?entry=sso",
            "Accept-Encoding": "deflate, br",
            "Accept-Language": "en-GB,en;q=0.8,zh-CN;q=0.6,zh;q=0.4"
        }

        self.postData = {"cdult": "3",
                         "domain": "sina.com.cn",
                         "encoding": "UTF-8",
                         "entry": "sso",
                         "from": "",
                         "gateway": "1",
                         "nonce": None,
                         "pagerefer": "http://login.sina.com.cn/sso/logout.php",
                         "prelt": "46",
                         "pwencode": "rsa2",
                         "returntype": "TEXT",
                         "rsakv": None,
                         "savestate": "30",
                         "servertime": None,
                         "service": "sso",
                         "sp": None,
                         "sr": "1366*768",
                         "su": None,
                         "useticket": "0",
                         "vsnf": "1"
                         }

        self.cookies = {}  # for requests "requests.get(url = url, data = data, headers = headers, cookies = self.cookies)"

        self.debug = debug

    def prelogin(self):
        url = r'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=&rsakt=mod&client=ssologin.js(v1.4.18)'
        html = requests.get(url, headers=self.headers).text

        jsonStr = re.findall(r'\((\{.*?\})\)', html)[0]
        prelogin_response = json.loads(jsonStr)

        if self.debug:
            print('prelogin_response =', prelogin_response)

        return prelogin_response

    def login(self):
        login_url = r'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)'

        login_request = urllib.request.Request(
            url=login_url,
            data=bytes(urllib.parse.urlencode(self.postData), encoding='utf8'),
            headers=self.headers,
            method='POST'
        )
        login_response = self.openner.open(login_request)
        login_response = json.loads(login_response.read().decode('utf8'))

        if self.debug:
            print('login_response =', login_response)
        
        return login_response

    def send_privateMessage(self, token):
        protection_url = 'https://passport.weibo.com/protection/privatemsg/send'
        postData = {'token': token}
        send_privateMessage_request = urllib.request.Request(
            url=protection_url,
            data=bytes(urllib.parse.urlencode(postData), encoding='utf8'),
            headers=self.headers,
            method='POST'
        )
        send_privateMessage_response = self.openner.open(send_privateMessage_request)
        send_privateMessage_response = json.loads(send_privateMessage_response.read().decode('utf8'))
        if self.debug:
            print('send_privateMessage_response =', send_privateMessage_response)

        return send_privateMessage_response

    def check_approvalStatus(self, token):
        getstatus_url = 'https://passport.weibo.com/protection/privatemsg/getstatus'
        postData = {'token': token}
        check_approvalStatus_request = urllib.request.Request(
            url=getstatus_url,
            data=bytes(urllib.parse.urlencode(postData), encoding='utf8'),
            headers=self.headers,
            method='POST'
        )
        check_approvalStatus_response = self.openner.open(check_approvalStatus_request)
        check_approvalStatus_response = json.loads(check_approvalStatus_response.read().decode('utf8'))
        if self.debug:
            print('check_approvalStatus_response =', check_approvalStatus_response)

        return check_approvalStatus_response

    def request_crossdomain1(self, crossdomain1_url):
        crossdomain1_request = urllib.request.Request(
            url=crossdomain1_url,
            headers=self.headers,
            method='GET'
        )
        crossdomain1_response = self.openner.open(crossdomain1_request)
        crossdomain1_response_text = crossdomain1_response.read().decode('GBK')

        if self.debug:
            print('crossdomain1_response_text =', crossdomain1_response_text)

        return crossdomain1_response_text

    def request_crossdomain2(self, crossdomain2_url):
        crossdomain2_url_request = urllib.request.Request(
            url=crossdomain2_url,
            headers=self.headers,
            method='GET'
        )
        crossdomain2_url_response = self.openner.open(crossdomain2_url_request)
        crossdomain2_response_text = crossdomain2_url_response.read().decode('GBK')

        if self.debug:
            print('crossdomain2_response_text =', crossdomain2_response_text)

        return crossdomain2_response_text

    def request_final(self, ticket, ssosavestate):
        final_url = 'https://passport.weibo.com/wbsso/login?ticket=' + ticket + '&ssosavestate=' + ssosavestate + '&callback=sinaSSOController.doCrossDomainCallBack&scriptId=ssoscript0&client=ssologin.js(v1.4.19)'
        request = urllib.request.Request(
            url=final_url,
            headers=self.headers,
            method='GET'
        )
        response = self.openner.open(request)

        final_url_response_text = response.read().decode('GBK')
        if self.debug:
            print('final_url_response_text = ', final_url_response_text)

        return final_url_response_text

    def main(self, username:str, password:str):
        """客户端主函数

        Args:
            username (str): 用户名
            password (str): 密码

        Returns:
            cookie: 返回cookie值
        """
        prelogin_response = self.prelogin()

        nonce = prelogin_response["nonce"]
        rsakv = prelogin_response["rsakv"]
        servertime = prelogin_response["servertime"]

        pubkey = prelogin_response["pubkey"]
        rsaPubkey = int(pubkey, 16)
        RSAKey = rsa.PublicKey(rsaPubkey, 65537)  # 创建公钥

        codeStr = str(servertime) + '\t' + str(nonce) + '\n' + str(password)  # 根据js拼接方式构造明文
        pwd = rsa.encrypt(bytes(codeStr, 'utf-8'), RSAKey)  # 使用rsa进行加密
        sp = binascii.b2a_hex(pwd)

        su = base64.encodebytes(bytes(username, 'utf-8'))[:-1]

        self.postData["nonce"] = nonce
        self.postData["rsakv"] = rsakv
        self.postData["servertime"] = servertime
        self.postData["sp"] = sp
        self.postData["su"] = su

        login_response = self.login()
        if login_response['retcode'] == '101':
            return -1
        token = login_response['protection_url'].split('%3D')[-1]
        if self.debug == True:
            print('token = ', token)

        send_privateMessage_response = self.send_privateMessage(token)

        approved = False
        while not approved:
            time.sleep(5)
            print("[+]请打开微博手机端授权登陆!")
            check_approvalStatus_response = self.check_approvalStatus(token)
            if check_approvalStatus_response['data']['status_code'] == '2':
                print("[+]微博手机端已授权!")
                approved = True

        crossdomain1_url = check_approvalStatus_response['data']['redirect_url'][:-26] + 'http%3A%2F%2Fmy.sina.com.cn'
        if self.debug:
            print('crossdomain1_url =', crossdomain1_url)

        crossdomain1_response_text = self.request_crossdomain1(crossdomain1_url)

        pattern = r'https://.+?&#39;'
        crossdomain2_url = re.search(pattern, crossdomain1_response_text).group()[:-5]
        if self.debug:
            print('crossdomain2_url =', crossdomain2_url)

        crossdomain2_response_text = self.request_crossdomain2(crossdomain2_url)

        ticket = get_ticket(crossdomain2_response_text)
        if self.debug:
            print('ticket =', ticket)

        ssosavestate = get_ssosavestate(crossdomain2_response_text)
        if self.debug:
            print('ssosavestate =', ssosavestate)

        final_url_response_text = self.request_final(ticket, ssosavestate)

        # extract cookies
        cookie_dict = {}
        for cookie in self.cookiejar:
            cookie_dict[cookie.name] = cookie.value
        cookies = "; ".join(cookie + "=" + cookie_dict[cookie] for cookie in cookie_dict)
        self.cookies['Cookies'] = cookies
        if self.debug:
            print('cookies =', self.cookies['Cookies'])

        login_result_dict = json.loads(final_url_response_text[40:-3])
        if self.debug:
            print('login_result_dict =', login_result_dict)

        if login_result_dict['result'] == False:
            self.cookies = -1
        return self.cookies




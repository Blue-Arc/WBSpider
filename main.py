from WeiboLogin import loginClient

def execute(uname:str, passwd:str):
    """登录到微博

    Args:
        uname (str): 用户名
        passwd (str): 密码
    """
    client = loginClient(debug=True)
    cookie = client.main(uname, passwd)
    # if cookie == -1:
    #     print("[+]用户名或密码错误请重新输入!\n")
    # else:
    #     with open('cookies.json','w+') as f:
    #         json.dump(cookie,f)
    #     print("[+]登录成功")
    return cookie




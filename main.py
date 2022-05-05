from WeiboLogin import loginClient

def execute(uname:str, passwd:str):
    """登录到微博

    Args:
        uname (str): 用户名
        passwd (str): 密码
    """
    client = loginClient(debug=True)
    cookie = client.main(uname, passwd)
    return cookie




import json
from time import sleep

from info import Info
from utils import bcolors, pwd_input
from WeiboLogin import loginClient

if __name__ == '__main__':
    logo = """
        ██╗    ██╗██████╗ ███████╗██████╗ ██╗██████╗ ███████╗██████╗ 
        ██║    ██║██╔══██╗██╔════╝██╔══██╗██║██╔══██╗██╔════╝██╔══██╗
        ██║ █╗ ██║██████╔╝███████╗██████╔╝██║██║  ██║█████╗  ██████╔╝
        ██║███╗██║██╔══██╗╚════██║██╔═══╝ ██║██║  ██║██╔══╝  ██╔══██╗
        ╚███╔███╔╝██████╔╝███████║██║     ██║██████╔╝███████╗██║  ██║
        ╚══╝╚══╝ ╚═════╝ ╚══════╝╚═╝     ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝  
                                                                by BlueArc                                          
    """
    print(logo)
    print("[+]正在读取用户cookie文件......")
    sleep(2)
    try:
        with open('cookies.json', 'r') as f:
            singal = input("[+]读取到一个cookie信息,是否使用?[Y/N]")
            if singal == 'N':
                raise FileNotFoundError
            else:
                print("[+]用户cookie读取成功!")
                cookie = json.load(f)
    except FileNotFoundError:
        print('[+]cookie读取错误,请使用账号密码登录!')
        client = loginClient(debug=False)
        while True:
            uname = input(">请输入登录名(手机/邮箱/用户名):\n")
            print(">请输入密码:")
            passwd = pwd_input()
            print("\n[+]正在登录请稍后.........")
            cookie = client.main(uname, passwd)
            if cookie == -1:
                print("[+]用户名或密码错误请重新输入!\n")
            else:
                with open('cookies.json','w+') as f:
                    json.dump(cookie,f)
                print("[+]登录成功")
                break
    info = Info(cookie)
    while True:
        try:
            inputstr = input('{}┌──({}WBSpider😄bluearc{}){}{}{}\n{}└─{}# '.format(
                bcolors.BLUE,
                bcolors.RED,
                bcolors.BLUE,
                bcolors.OKBLUE,
                bcolors.BLUE,
                bcolors.BLUE,
                bcolors.BLUE,
                bcolors.ENDC)) #读取命令
        except EOFError:
            break
        orderlist = inputstr.split(' ') #parts列表存储命令
        if len(orderlist) == 1:
            orderlist.append(' ')
        if orderlist[0] == 'exit':
            break
        if orderlist[0] == 'help':
            print("  "+ "-"*60)
            print("   [1]    ", "set".ljust(15, " "), "Set target")
            print("   [2]    ", "showinfo".ljust(15, " "), "Show info")
            print("   [3]    ", "getfollowers".ljust(15, " "), "Get followers")
            print("   [4]    ", "getfriends".ljust(15, " "), "Get friends")
            print("   [5]    ", "getstatuses".ljust(15, " "), "Get statuses")
            print("   [6]    ", "getcomments".ljust(15, " "), "Get comments by input num")
            print("  "+ "-"*60)
            continue
        if orderlist[0] == 'set':
            uname = orderlist[1]
            print("[+]选择目标:%s " % uname,"正在为您搜索相关用户......")
            uid = info.get_Info(uname)
            continue
        if orderlist[0] == 'showinfo':
            print("个人信息")
            info.show_Info(uid)
            continue
        if orderlist[0] == 'getfriends':
            print("关注人信息(前10位)")
            info.get_Friends(uid)
            continue
        if orderlist[0] == 'getfollowers':
            print("粉丝信息(前10位)")
            info.get_Followers(uid)
            continue
        if orderlist[0] == 'getstatuses':
            print("获取前10条微博动态")
            json_dict = info.get_Statuses(uid)
            continue
        if orderlist[0] == 'getcomments':
            print("获取当前动态评论")
            num = orderlist[1]
            info.get_Comments(num, uid, json_dict)
            continue 
        else:
            print("命令错误,请输入help查看命令")
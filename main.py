import json
from time import sleep
from multiprocessing import Process
from info import Info
from utils import bcolors, pwd_input
from WeiboLogin import loginClient

sign = True

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
    sleep(1)
    try:
        with open('cookies.json', 'r') as f:
            singal = input("[+]读取到一个cookie信息,是否使用?[Y/N]")
            if singal == 'N' or singal == 'n':
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
    print("[+]正在验证cookie有效性")
    info = Info(cookie)
    if (info.cookie_validate()):
        print("[+]cookie已失效, 请重新登录!")
        exit(0)
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
            print("   [1]    ", "set 'name'".ljust(15, " "), "Set target by name")
            print("   [2]    ", "showinfo".ljust(15, " "), "Show target info")
            print("   [3]    ", "getfollowers".ljust(15, " "), "Get target followers")
            print("   [4]    ", "getfriends".ljust(15, " "), "Get target friends")
            print("   [5]    ", "getstatuses".ljust(15, " "), "Get target statuses")
            print("   [6]    ", "getcomments 'num' ".ljust(15, " "), "Get comments by num")
            print("   [7]    ", "getallcomments".ljust(15, " "), "Get all comments")
            print("  "+ "-"*60)
            continue
        if orderlist[0] == 'set':
            uname = orderlist[1]
            if sign:
                print("[+]选择目标:%s " % uname,"正在为您搜索相关用户......")
                uid = info.get_Info(uname)
                p = Process(target=info.start_surpervise, args=(uid, ))
                p.start()
                sign = False
                continue
            if p.is_alive:
                p.terminate()
                sleep(2)
                print('检测到目标已更改')
                p.join()
                print("[+]选择目标:%s " % uname,"正在为您搜索相关用户......")
                uid = info.get_Info(uname)
                p = Process(target=info.start_surpervise, args=(uid, ))
                p.start()
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
        if orderlist[0] == 'get_all_comments':
            print("获取所有动态评论")
            info.get_AllComments(uid)
            continue 
        else:
            print("命令错误,请输入help查看命令")
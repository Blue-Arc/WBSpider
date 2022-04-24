## Feature

1. 通过帐户密码登录，手机端手动验证
2. 支持cookie文件读取
3. 支持关键词搜索用户
5. 支持随机agent替换，防反爬
4. 爬取用户详细信息
5. 爬取用户关注和粉丝信息
6. 爬取用户热点微博及相关评论

### 运行 

- 方法一：使用Git:  

```shell
git clone https://github.com/Blue-Arc/WBSpider.git/
```

> 墙国加速
>  
> ```shell
> git clone https://github.do/https://github.com/Blue-Arc/WBSpider.git
> ```


### 配置环境  

> **请确保自己的电脑有 `python3.x` 的环境,推荐使用 `3.8` 及以上！**  

- 安装 pipenv 包管理工具.  

```shell
pip install pipenv  # windows
```

- 为项目构建虚拟环境.  

```shell
pipenv shell
pipenv install
```

- 尝试运行 main.py  

```shell
python main.py # windows
```

若无报错，输出帮助信息，则说明环境已经正确安装。

### 运行  

```shell
# 输出帮助信息
# python .\main.py

        ██╗    ██╗██████╗ ███████╗██████╗ ██╗██████╗ ███████╗██████╗
        ██║    ██║██╔══██╗██╔════╝██╔══██╗██║██╔══██╗██╔════╝██╔══██╗
        ██║ █╗ ██║██████╔╝███████╗██████╔╝██║██║  ██║█████╗  ██████╔╝
        ██║███╗██║██╔══██╗╚════██║██╔═══╝ ██║██║  ██║██╔══╝  ██╔══██╗
        ╚███╔███╔╝██████╔╝███████║██║     ██║██████╔╝███████╗██║  ██║
        ╚══╝╚══╝ ╚═════╝ ╚══════╝╚═╝     ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝
                                                                by BlueArc

[+]正在读取用户cookie文件......
[+]读取到一个cookie信息,是否使用?[Y/N]Y
[+]用户cookie读取成功!
┌──(WBSpider😄bluearc)
└─# 
```

- 启动轰炸  

帮助信息:

```shell
┌──(WBSpider😄bluearc)
└─# help
  ------------------------------------------------------------
   [1]     set             Set target
   [2]     showinfo        Show info
   [3]     getfollowers    Get followers
   [4]     getfriends      Get friends
   [5]     getstatuses     Get statuses
   [6]     getcomments     Get comments by input num
  ------------------------------------------------------------
```

### Todo list
- [ ] 多线程异步爬取
- [ ] web可视化

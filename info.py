import json
from utils import Spider

class Info(object):
    def __init__(self, cookie):
        self.spider = Spider(Cookie=cookie)
    def get_Info(self, name:str):
        """获取用户输入的微博名，搜索相关人物供选择
        Args:
            name (str): 用户名
        Returns:
            uid: 用户uid
        """
        obj = self.spider.get(f"https://s.weibo.com/user?q={name}")
        content = obj.html.find('div#pl_user_feedList', first=True)
        content_list = content.text.replace('\n',' ').split('关注')
        content_list.pop(-1)
        print('[+]为您筛选%d个结果'%(len(content_list)))
        i = 1
        for e in content_list:
            print(str(i) + '.' + e)
            i += 1
        input_num = eval(input("[+]请输入序号:"))
        print("[+]您已选择%d号"%input_num)
        b_s = content.find('button')
        uid = b_s[input_num-1].attrs['uid']
        return uid
        
    def show_Info(self, uid:str):
        """根据uid获取人物详细信息
        Args:
            uid (str): 用户uid
        """
        genderlist = {'m':'男', 'f':'女'}
        url = f"https://weibo.com/ajax/profile/info?uid={uid}"
        d_url = f"https://weibo.com/ajax/profile/detail?uid={uid}"
        obj_dict = self.spider.get_json(url)
        d_obj_dict = self.spider.get_json(d_url)
        screen_name = obj_dict['data']['user']['screen_name']
        gender = obj_dict['data']['user']['gender']
        weihao = obj_dict['data']['user']['weihao']
        verified_reason = obj_dict['data']['user']['verified_reason']
        dscp = obj_dict['data']['user']['description']
        loc = obj_dict['data']['user']['location']
        statuses_count = obj_dict['data']['user']['statuses_count']
        followers_count = obj_dict['data']['user']['followers_count']
        friends_count = obj_dict['data']['user']['friends_count']
        birthday = d_obj_dict['data']['birthday']
        created_time = d_obj_dict['data']['created_at']
        print("用户名:%s" % screen_name)
        print("性别:%s" % genderlist[gender])
        print("生日:%s" % birthday)
        print("地址:%s" % loc)
        print("职业:%s" % verified_reason)
        print("简介:%s" % dscp)
        print("粉丝数:%s" % followers_count)
        print("关注数:%s" % friends_count)
        print("微号:%s" % weihao)
        print("微博数量:%s" % statuses_count)
        print("创建时间:%s" % created_time)

    def get_Friends(self, uid:str):
        """获取关注者信息, 包括用户名、所在地、链接、关注和粉丝数、微博数
        Args:
            uid (str): _description_
        """
        url = f"https://weibo.com/ajax/friendships/friends?page=1&uid={uid}"
        # with open('friends.json', 'w+', encoding='utf-8') as f:
        #     json.dump(json.loads(res.text),f)
        #     f.close()   
        json_dict = self.spider.get_json(url)
        i = 1
        for info_dict in json_dict['users']:
            if i>10:break
            print('*'*50 + str(i) + '*'*50)
            print("昵称:%s" % info_dict['name'])
            print("所在地:%s" % info_dict['location'])
            print("链接:%s" % ("https://weibo.com/"+info_dict['profile_url']))
            print("关注人数:%s" % info_dict['followers_count'])
            print("粉丝数:%s" % info_dict['friends_count'])
            print("微博数:%s" % info_dict['statuses_count'])
            i += 1
        
    def get_Followers(self, uid:str):
        """获取粉丝信息, 包括用户名、所在地、链接、关注和粉丝数、微博数
        Args:
            uid (str): _description_
        """
        url = f"https://weibo.com/ajax/friendships/friends?relate=fans&page=1&uid={uid}&type=all&newFollowerCount=0"
        res = self.spider.get(url)
        # with open('followers.json', 'w+', encoding='utf-8') as f:
        #     json.dump(json.loads(res.text),f)
        #     f.close()
        json_dict = self.spider.get_json(url)
        i = 1
        for info_dict in json_dict['users']:
            if i>10:break
            print('*'*50 + str(i) + '*'*50)
            print("昵称:%s" % info_dict['name'])
            print("所在地:%s" % info_dict['location'])
            print("链接:%s" % ("https://weibo.com/"+info_dict['profile_url']))
            print("关注人数:%s" % info_dict['followers_count'])
            print("粉丝数:%s" % info_dict['friends_count'])
            print("微博数:%s" % info_dict['statuses_count'])
            i += 1

    def get_Statuses(self, uid:str):
        """
        所有发帖和转发贴(如果发帖和转发贴的总量超过10,则只采集前10条),每个帖子的信息包括发帖时间、
        发帖内容、转发次数、评论次数、点赞次数、是否是转发
        Args:
            uid (str): 用户uid
        """
        url = f"https://weibo.com/ajax/statuses/mymblog?uid={uid}&page=1&feature=0"
        res = self.spider.get(url)
        # with open('statuses.json', 'w+', encoding='utf-8') as f:
        #     json.dump(json.loads(res.text),f)
        #     f.close() 
        json_dict = self.spider.get_json(url)
        i = 1
        for info_dict in json_dict['data']['list']:
            if i>10:break
            print('*'*50 + str(i) + '*'*50)
            retweeted_status = False
            if 'retweeted_status' in info_dict:
                retweeted_status = True               
            print("发帖时间:%s" % info_dict['created_at'])
            print("发帖内容:%s" % info_dict['text_raw'])
            print("转发数:%s" % info_dict['reposts_count'])
            print("评论数:%s" % info_dict['comments_count'])
            print("点赞数:%s" % info_dict['attitudes_count'])
            print("是否为转发:%s" % retweeted_status)
            if retweeted_status:
                print("转发内容:%s" % info_dict['retweeted_status']['text_raw'])
            i += 1
        return json_dict
    def get_Comments(self, num:str, uid:str, dic:dict):
        """按照热度排序的前10条评论
        (评论人ID、评论人昵称、评论时间、评论内容、点赞次数)

        Args:
            num (str): 动态序号
        """
        sid = dic['data']['list'][int(num)-1]['id']
        print("发帖内容:%s" % dic['data']['list'][int(num)-1]['text_raw'])
        url = f"https://weibo.com/ajax/statuses/buildComments?is_reload=1&id={sid}&is_show_bulletin=2&is_mix=0&count=10&uid={uid}"
        # with open('comments.json', 'w+', encoding='utf-8') as f:
        #     json.dump(json.loads(res.text),f)
        #     f.close() 
        json_dict = self.spider.get_json(url)
        i = 1
        for info_dict in json_dict['data']:
            if i>10:break
            print('*'*50 + str(i) + '*'*50)            
            print("昵称:%s" % info_dict['user']['name'])
            print("ID:%s" % info_dict['user']['id'])
            print("评论时间:%s" % info_dict['created_at'])
            print("评论内容:%s" % info_dict['text'])
            print("点赞数:%s" % info_dict['like_counts'])
            i += 1            
if __name__ == "__main__":
    with open('cookies.json','r') as f:
        cookie = json.load(f)
    info = Info(cookie=cookie)

import json

from time import sleep
from utils import Spider
from concurrent.futures import ThreadPoolExecutor, as_completed

class Info(object):
    def __init__(self, cookie):
        self.spider = Spider(Cookie=cookie)
        
    def cookie_validate(self):
        url = "https://weibo.com"
        res = self.spider.get(url)
        if res.status_code == "302":
            return 0
        else:
            return 1
        
    def get_Info(self, name:str):
        """获取用户输入的微博名，搜索相关人物供选择
        
        Args:
            name (str): 用户名
        Returns:
            uid: 用户uid
        """
        count = 0
        while True:
            if count > 5:
                return 0 # cookie失效
            obj = self.spider.get(f"https://s.weibo.com/user?q={name}")
            input_num = 1 # 默认为搜索的第一个结果
            e = obj.html.xpath(f'//*[@id="pl_user_feedList"]/div[{input_num}]/div[2]/div/a',first=True)
            count += 1
            if e!= None:
                break
        json_dict = self.spider.get_json(f"https://weibo.com/ajax/profile/info?screen_name={e.text}")
        uid = json_dict['data']['user']['idstr']
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
        verified_reason = " "
        if obj_dict['data']['user']['verified_type'] == 0:
            verified_reason = obj_dict['data']['user']['verified_reason']
        dscp = obj_dict['data']['user']['description']
        loc = obj_dict['data']['user']['location']
        statuses_count = obj_dict['data']['user']['statuses_count']
        followers_count = obj_dict['data']['user']['followers_count_str']
        friends_count = obj_dict['data']['user']['friends_count']
        birthday = d_obj_dict['data']['birthday']
        created_time = d_obj_dict['data']['created_at']
        avatar = obj_dict['data']['user']['avatar_hd']
        t1 = [screen_name,genderlist[gender],weihao,verified_reason,dscp,loc,statuses_count,
            followers_count,friends_count,birthday,created_time,avatar]
        t2 = ['usname','gender','id','des','pro','address','counts',
              'fans','friends','birth','time','avatar_url']
        dic = dict(zip(t2,t1))
        return dic

    def get_Friends(self, uid:str):
        """获取关注者信息, 包括用户名、所在地、链接、关注和粉丝数、微博数
        
        Args:
            uid (str): _description_
        """
        url = f"https://weibo.com/ajax/friendships/friends?page=1&uid={uid}"
        return self.spider.get_json(url)
        
    def get_Followers(self, uid:str):
        """获取粉丝信息, 包括用户名、所在地、链接、关注和粉丝数、微博数
        
        Args:
            uid (str): _description_
        """
        url = f"https://weibo.com/ajax/friendships/friends?relate=fans&page=1&uid={uid}&type=all&newFollowerCount=0"
        return self.spider.get_json(url)

    def get_Statuses(self, uid:str):
        """
        所有发帖和转发贴(如果发帖和转发贴的总量超过10,则只采集前10条),每个帖子的信息包括发帖时间、
        发帖内容、转发次数、评论次数、点赞次数、是否是转发
        
        Args:
            uid (str): 用户uid
        """
        url = f"https://weibo.com/ajax/statuses/mymblog?uid={uid}&page=1&feature=0"
        return self.spider.get_json(url)
    
    def get_Comments(self, uid:str, dic:dict):
        """按照热度排序的前10条评论
        (评论人ID、评论人昵称、评论时间、评论内容、点赞次数)
        
        Args:
            num (str): 动态序号
        """
        Comments_dict = []
        for i in range(0,10):
            comments_dict = []
            comment_dict = {}
            sid = dic['data']['list'][i]['id']
            url = f"https://weibo.com/ajax/statuses/buildComments?is_reload=1&id={sid}&is_show_bulletin=2&is_mix=0&count=10&uid={uid}"
            json_dict = self.spider.get_json(url)
            j = 1
            for info_dict in json_dict['data']:
                if j>10:break
                name = info_dict['user']['name']
                uid = info_dict['user']['id']
                time = info_dict['created_at']
                text = info_dict['text']
                likes = info_dict['like_counts']
                comment_dict = {"name":name, "id":uid, "time":time, "text":text, "likes":likes}
                comments_dict.append(comment_dict)
                j += 1
            Comments_dict.append(comments_dict)
        return Comments_dict
            
    def get_AllComments(self, uid:str):
        """获取所有动态及其评论

        Args:
            uid (str): 用户uid
        """
        url = f"https://weibo.com/ajax/statuses/mymblog?uid={uid}&page=1&feature=0"
        json_dict = self.spider.get_json(url)
        i = 1
        with ThreadPoolExecutor(max_workers = 10) as pool: # with创建线程池会阻塞到所有线程任务完成
            futures = []
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
                futures.append(pool.submit(self.get_Comments, i, uid, json_dict))       
                i += 1 
            as_completed(futures)

    def check(self, uid:str, dicts:dict):
        """实时监控动态的更新变化

        Args:
            uid (str): 用户uid
            dicts(dict): 原始动态
        """
        print("[+]正在监控目标...")
        url = f"https://weibo.com/ajax/statuses/mymblog?uid={uid}&page=1&feature=0"
        json_dict = dicts
        # 更新id值
        if("isTop" in json_dict["data"]["list"][0]): # 置顶动态更新后不变
            id = json_dict["data"]["list"][1]['id']
        else:
            id = json_dict["data"]["list"][0]['id'] # 获取原来第一条动态id值
        json_dict = self.spider.get_json(url)
        if (id != json_dict["data"]["list"][0]['id']):
            print("[+]目标动态已更新, 请及时查看")
            return json_dict
        else:
            print("[+]目标动态尚未更新, 请稍后...")
            return -1              
                    
             
if __name__ == "__main__":
    with open('cookies.json','r') as f:
        cookie = json.load(f)
    uid = "7383498934"
    info = Info(cookie=cookie)
    info.start_surpervise(uid)

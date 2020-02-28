import json
from scrapy import Request, Spider
from web.items import *
import time

class ZhihuSpider(Spider):
    name = 'zhihuSpider'

    allowed_domains = ['zhihu.com']
    
    # # 用户链接
    # user_url = 'https://m.weibo.cn/api/container/getIndex?uid={uid}&type=uid&value={uid}&containerid=100505{uid}'
    # # 关注者链接
    # follow_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_{uid}&luicode=10000011&lfid=100505{uid}&page={page}'
    # # 粉丝链接
    # fan_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_{uid}&luicode=10000011&lfid=100505{uid}&page={page}'
    # # 微博链接
    # weibo_url = 'https://m.weibo.cn/api/container/getIndex?uid={uid}&type=uid&page={page}&containerid=107603{uid}'
    
    # 用户链接
    user_url = """https://www.zhihu.com/api/v4/members/{user}?include=locations,employments,gender,educations,business,voteup_count,thanked_Count,follower_count,
    following_count,cover_url,following_topic_count,following_question_count,following_favlists_count,following_columns_count,
    answer_count,articles_count,pins_count,question_count,commercial_question_count,favorite_count,favorited_count,logs_count,
    marked_answers_count,marked_answers_text,message_thread_token,account_status,is_active,is_force_renamed,is_bind_sina,
    sina_weibo_url,sina_weibo_name,show_sina_weibo,is_blocking,is_blocked,is_following,is_followed,mutual_followees_count,
    vote_to_count,vote_from_count,thank_to_count,thank_from_count,thanked_count,description,hosted_live_count,participated_live_count,
    allow_message,industry_category,org_name,org_homepage,badge[?(type=best_answerer)].topics"""

    # 问答链接 offset的值是20的倍数
    answer_url ='https://www.zhihu.com/api/v4/members/{user}/answers?include=data%5B*%5D.is_normal%2Cexcerpt%2Ccomment_count%2Cvoteup_count&offset={offset}&limit=20&sort_by=created'

    # 关注链接
    follow_url ='https://www.zhihu.com/api/v4/members/{user}/followees?include=data&offset={offset}&limit=20'

    # 粉丝链接
    fan_url = 'https://www.zhihu.com/api/v4/members/{user}/followers?include=data&offset={offset}&limit=20'

    start_users = ['evanyou']
    # 尤雨溪知乎

    def start_requests(self):
        for user in self.start_users:
            yield Request(self.user_url.format(user=user), callback=self.parse_user)
    
    def parse_user(self,response):

        self.logger.debug(response)
        result = json.loads(response.text)
        
        if result:
            user_info = result
            user_item = UserItem()
            field_map = {
                'user': 'url_token', 'name': 'name', 'headline': 'headline', 'description': 'description',
                'gender': 'gender', 'follower_count': 'follower_count', 'following_count': 'following_count',
                'answer_count': 'answer_count', 'question_count': 'question_count', 'voteup_count': 'voteup_count',
                'thanked_count': 'thanked_count', 'business': 'business'
            }
            for field, attr in field_map.items():
                user_item[field] = user_info.get(attr)
            yield user_item

            # 关注
            user = user_info.get('url_token')
            yield Request(self.follow_url.format(user=user, offset=0), callback=self.parse_follows,
                          meta={'offset': 0, 'user': user})
            # 粉丝
            yield Request(self.fan_url.format(user=user, offset=0), callback=self.parse_fans,
                          meta={'offset': 0, 'user': user})
            # 微博
            yield Request(self.answer_url.format(user=user, offset=0), callback=self.parse_answers,
                          meta={'offset': 0, 'user': user})
        # time.sleep(2)

    def parse_follows(self,response):

        result = json.loads(response.text)
        if result.get('data'):
            # 解析用户
            follows = result.get('data')
            for follow in follows:
                if follow.get('url_token'):
                    user = follow.get('url_token')
                    yield Request(self.user_url.format(user=user), callback=self.parse_user)
            
            user = response.meta.get('user')
            # 关注列表
            user_relation_item = UserRelationItem()
            follows = [{'id': follow.get('id'), 'name': follow.get('name'),'headline':follow.get('headline')} for follow in
                       follows]
            user_relation_item['id'] = user
            user_relation_item['follows'] = follows
            user_relation_item['fans'] = []
            yield user_relation_item
            # 下一页关注
            offset = response.meta.get('offset') + 20
            yield Request(self.follow_url.format(user=user, offset=offset),
                          callback=self.parse_follows, meta={'offset': offset, 'user': user})
    
    def parse_fans(self, response):
        """
        解析用户粉丝
        :param response: Response对象
        """
        result = json.loads(response.text)
        if result.get('data'):
            # 解析用户
            fans = result.get('data')
            for fan in fans:
                if fan.get('url_token'):
                    user = fan.get('url_token')
                    yield Request(self.user_url.format(user=user), callback=self.parse_user)
            
            user = response.meta.get('user')
            # 粉丝列表
            user_relation_item = UserRelationItem()
            fans = [{'id': fan.get('id'), 'name': fan.get('name'),'headline':fan.get('headline')} for fan in
                       fans]
            user_relation_item['id'] = user
            user_relation_item['fans'] = fans
            user_relation_item['follows'] = []
            yield user_relation_item
            # 下一页粉丝
            offset = response.meta.get('offset') + 20
            yield Request(self.fan_url.format(user=user, offset=offset),
                          callback=self.parse_fans, meta={'offset': offset, 'user': user})
    


    def parse_answers(self, response):
        """
        解析回答列表
        :param response: Response对象
        """
        result = json.loads(response.text)
        if result.get('data'):
            datas = result.get('data')
            for data in datas:
                question = data.get('question')
                if question:
                    answer_item = AnswerItem()
                    question_map ={
                        'question_type':'question_type','question_url':'url','question_title':'title',
                        'question_id':'id','question_created':'created','question_updated':'updated_time'
                    }
                    for field, attr in question_map.items():
                        answer_item[field] = question.get(attr)

                    answer_map = {
                        'answer_text':'excerpt','voteup_count':'voteup_count','comment_count':'comment_count',
                        'is_copyable':'is_copyable','answer_created':'created_time','answer_update':'updated_time'
                    }
                    for field, attr in answer_map.items():
                        answer_item[field] = question.get(attr)

                    answer_item['user'] = response.meta.get('user')
                    yield answer_item
            # 下一页微博
            user = response.meta.get('user')
            offset = response.meta.get('offset') + 20
            yield Request(self.answer_url.format(user=user, offset=offset), callback=self.parse_answers,
                          meta={'user': user, 'offset': offset})

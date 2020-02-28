import json
from scrapy import Request, Spider
from web.items import *

class ZhihuSpider(Spider):
    name = 'zhihuSpider'

    allowed_domains = ['zhihu.com']
    
    # 用户链接
    user_url = 'https://m.weibo.cn/api/container/getIndex?uid={uid}&type=uid&value={uid}&containerid=100505{uid}'
    # 关注者链接
    follow_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_{uid}&luicode=10000011&lfid=100505{uid}&page={page}'
    # 粉丝链接
    fan_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_{uid}&luicode=10000011&lfid=100505{uid}&page={page}'
    # 微博链接
    weibo_url = 'https://m.weibo.cn/api/container/getIndex?uid={uid}&type=uid&page={page}&containerid=107603{uid}'
    
    # 问答链接 page的值是20的倍数
    answer_url ='https://www.zhihu.com/api/v4/members/{user}/answers?include=data&offset={page}&limit=20&sort_by=created'

    # 关注链接
    follow_url ='https://www.zhihu.com/api/v4/members/{user}/followees?include=data&offset={page}&limit=20'

    # 粉丝链接
    fan_url = 'https://www.zhihu.com/api/v4/members/{user}/followers?include=data&offset={page}&limit=20'

    start_users = ['5796662600']
    # 吴宣仪微博

    def start_requests(self):
        for uid in self.start_users:
            yield Request(self.user_url.format(uid=uid), callback=self.parse_user)
    
    def parse_user(self,response):

        # self.logger.debug(response)
        result = json.loads(response.text)
        
        if result.get('data').get('userInfo'):
            user_info = result.get('data').get('userInfo')
            user_item = UserItem()
            field_map = {
                'id': 'id', 'name': 'screen_name', 'avatar': 'profile_image_url', 'cover': 'cover_image_phone',
                'gender': 'gender', 'description': 'description', 'fans_count': 'followers_count',
                'follows_count': 'follow_count', 'weibos_count': 'statuses_count', 'verified': 'verified',
                'verified_reason': 'verified_reason', 'verified_type': 'verified_type'
            }
            for field, attr in field_map.items():
                user_item[field] = user_info.get(attr)
            yield user_item

            # 关注
            uid = user_info.get('id')
            yield Request(self.follow_url.format(uid=uid, page=1), callback=self.parse_follows,
                          meta={'page': 1, 'uid': uid})
            # 粉丝
            yield Request(self.fan_url.format(uid=uid, page=1), callback=self.parse_fans,
                          meta={'page': 1, 'uid': uid})
            # 微博
            yield Request(self.weibo_url.format(uid=uid, page=1), callback=self.parse_weibos,
                          meta={'page': 1, 'uid': uid})


    def parse_follows(self,response):

        result = json.loads(response.text)
        if result.get('ok') and result.get('data').get('cards') and len(result.get('data').get('cards')) and result.get('data').get('cards')[-1].get(
            'card_group'):
            # 解析用户
            follows = result.get('data').get('cards')[-1].get('card_group')
            # get('cards')[-1]是因为微博可能会有类似 共同关注 这样的卡片，得选择最后一个才是全部关注
            for follow in follows:
                if follow.get('user'):
                    uid = follow.get('user').get('id')
                    yield Request(self.user_url.format(uid=uid), callback=self.parse_user)
            
            uid = response.meta.get('uid')
            # 关注列表
            user_relation_item = UserRelationItem()
            follows = [{'id': follow.get('user').get('id'), 'name': follow.get('user').get('screen_name')} for follow in
                       follows]
            user_relation_item['id'] = uid
            user_relation_item['follows'] = follows
            user_relation_item['fans'] = []
            yield user_relation_item
            # 下一页关注
            page = response.meta.get('page') + 1
            yield Request(self.follow_url.format(uid=uid, page=page),
                          callback=self.parse_follows, meta={'page': page, 'uid': uid})
    
    def parse_fans(self, response):
        """
        解析用户粉丝
        :param response: Response对象
        """
        result = json.loads(response.text)
        if result.get('ok') and result.get('data').get('cards') and len(result.get('data').get('cards')) and result.get('data').get('cards')[-1].get(
            'card_group'):
            # 解析用户
            fans = result.get('data').get('cards')[-1].get('card_group')
            for fan in fans:
                if fan.get('user'):
                    uid = fan.get('user').get('id')
                    yield Request(self.user_url.format(uid=uid), callback=self.parse_user)
            
            uid = response.meta.get('uid')
            # 粉丝列表
            user_relation_item = UserRelationItem()
            fans = [{'id': fan.get('user').get('id'), 'name': fan.get('user').get('screen_name')} for fan in
                    fans]
            user_relation_item['id'] = uid
            user_relation_item['fans'] = fans
            user_relation_item['follows'] = []
            yield user_relation_item
            # 下一页粉丝
            page = response.meta.get('page') + 1
            yield Request(self.fan_url.format(uid=uid, page=page),
                          callback=self.parse_fans, meta={'page': page, 'uid': uid})
    
    def parse_weibos(self, response):
        """
        解析微博列表
        :param response: Response对象
        """
        result = json.loads(response.text)
        if result.get('ok') and result.get('data').get('cards'):
            weibos = result.get('data').get('cards')
            for weibo in weibos:
                mblog = weibo.get('mblog')
                if mblog:
                    weibo_item = WeiboItem()
                    field_map = {
                        'id': 'id', 'attitudes_count': 'attitudes_count', 'comments_count': 'comments_count',
                        'reposts_count': 'reposts_count', 'picture': 'original_pic', 'pictures': 'pics',
                        'created_at': 'created_at', 'source': 'source', 'text': 'text', 'raw_text': 'raw_text',
                        'thumbnail': 'thumbnail_pic',
                    }
                    for field, attr in field_map.items():
                        weibo_item[field] = mblog.get(attr)
                    weibo_item['user'] = response.meta.get('uid')
                    yield weibo_item
            # 下一页微博
            uid = response.meta.get('uid')
            page = response.meta.get('page') + 1
            yield Request(self.weibo_url.format(uid=uid, page=page), callback=self.parse_weibos,
                          meta={'uid': uid, 'page': page})
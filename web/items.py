# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    collection = 'users' # 数据库collection名称

    id = scrapy.Field() # 用户ID

    user = scrapy.Field() # 用户URL_TOKEN
    name = scrapy.Field() # 用户名字
    headline = scrapy.Field() # 用户标题
    description = scrapy.Field() # 用户描述
    gender = scrapy.Field() # 用户性别
    follower_count = scrapy.Field() # 用户追随者数量
    following_count = scrapy.Field() # 用户关注数量
    answer_count = scrapy.Field() # 用户回答数量
    question_count = scrapy.Field() # 用户提问数量
    voteup_count = scrapy.Field() # 用户收到的总赞数
    thanked_count = scrapy.Field() # 用户收到的感谢数
    business = scrapy.Field() # 用户领域
    
    crawled_at = scrapy.Field() # 爬取时间

    
class UserRelationItem(scrapy.Item):
    collection = 'users' # 数据库collection名称
    
    id = scrapy.Field() # 用户ID
    follows = scrapy.Field() # 数组，用户的关注者
    fans = scrapy.Field() # 数组，用户的粉丝

class AnswerItem(scrapy.Item):
    collection = 'answers'# 数据库collection名称
    
    id = scrapy.Field()# 用户ID
    user = scrapy.Field()# URL_TOKEN

    question_type = scrapy.Field()# 问题类型
    question_url = scrapy.Field() # 问题链接
    question_title = scrapy.Field()# 问题标题
    question_created = scrapy.Field()# 问题创建时间
    question_updated = scrapy.Field()# 问题更新时间
    question_id = scrapy.Field()# 问题ID

    answer_text = scrapy.Field()# 回答文本
    voteup_count = scrapy.Field()# 回答点赞数
    comment_count = scrapy.Field()# 回答评论数
    is_copyable = scrapy.Field()# 回答可复制
    answer_created = scrapy.Field()# 回答创建时间
    answer_updated = scrapy.Field()# 回答更新时间

    crawled_at = scrapy.Field()# 爬取时间


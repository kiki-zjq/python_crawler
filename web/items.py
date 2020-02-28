# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    collection = 'users'

    id = scrapy.Field()

    user = scrapy.Field()
    name = scrapy.Field()
    headline = scrapy.Field()
    description = scrapy.Field()
    gender = scrapy.Field()
    follower_count = scrapy.Field()
    following_count = scrapy.Field()
    answer_count = scrapy.Field()
    question_count = scrapy.Field()
    voteup_count = scrapy.Field()
    thanked_count = scrapy.Field()
    business = scrapy.Field()
    
    crawled_at = scrapy.Field()

    
class UserRelationItem(scrapy.Item):
    collection = 'users'
    
    id = scrapy.Field()
    follows = scrapy.Field()
    fans = scrapy.Field()


class WeiboItem(scrapy.Item):
    collection = 'weibos'
    
    id = scrapy.Field()
    attitudes_count = scrapy.Field()
    comments_count = scrapy.Field()
    reposts_count = scrapy.Field()
    picture = scrapy.Field()
    pictures = scrapy.Field()
    source = scrapy.Field()
    text = scrapy.Field()
    raw_text = scrapy.Field()
    thumbnail = scrapy.Field()
    user = scrapy.Field()
    created_at = scrapy.Field()
    crawled_at = scrapy.Field()


class AnswerItem(scrapy.Item):
    collection = 'answers'
    
    user = scrapy.Field()

    question_type = scrapy.Field()
    question_url = scrapy.Field()
    question_title = scrapy.Field()
    question_created = scrapy.Field()
    question_updated = scrapy.Field()
    question_id = scrapy.Field()

    answer_text = scrapy.Field()
    voteup_count = scrapy.Field()
    comment_count = scrapy.Field()
    is_copyable = scrapy.Field()
    answer_created = scrapy.Field()
    answer_update = scrapy.Field()

    crawled_at = scrapy.Field()


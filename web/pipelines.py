# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import logging
import pymongo
import re, time
from web.items import *

class WebPipeline(object):

    def parse_time(self, date):
        dateArray = time.localtime(date)
        formalTime = time.strftime("%Y-%m-%d %H:%M:%S",dateArray)
        return formalTime
    
    def process_item(self, item, spider):
        if isinstance(item, AnswerItem):
            if item.get('question_created'):
                item['question_created'] = self.parse_time(item.get('question_created'))
            if item.get('question_updated'):
                item['question_updated'] = self.parse_time(item.get('question_updated'))
            if item.get('answer_created'):
                item['answer_created'] = self.parse_time(item.get('answer_created'))
            if item.get('answer_updated'):
                item['answer_updated'] = self.parse_time(item.get('answer_updated'))

            
        return item


class TimePipeline():
    def process_item(self, item, spider):
        if isinstance(item, UserItem) or isinstance(item, AnswerItem):
            now = time.strftime('%Y-%m-%d %H:%M', time.localtime())
            item['crawled_at'] = now
        return item


class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )
    
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.db[UserItem.collection].create_index([('id', pymongo.ASCENDING)])
        self.db[AnswerItem.collection].create_index([('id', pymongo.ASCENDING)])
    
    def close_spider(self, spider):
        self.client.close()
    
    def process_item(self, item, spider):
        if isinstance(item, UserItem) or isinstance(item, AnswerItem):
            self.db[item.collection].update({'id': item.get('id')}, {'$set': item}, True)
        if isinstance(item, UserRelationItem):
            self.db[item.collection].update(
                {'id': item.get('id')},
                {'$addToSet':
                    {
                        'follows': {'$each': item['follows']},
                        'fans': {'$each': item['fans']}
                    }
                }, True)
        return item

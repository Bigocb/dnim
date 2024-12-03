from pymongo import MongoClient
from dataclasses import dataclass


try:
    client = MongoClient("localhost", 27017)
    db = client.dnim
    topics = db.topics
except:
    raise Exception("DB Cannot be reached")


@dataclass
class Page:
    topic: str
    body: str
    ts: int
    tags: list


class Database:


    def insert_topic(self, topic: Page):
        id = topics.insert_one({
            "topic":f"{topic.topic}",
            "body":f"{topic.body}",
            "tags":f"{topic.tags}",
            "ts" : f"{topic.ts}"
            }).inserted_id
        return topics.find_one({"topic": topic.topic})



    def get_page(self, topic):
        sea = topics.find({'topic' : topic}).sort({'_id':-1})
        return sea[0]
    
    def get_page_version(self, topic, version):
        # lookup from mongodb by _id
        sea = topics.find_one({'topic' : topic, '_id': version})
        return sea

    def get_versions(seld, topic):
        sea = topics.find({'topic' : topic}).sort({'_id':-1}).limit(5)
        return sea
    
    def get_last_n_topics(self, n: int):
        """Get the last n documents with the 'topic' key."""
        return list(topics.find({'topic': {'$exists': True}}).sort('_id', -1).limit(n))

    def get_pages(self,val = None):
        if val:
            res = topics.find({"topic":{"$regex": f"{val}"}})
        else:
            res = topics.find({})
        res_list = []
        for i,v in enumerate(res):
            t = v['topic']
            if v['topic'] not in res_list:
                res_list.append(v['topic'])
            
        return res_list
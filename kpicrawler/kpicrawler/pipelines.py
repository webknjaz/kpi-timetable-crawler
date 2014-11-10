# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy_mongodb import MongoDBPipeline

class KpicrawlerPipeline(object):
    def process_item(self, item, spider):
        return item

class PerSpiderMongoDBPipeline(MongoDBPipeline):
    collections = {}

    def __init__(self, crawler):
        MongoDBPipeline.__init__(self, crawler)

        for k in crawler.settings['MONGODB_COLLECTIONS_POSTFIX']:
            self.collections[k] = self.settings['MONGODB_COLLECTION'] + '_' + crawler.settings['MONGODB_COLLECTIONS_POSTFIX'][k]
        #crawler.settings['MONGODB_COLLECTIONS_POSTFIX'] += '_' + crawler.settings['MONGODB_COLLECTIONS_POSTFIX']
        print(self.collections)

# Scrapy settings for kpicrawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'kpicrawler'

SPIDER_MODULES = ['kpicrawler.spiders']
NEWSPIDER_MODULE = 'kpicrawler.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'kpicrawler (+http://www.yourdomain.com)'

MONGODB_URI = 'mongodb://localhost:27017'
MONGODB_DATABASE = 'scrapy'
MONGODB_COLLECTION = 'KPItimetable'
MONGODB_UNIQUE_KEY = 'id'
MONGODB_ADD_TIMESTAMP = True

MONGODB_COLLECTIONS_POSTFIX = {
        'GROUPS': 'Groups',
        'LECTORS': 'Lectors',
        'TIMETABLES': 'Timetables'
        }

ITEM_PIPELINES = {
        'kpicrawler.pipelines.PerSpiderMongoDBPipeline': 100,
        }

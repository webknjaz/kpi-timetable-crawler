# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class KpiScheduleItemBase(Item):
    id = Field()
    odd = Field()
    even = Field()
    pass

class KpiAutosuggestItemBase(Item):
    # define the fields for your item here like:
    id = Field()
    name = Field()
    pass


class KpiGroupItem(KpiAutosuggestItemBase):
    # define the fields for your item here like:
    full_name = Field()
    pass

class KpiGroupscheduleItem(KpiScheduleItemBase):
    # define the fields for your item here like:
    pass


class KpiTeacherItem(KpiAutosuggestItemBase):
    # define the fields for your item here like:
    surname = Field()
    midint = Field()
    pass

class KpiTeacherscheduleItem(KpiScheduleItemBase):
    # define the fields for your item here like:
    pass

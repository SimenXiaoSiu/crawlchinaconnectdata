# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PostscrapeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class StockItem(scrapy.Item):
    date = scrapy.Field()
    market = scrapy.Field()
    stockcode = scrapy.Field()
    stockname = scrapy.Field()
    shareholding = scrapy.Field()
    shareholdingpercent = scrapy.Field()
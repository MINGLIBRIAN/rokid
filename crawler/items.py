# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlerItem(scrapy.Item):
    id = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    stock = scrapy.Field()
    img = scrapy.Field()

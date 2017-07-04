# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class QchuiProduct(scrapy.Item):
    entity_id = scrapy.Field(serializer=int)
    href = scrapy.Field(serializer=str)
    name = scrapy.Field(serializer=str)
    current_price = scrapy.Field(serializer=float)
    desc = scrapy.Field()

    image_urls = scrapy.Field()
    images = scrapy.Field()

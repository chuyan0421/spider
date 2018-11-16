# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GujingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    sku = scrapy.Field()
    slogan = scrapy.Field()
    url = scrapy.Field()
    images_urls = scrapy.Field()
    images_urls_local = scrapy.Field()
    name = scrapy.Field()
    odor_type = scrapy.Field()
    volume = scrapy.Field()
    net_weight = scrapy.Field()
    general_agency = scrapy.Field()
    package = scrapy.Field()
    price = scrapy.Field()

# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BjjItem(scrapy.Item):
    # Define the fields for your item here like:
    id = scrapy.Field()
    first_name = scrapy.Field()
    last_name = scrapy.Field()
    nickname = scrapy.Field()
    team = scrapy.Field()
    wins = scrapy.Field()
    wins_by_sub = scrapy.Field()
    losses = scrapy.Field()
    losses_by_sub = scrapy.Field()
    history = scrapy.Field()

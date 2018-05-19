# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ShanbayItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    user_name = scrapy.Field()
    listen_num = scrapy.Field()
    reading_num = scrapy.Field()
    word_num = scrapy.Field()
    sentence_num = scrapy.Field()
    course_num = scrapy.Field()
    training_num = scrapy.Field()
    study_time = scrapy.Field()
    speaking_num = scrapy.Field()
    voc_all = scrapy.Field()
# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Scrapyfor104Item(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    salary = scrapy.Field()
    job_category = scrapy.Field()
    update_time = scrapy.Field()
    exp = scrapy.Field()
    address = scrapy.Field()
    edu = scrapy.Field()
    company = scrapy.Field()

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Scrapyfor104Item(scrapy.Item):
    # for job
    job_title = scrapy.Field()  # ok
    company = scrapy.Field()  # ok
    salary = scrapy.Field()  # ok
    address = scrapy.Field()  # ok
    industry = scrapy.Field()
    update_time = scrapy.Field()  # ok

    # for education
    edu = scrapy.Field()  # ok

    # for experience
    exp = scrapy.Field()  # ok

    # for skill
    skill = scrapy.Field()  # ok

    # for category
    category_name = scrapy.Field()  # ok

    # for tool
    specialty_tool = scrapy.Field()  # ok

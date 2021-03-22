# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    date_of_publication = scrapy.Field()
    headline = scrapy.Field()
    main_text = scrapy.Field()
    reports = scrapy.Field()

class ReportItem(scrapy.Item):
    diseases = scrapy.Field()
    syndromes = scrapy.Field()
    event_date = scrapy.Field()
    locations = scrapy.Field()

class LocationItem(scrapy.Item):
    country = scrapy.Field()
    location = scrapy.Field()

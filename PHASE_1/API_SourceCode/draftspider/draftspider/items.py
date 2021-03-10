# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DraftspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    date_of_publication = scrapy.Field()
    headline = scrapy.Field()
    main_text = scrapy.Field()
    report = scrapy.Field()

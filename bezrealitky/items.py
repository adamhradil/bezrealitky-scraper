# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BezrealitkyItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    type = scrapy.Field()
    url = scrapy.Field()
    rent = scrapy.Field()
    service_fees = scrapy.Field()
    security_deposit = scrapy.Field()
    address = scrapy.Field()
    description = scrapy.Field()
    disposition = scrapy.Field()
    available_from = scrapy.Field()
    floor = scrapy.Field()
    area = scrapy.Field()
    furnished = scrapy.Field()
    status = scrapy.Field()
    ownership = scrapy.Field()
    penb = scrapy.Field()
    design = scrapy.Field()
    balcony = scrapy.Field()
    cellar = scrapy.Field()
    garden = scrapy.Field()
    terrace = scrapy.Field()
    elevator = scrapy.Field()
    parking = scrapy.Field()
    garage = scrapy.Field()
    # pets = scrapy.Field()
    loggie = scrapy.Field()
    # public_transport = scrapy.Field()
    gps_lat = scrapy.Field()
    gps_lon = scrapy.Field()

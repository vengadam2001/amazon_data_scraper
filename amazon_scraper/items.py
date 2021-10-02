# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from io import BufferedRandom
import scrapy


class AmazonScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name            = scrapy.field()
    mrp             = scrapy.field()
    save            = scrapy.field()
    price           = scrapy.field()
    about           = scrapy.field()
    no_of_rating    = scrapy.field()
    avg_rating      = scrapy.field()
    total_no_answer = scrapy.field()
    delivery_type   = scrapy.field()
    delivery_date   = scrapy.field()
    Model	        = scrapy.field()
    Brand	        = scrapy.field()
    SpecificUses    = scrapy.field()
    ScreenSize      = scrapy.field()
    OS              = scrapy.field()
    more_detail     = scrapy.field()
    order_within    = scrapy.field()
    emi             = scrapy.field()
    exchange        = scrapy.field()
    five_star       = scrapy.field()
    four_star       = scrapy.field()
    three_star      = scrapy.field()
    two_star        = scrapy.field()
    one_star        = scrapy.field()
    reviews         = scrapy.field()    

    

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AirbnbScrapyItem_LV(scrapy.Item):
    # define the fields for your item here like:
    stay_name = scrapy.Field()
    stay_image_url = scrapy.Field()
    stay_url = scrapy.Field()
    stay_type = scrapy.Field()
    stay_number_of_beds = scrapy.Field()
    stay_price = scrapy.Field()
    stay_name = scrapy.Field()
    stay_name = scrapy.Field()
    stay_rating_and_totalreviews = scrapy.Field()
    pass

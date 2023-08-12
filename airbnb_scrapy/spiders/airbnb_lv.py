import scrapy
from selenium.webdriver.common.by import By
import pymongo
from ..items import AirbnbScrapyItem_LV
import random
import time

DRIVER_FILE_PATH = "/Users/qunishdash/Documents/chromedriver_mac64/chromedriver"
USER_AGENT_LIST = ['Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
                    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:72.0) Gecko/20100101 Firefox/72.0',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
                    ]


class AirbnbLvSpider(scrapy.Spider):
    name = "airbnb_lv"
    handle_httpstatus_list = [403]
    page_number = 1
    start_urls = [
        "https://www.airbnb.co.in/s/Hulimavu--Bengaluru--Karnataka--India/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2023-09-01&monthly_length=3&price_filter_input_type=0&price_filter_num_nights=5&channel=EXPLORE&query=Hulimavu%2C%20Bengaluru%2C%20Karnataka&place_id=ChIJlWpoKNRqrjsRnkhk-wJHg58&date_picker_type=calendar&source=structured_search_input_header&search_type=autocomplete_click"
    ]

    # def __init__(self):
    #     self.conn = pymongo.MongoClient(
    #         "localhost",
    #         27017
    #     )
    #     db = self.conn["airbnb_scrapy_db"]
    #     self.collection = db["hulimavu_lv"]

    def get_chrome_driver(self, headless_flag):
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        if headless_flag:
            # in case you want headless browser
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--start-maximized")
            # chrome_options.add_experimental_option('prefs', {'headers': headers}) # if you want to add custom header
            chrome_options.add_argument("user-agent={}".format(random.choice(USER_AGENT_LIST)))
            driver = webdriver.Chrome(options=chrome_options) 
        else:
            # in case  you want to open browser
            chrome_options = Options()
            # chrome_options.add_experimental_option('prefs', {'headers': headers}) # if you want to add custom header
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("user-agent={}".format(random.choice(USER_AGENT_LIST)))
            chrome_options.headless = False
            driver = webdriver.Chrome(options=chrome_options)

        return driver

    def parse(self, response):
        if response.status == 403:
            self.logger.warning("Status 403 - but chill we are handling using selenium driver.")

        driver = self.get_chrome_driver(headless_flag=False)
        driver.get(response.url)
        time.sleep(5)
        
        items = AirbnbScrapyItem_LV()

        # Extract data using Selenium and yield items
        all_cards = driver.find_elements(By.XPATH, "/html/body/div[5]/div/div/div[1]/div/div[3]/div[2]/main/div[2]/div/div[2]/div/div/div/div/div[1]/div/div/div[2]/div/div/div/div[1]/div")

        for card in all_cards:
            time.sleep(5)
            try:
                stay_name = card.find_element(By.XPATH, "/html/body/div[5]/div/div/div[1]/div/div[3]/div[2]/main/div[2]/div/div[2]/div/div/div/div/div[1]/div/div/div[2]/div/div/div/div[1]/div/div[2]/div[2]").text
            except Exception as e:
                stay_name = ''
                print("EXCEPTION", e)
            try:
                stay_image_url = card.find_element(By.XPATH, "/html/body/div[5]/div/div/div[1]/div/div[3]/div[2]/main/div[2]/div/div[2]/div/div/div/div/div[1]/div/div/div[2]/div/div/div/div[1]/div/div[1]/div/div/div[2]/div/div/div/div/a[1]/div/div/picture/img").get_attribute("src")
            except Exception as e:
                stay_image_url = ''
            try:
                stay_url = card.find_element(By.XPATH, "/html/body/div[5]/div/div/div[1]/div/div[3]/div[2]/main/div[2]/div/div[2]/div/div/div/div/div[1]/div/div/div[2]/div/div/div/div[1]/div/div[1]/div/div/div[2]/div/div/div/div/a[2]").get_attribute("href")
            except Exception as e:
                stay_url = ''
            try:
                stay_type = card.find_element(By.XPATH, "/html/body/div[5]/div/div/div[1]/div/div[3]/div[2]/main/div[2]/div/div[2]/div/div/div/div/div[1]/div/div/div[2]/div/div/div/div[1]/div/div[2]/div[1]").text
            except Exception as e:
                stay_type = ''
            try:
                stay_number_of_beds = card.find_element(By.XPATH, "/html/body/div[5]/div/div/div[1]/div/div[3]/div[2]/main/div[2]/div/div[2]/div/div/div/div/div[1]/div/div/div[2]/div/div/div/div[1]/div/div[2]/div[3]").text
            except Exception as e:
                stay_number_of_beds = ''
            try:
                stay_price = card.find_element(By.XPATH, "/html/body/div[5]/div/div/div[1]/div/div[3]/div[2]/main/div[2]/div/div[2]/div/div/div/div/div[1]/div/div/div[2]/div/div/div/div[1]/div/div[2]/div[5]/div/div/span/span").text
            except Exception as e:
                stay_price = ''
            try:
                stay_rating_and_totalreviews = card.find_element(By.XPATH, "/html/body/div[5]/div/div/div[1]/div/div[3]/div[2]/main/div[2]/div/div[2]/div/div/div/div/div[1]/div/div/div[2]/div/div/div/div[1]/div/div[2]/span/span[2]").text
            except Exception as e:
                stay_rating_and_totalreviews = ''

            items["stay_name"] = stay_name
            items["stay_image_url"] = stay_image_url
            items["stay_url"] = stay_url
            items["stay_type"] = stay_type
            items["stay_number_of_beds"] = stay_number_of_beds
            items["stay_price"] = stay_price
            items["stay_rating_and_totalreviews"] = stay_rating_and_totalreviews

            # if any(items.values()):
            #     self.collection.insert_one(dict(items))

            yield items

        next_page = response.xpath("/html/body/div[5]/div/div/div[1]/div/div[3]/div[2]/main/div[2]/div/div[3]/div/div/div/nav/div/a[6]/@href").get()
        if next_page is not None:
            yield response.follow(next_page, callback = self.parse)

        driver.quit()


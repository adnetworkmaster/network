import scrapy
from ajar.items import AmazonUs
from scrapy.spiders import CrawlSpider, Rule
from selenium import webdriver
from time import sleep
from scrapy.selector import Selector
import json
import os
from scrapy.linkextractors import LinkExtractor as sle
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# chrome requirments
GOOGLE_CHROME_PATH = "/app/.apt/usr/bin/google-chrome"
CHROMEDRIVER_PATH = "/app/.chromedriver/bin/chromedriver"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.binary_location = GOOGLE_CHROME_PATH


class QuotesInfiniteScrollSpider(CrawlSpider):
    name = "bhphotovideo"
    rotate_user_agent = True
    allowed_domains = ["www.bhphotovideo.com"]
    start_urls = ["https://www.bhphotovideo.com/"]
    rules = (
        Rule(
            sle(
                allow="/c/product/",
                deny=("/find/", "/browse/", "/buy/", "/bnh/", "/explora/"),
            ),
            callback="parse_result",
            follow=True,
        ),
    )
    # parsing results with below function
    def parse_result(self, response):
        amazon = []
        amazon = AmazonUs()
        print(response.url)
        browser = webdriver.Chrome(
            executable_path=os.environ.get("CHROMEDRIVER_PATH"),
            chrome_options=chrome_options,
        )
        browser.get(response.url)
        sleep(0.5)
        scrapy_selector = Selector(text=browser.page_source)
        # css selection of html data tags
        product_id = scrapy_selector.css(
            'head > link[rel="canonical"]::attr(href)'
        ).get()
        product_mrp = (
            scrapy_selector.css(
                "del[data-selenium='strikeThroughPrice']::text"
            ).getall()
            # or response.css(
            #     "#productRecap > div.Gm > aside > div.Jm > div > div > span.fo > span.io > span::text"
            # ).getall()
            # or scrapy_selector.css("div._3auQ3N._1POkHg::text").getall()
        )
        product_description = (
            scrapy_selector.css(
                "div[data-selenium='sellingPointsOverviewDescription']::text"
            ).getall()
            # or scrapy_selector.css("div._3la3Fn._1zZOAc > p::text").getall()
            # or scrapy_selector.css("div._3la3Fn::text").getall()
        )
        product_name = (
            scrapy_selector.css("h1[data-selenium='productTitle']::text").getall()
            # or scrapy_selector.css("div._3aS5mM > p::text").getall()
            # or scrapy_selector.css("span._35KyD6::text").getall()
        )
        product_ASIN = scrapy_selector.css(
            'head > link[rel="canonical"]::attr(href)'
        ).get()
        product_by_url = "bhphotovideo.com"
        product_by_name = "bhphotovideo"
        product_rating = (
            scrapy_selector.css("span[data-selenium='reviewsNumber']::text").getall()
            or "NULL"
        )
        product_image = (
            # scrapy_selector.css(
            #     "#container > div > div.t-0M7P._3GgMx1._2doH3V > div._3e7xtJ > div._1HmYoV.hCUpcT > div._1HmYoV._35HD7C.col-5-12._3KsTU0 > div > div > div._2uAjEK > div._2rDnao > div._1ov7-N > div._3BTv9X._3iN4zu > img::attr(src)"
            # ).get()
            scrapy_selector.css(
                "img[data-selenium='inlineMediaMainImage']::attr(src)"
            ).get()
            or scrapy_selector.css(
                "head > meta[property='og:image']::attr(content)"
            ).get()
        )
        product_price = (
            scrapy_selector.css("div[data-selenium='pricingPrice']::text").get()
            # or response.css(
            #     "#productRecap > div.Gm > aside > div.Jm > div > div > span.go.ho::text"
            # ).get()
            # or response.css(
            #     "#productRecap > div.Gm > aside > div.Jm > div > div > span::text"
            # ).getall()
            # or scrapy_selector.css("div._1vC4OE._3qQ9m1::text").getall()
        )
        product_about = (
            scrapy_selector.css(
                "li[data-selenium='sellingPointsListItem']::text"
            ).getall()
            # or scrapy_selector.css("div._3WHvuP > ul > li._2-riNZ::text").getall()
        )
        product_keywords = scrapy_selector.css(
            "div[data-selenium='overviewLongDescription'] > div > p::text"
        ).getall()
        product_catlog = (
            scrapy_selector.css("a[data-selenium='linkCrumb']::text").getall()
            # or scrapy_selector.css("a._1KHd47::text").getall()
        )
        product_price_2 = (
            # scrapy_selector.css(
            #     "#container > div > div.t-0M7P._3GgMx1._2doH3V > div._3e7xtJ > div._1HmYoV.hCUpcT > div._1HmYoV._35HD7C.col-8-12 > div > div > div._3iZgFn > div._2i1QSc > div > div.VGWI6T._1iCvwn > span::text"
            # ).getall()
            scrapy_selector.css(
                "span[data-selenium='defaultSavingLabel'] > span::text"
            ).getall()
        )

        product_keywords_2 = (
            scrapy_selector.css(
                "head > meta[name='description']::attr(content)"
            ).getall()
            # or response.css(
            #     "#itemInformation > div > div > div > ul > li > ul > li::text"
            # ).getall()
            # or scrapy_selector.css("div._1aK10F > p::text").getall()
        )
        # master push

        # append data to items
        amazon["product_id"] = product_id
        amazon["product_mrp"] = product_mrp
        amazon["product_description"] = product_description
        amazon["product_name"] = product_name
        amazon["product_ASIN"] = product_ASIN
        amazon["product_by_url"] = product_by_url
        amazon["product_by_name"] = product_by_name
        amazon["product_rating"] = product_rating
        amazon["product_image"] = product_image
        amazon["product_price"] = product_price
        amazon["product_about"] = product_about
        amazon["product_keywords"] = product_keywords
        amazon["product_catlog"] = product_catlog
        amazon["product_price_2"] = product_price_2
        amazon["product_keywords_2"] = product_keywords_2
        browser.quit()
        return amazon


# git push change usage comments
# push 1
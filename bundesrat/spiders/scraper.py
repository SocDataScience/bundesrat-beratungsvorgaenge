# This script runs on Python 3!

# ***************************************** #
# Useful inspiration and docs for Selenium crawler:
# https://github.com/voliveirajr/seleniumcrawler/blob/master/seleniumcrawler/spiders/seleniumcrawler_spider.py
# http://stackoverflow.com/questions/17975471/selenium-with-scrapy-for-dynamic-page
# https://seleniumhq.github.io/selenium/docs/api/py/api.html

# ***************************************** #
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from bundesrat.items import MeetingsItem

from selenium import webdriver
# See the official documentation for selenium at
# http://selenium-python.readthedocs.io/getting-started.html
from selenium.webdriver.common.keys import Keys

import time

# ***************************************** #
class BundesratSpider(CrawlSpider):

    name = "BundesratSpider"
    allowed_domains = ["bundesrat.de"]

    rules = (
        # Sites which should be saved
        Rule(LinkExtractor(
            restrict_xpaths=("//div[@class='pagination-index']/ul/li[class='next']/a",),
            unique=True),
            callback='parse_start_url',  # this function is defined below. It needs to be defined below.
            follow=True),)

    # Define the years for which you want to have the data:
    # 2014 to 2016. (can be extended to greater time periods by
    # changing start and end year).
    startyear = 2014
    endyear = 2016
    years = list(range(startyear, endyear + 1))

    # Define the websites that should be scraped (starturls):
    start_urls = ["http://www.bundesrat.de/DE/dokumente/beratungsvorgaenge/" + \
                  str(year) + "/beratungsvorgaenge-node.html" for year in years]

    start_urls = ["http://www.bundesrat.de/DE/dokumente/beratungsvorgaenge/2015/beratungsvorgaenge-node.html"]


# ***************************************** #
    def __init__(self):
        self.driver = webdriver.Firefox()

    def parse(self, response):
        self.driver.get(response.url)

        print(response.url)
        time.sleep(2)

        # # Start with just one website for developing the script:
        # # driver.get("http://www.bundesrat.de/DE/dokumente/beratungsvorgaenge/2015/beratungsvorgaenge-node.html") # for development
        #
        #
        # tops = self.driver.find_elements_by_xpath("//li[contains(@class, 'top-item type-')]")
        #
        # # top = tops[2] # for development
        # # top = driver.find_element_by_xpath("//li[contains(@id, 'top-644/15')]") # for development
        # # top = driver.find_element_by_xpath("//li[contains(@id, 'top-643/15')]") # for development
        # # top = driver.find_element_by_xpath("//li[contains(@id, 'top-640/15')]") # for development
        #
        #
        # for top in tops:
        #     item = MeetingsItem()
        #     top_nr = (top.find_element_by_xpath(".//h2[@class='top-number']")).text
        #     print(top_nr)
        #     item['id'] = top_nr
        #
        #     details = top.find_element_by_xpath(".//div[@class='top-item-switcher']/a")
        #
        #     details.send_keys("\n")
        #     #  this works for 644/15, 643/15, 640/15
        #     # see http://stackoverflow.com/questions/8832858/using-python-bindings-selenium-webdriver-click-is-not-working-sometimes
        #
        #     time.sleep(2)  # I need to wait until the new content has appeared!!!
        #
        #
        #     date = (top.find_elements_by_xpath(".//div[@class='zusatztitel']/following-sibling::p"))[0].text
        #     item['date'] = date
        #
        #     year = date.split(".")[-1]
        #     item['year'] = year
        #
        #
        #     # If there are details on the committees involved, get those details:
        #     try:
        #         committees = (top.find_element_by_xpath(".//h3[contains(text(), 'Ausschusszuweisung')]/following-sibling::p")).text
        #
        #         item['committees'] = committees
        #
        #         fdf = committees.split(" - ")
        #         fdf = str([i for i in fdf if "fdf" in i][0])
        #         fdf = fdf.replace(" (fdf)", "")
        #         item['fdf'] = fdf
        #
        #         com_list = committees.replace(" (fdf)", "").split(" - ")
        #
        #         # add a function for coding "(fdf)" ("federführend") later!!
        #
        #         com_list2 = ['AV', 'AIS', 'AA', 'EU', 'Fz', 'FJ', 'G', 'In',
        #                       'K', 'R', 'Wo', 'U', 'Vk', 'V', 'Wi', 'other']
        #
        #         for com in com_list2:
        #             print(com)
        #             item[com] = (1 if com in com_list else 0)
        #
        #
        #     except: # if no details on the "Ausschusszuweisung" given:
        #         pass
        #
        #
        #
        #     print(item)
        #     yield item
        #


        # Close the driver:
        self.driver.close()



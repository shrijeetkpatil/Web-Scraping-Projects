import scrapy

from selenium import webdriver
from scrapy.http import HtmlResponse
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import logging
from selenium.webdriver.remote.remote_connection import LOGGER

import json
import os

class JustDialSpider(scrapy.Spider):

    name = "justdial"

    def start_requests(self):

        urls = [
            'http://www.justdial.com/Delhi/Estate-Agents-For-Residential-Rental/nct-10192844/page-1',
            'http://www.justdial.com/Delhi/Estate-Agents-For-Residential-Rental/nct-10192844/page-2',            
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)



    def parse(self, response):

        json_data = self.scrap_from_lazy_loader(response.url)
        
        directory = 'SCRAPED_DATA/'+self.name+'/'
        if not os.path.exists(directory):
            os.makedirs(directory)

        page = response.url.split("/")[-1]
        filename = directory+'justdial-%s.json' % page

        with open(filename, 'w') as f:
            f.write(json_data)
            
        self.log('Saved file %s' % filename)



    icon_dict = {
        'icon-acb': '0',
        'icon-yz': '1',
        'icon-wx': '2',
        'icon-vu': '3',
        'icon-ts': '4',
        'icon-rq': '5',
        'icon-po': '6',
        'icon-nm': '7',
        'icon-lk': '8',
        'icon-ji': '9',
        'icon-ba': '-',
        'icon-dc': '+',
        'icon-fe': '(',
        'icon-hg': ')',
    }

    def scrap_from_lazy_loader(self, url):

        LOGGER.setLevel(logging.WARNING)
        
        self.driver = webdriver.Firefox()
        self.driver.get(url)
        
        items = self.driver.find_elements_by_class_name("cntanr")
        
        while len(items) < 101:
            try:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                WebDriverWait(self.driver, 20).until(
                    lambda driver: self.new_data(driver, len(items)))
                items = self.driver.find_elements_by_class_name("cntanr")
                
            except TimeoutException:
                break

        # body = self.driver.page_source  # Source Code Of HTML Page
        # all_items = self.driver.find_elements_by_xpath('//div[@class=" col-sm-5 col-xs-8 store-details sp-detail paddingR0"]')  # All Items

        name = self.driver.find_elements_by_xpath('//span[@class="lng_cont_name"]')

        raiting = self.driver.find_elements_by_xpath('//span[@class="green-box"]')

        contact_items = self.driver.find_elements_by_xpath('//div[@class=" col-sm-5 col-xs-8 store-details sp-detail paddingR0"]//p[@class="contact-info "]')

        address = self.driver.find_elements_by_xpath('//span[@class="adWidth cont_sw_addr"]') #find_elements_by_class_name("cont_fl_addr")

        # print('info===',name[0].text, "==", raiting[0].text, "==", address[0].text)
        # print(len(name), len(raiting), len(contact_items), len(address))

        multikeys = []
        for i in range(len(name)):

            c_no_body = contact_items[i].get_attribute('innerHTML')

            icons = [word.split('"')[0] for word in c_no_body.split() if word.startswith('icon')]

            c_no = [self.icon_dict.get(x,"") for x in icons[6:]]

            contact_no = ''
            for c in c_no:
                contact_no = contact_no + c

            record = {
                "name" : name[i].text,
                "rateing" : float(raiting[i].text),
                "phone" : contact_no,
                "address": address[i].text.replace('|','')
            }

            multikeys.append(record)

        self.driver.close()

        return json.dumps(multikeys, indent = 4)

        # response = HtmlResponse(self.driver.current_url, body=body, encoding='utf-8')



    def new_data(self, driver, min_len):
        return len(driver.find_elements_by_class_name("cntanr")) > min_len



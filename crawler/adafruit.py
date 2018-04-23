# -*- coding: utf-8 -*-
import logging
import requests
import scrapy

from .items import CrawlerItem


class AdafruitSpider(scrapy.Spider):
    name = 'adafruit'
    start_urls = []

    def __init__(self, initialization=False):
        super().__init__()
        self.initialization = initialization

        # Get the pages of products list
        r = requests.get('https://www.adafruit.com/api/category_tree.json')
        base_url = 'https://www.adafruit.com/category/'
        categories = r.json()
        self.start_urls = [base_url + c['id'] for c in categories]

    def parse(self, response):
        product_list_xpath = '//*[@id="productListing"]/div[@class="row product-listing"]'
        product_list = response.xpath(product_list_xpath)
        # print('The number of products in this page:', len(product_list))
        for product in product_list:
            item = self.parse_item(product)
            if item:
                yield item

    def parse_item(self, product):
        try:
            item = CrawlerItem()

            # Parse all the information
            # ID
            id = product.css("h1 a::attr(data-pid)").extract()[0]
            item['id'] = id

            # URL
            base_url = 'https://www.adafruit.com/'
            url = product.css("h1 a::attr(href)").extract()[0]
            url = base_url + url
            item['url'] = url

            # Product name
            name = product.css("h1 a::text").extract()[0]
            name = name.replace('\n', '', 1)
            name = name.replace("'", "''")
            item['name'] = name

            # Price
            price = product.css("span.red-sale-price::text").extract()
            if not price:
                price = product.css("span.normal-price span::text").extract()
                # If no price information
                if not price:
                    price = '-1'
                else:
                    price = price[0]
            else:
                # Trim dollar sign
                price = price[0][1:]
            price = float(price.replace(',', ''))
            item['price'] = price

            # Stock information
            stock = product.css(".stock span::text").extract()
            # If no stock information
            if not stock:
                stock = -1
            else:
                stock = stock[0]
                if stock == 'IN STOCK':
                    stock = 101
                elif stock == 'OUT OF STOCK':
                    stock = 0
                else:
                    stock_data = stock.split(" IN STOCK")
                    # Store the real quantity of stock
                    if len(stock_data) > 1:
                        stock = int(stock_data[0])
                    # For DISCONTINUED
                    else:
                        stock = 102
            item['stock'] = stock

            # Product image
            img = product.css("img::attr(src)").extract()[0]
            item['img'] = img
            return item
        except IndexError:
            logging.error("Crawler Parsing Error")
            return

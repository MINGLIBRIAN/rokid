# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymysql
import logging
import redis


class CrawlerPipeline(object):
    def __init__(self):
        self.redis_db = redis.Redis()
        self.connection = pymysql.connect(host='localhost',
                                          user='root',
                                          password='10',
                                          charset='utf8mb4')
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS rokid")
        self.cursor.execute("USE rokid")

    def open_spider(self, spider):
        # print("Crawler init:", spider.settings['IS_INITIALIZE'])
        if spider.settings['IS_INITIALIZE']:
            self.cursor.execute("DROP TABLE products")
            self.cursor.execute("CREATE TABLE IF NOT EXISTS products ({})".format(",".join([
                "id CHAR(100) NOT NULL",
                "url CHAR(100)",
                "name CHAR(100)",
                "price FLOAT",
                "stock INT",
                "img CHAR(100)",
                "PRIMARY KEY (id)"
            ])))

    def process_item(self, item, spider):
        '''
        :param item: The item return by spider
        :param spider: The spider object
        :return: Pass item to the pipeline
        '''
        if item['id'] in self.redis_db:
            # If initialization, this item is just repeated
            if spider.settings['IS_INITIALIZE']:
                # print('Duplicated item!')
                return
            num = int(self.redis_db.get(item['id']).decode('utf-8'))
            # Only update if stock information is changed
            if num == item['stock']:
                # print('Unchanged item!')
                return
        self.redis_db.set(item['id'], item['stock'])

        try:
            new_row = [item['id'], item['url'], item['name'], item['price'], item['stock'], item['img']]
            new_row = list(map(lambda x: "'" + str(x) + "'", new_row))

            # Only insert when initialization, otherwise update the records
            if spider.settings['IS_INITIALIZE']:
                new_row = ",".join(new_row)
                self.cursor.execute("INSERT IGNORE INTO products VALUES ({})".format(new_row))
            else:
                new_row = "url={}, name={}, price={}, stock={}, img={}".format(*new_row[1:])
                self.cursor.execute("UPDATE products SET {} WHERE id={}".format(new_row, item['id']))
            self.connection.commit()
        except pymysql.Error as e:
            logging.error("Database Access Error:", e.args[0], e.args[1])
        return item

    def close_spider(self, spider):
        self.connection.close()

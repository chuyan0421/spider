# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql as pq

class TianmaoMysqlPipeline(object):
    def open_spider(self,spider):
        self.conn = pq.connect(host='192.168.33.55', user='root', passwd='', db='ir', charset='utf8')
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        name = item['name']
        brands = item['brands']
        address = item['address']
        products = item['products']
        service = item['service']
        logistic = item['logistic']

        sql = "insert into tianmao(name,brands,address,products,service,logistic) VALUES (%s,%s,%s,%s,%s,%s)"
        self.cur.execute(sql, (name, brands, address, products, service, logistic))
        self.conn.commit()

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()


class TianmaoPipeline(object):
    def process_item(self, item, spider):
        return item

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.utils.project import get_project_settings
from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request
from scrapy.exceptions import DropItem
import os
import pymysql as pq
import shutil

class WinePipeline(object):
    def open_spider(self, spider):
        settings = get_project_settings()
        storage = settings.get('IMAGES_STORE')
        try:
            os.mkdir(storage+'/'+spider.name)
        except:
            print('folder exists')

class GujingImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        image_url = item['images_urls']
        yield Request(image_url)

    def file_path(self, request, response=None, info=None):
        url = request.url
        imageName = url.split('/')[-1]
        return '%s' % (imageName)

    def item_completed(self, results, item, info):
        # image_path = [x['path'] for ok, x in results if ok]
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem('Item contains no images')

        settings = get_project_settings()
        storage = settings.get('IMAGES_STORE')
        subdir = storage+'/gujing/'+item['sku']

        new_paths = []
        # shutil.rmtree(subdir)

        try:
            os.mkdir(subdir)
        except IOError:
            print('folder exists')

        for x in image_paths:
            shutil.move(storage + '/' + x, subdir + '/' + x)

        # new_paths.append('/usr/local/webserver/nginx/html/pics/'+item['sku']+'/'+x)

        # item['images_urls_local'] = new_paths
        return item

class GujingMysqlPipeline(object):
    def open_spider(self,spider):
        self.conn = pq.connect(host='192.168.33.55', user='root', passwd='', db='ir', charset='utf8')
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        sku = item['sku']
        url = item['url']
        images_urls = item['images_urls']
        images_urls_local = item['images_urls_local']
        slogan = item['slogan']
        name = item['name']
        odor_type = item['odor_type']
        volume = item['volume']
        net_weight = item['net_weight']
        general_agency = item['general_agency']
        package = item['package']
        price = item['price']

        sql = "insert into products(sku,url,images_urls,images_urls_local,slogan,name,odor_type,volume,net_weight,general_agency,package,price) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        self.cur.execute(sql, (sku, url, images_urls, images_urls_local, slogan, name, odor_type, volume, net_weight, general_agency, package, price))
        self.conn.commit()

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()

class GujingPipeline(object):
    def process_item(self, item, spider):
        return item

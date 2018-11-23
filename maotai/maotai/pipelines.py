# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.http import Request
from scrapy.utils.project import get_project_settings
import os
from scrapy.exporters import JsonLinesItemExporter
from scrapy.exporters import CsvItemExporter
import shutil
import re
from urllib import request
import time
import pymysql as pq

class WinePipeline(object):
    def open_spider(self, spider):
        settings = get_project_settings()
        storage = settings.get('IMAGES_STORE')
        dirName = spider.name
        os.mkdir(storage+'/'+dirName)

class MaotaiImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['images_urls']:
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
        subdir = storage+'/emaotai/'+item['sku']

        new_paths = []
        # shutil.rmtree(subdir)
        os.mkdir(subdir)
        for x in image_paths:
            os.rename(storage +'/'+ x, subdir+'/1.jpg')
            # new_paths.append('/usr/local/webserver/nginx/html/pics/'+item['sku']+'/'+x)

        # item['images_urls_local'] = new_paths
        return item

class MaotaiJsonPipeline(object):
    def open_spider(self,spider):
        settings = get_project_settings()
        storage = settings.get('IMAGES_STORE')
        self.file = open(storage+'/maotaiInfo.json', 'wb')
        self.exporter = JsonLinesItemExporter(self.file, encoding='utf-8')
        self.exporter.start_exporting()

    def close_spider(self,spider):
        self.exporter.finish_exporting()
        self.file.close()
        settings = get_project_settings()
        storage = settings.get('IMAGES_STORE')
        fileTime = time.strftime('%Y%m%d%H%M%S',time.localtime())
        os.rename(storage + '/maotaiInfo.json', storage+'/maotai/maotaiInfo'+fileTime+'.json')

    def process_item(self,item,spider):
        self.exporter.export_item(item)
        return item

class MaotaiCsvPipeline(object):
    def open_spider(self,spider):
        settings = get_project_settings()
        storage = settings.get('IMAGES_STORE')
        self.file = open(storage+'/maotaiInfo.csv', 'wb')
        self.exporter = CsvItemExporter(self.file, encoding='utf-8')
        self.exporter.start_exporting()

    def close_spider(self,spider):
        self.exporter.finish_exporting()
        self.file.close()
        settings = get_project_settings()
        storage = settings.get('IMAGES_STORE')
        fileTime = time.strftime('%Y%m%d%H%M%S',time.localtime())
        os.rename(storage + '/maotaiInfo.csv', storage+'/maotai/maotaiInfo'+fileTime+'.csv')

    def process_item(self,item,spider):
        self.exporter.export_item(item)
        return item

class MaotaiMysqlPipeline(object):
    def open_spider(self,spider):
        self.conn = pq.connect(host='localhost', user='', passwd='', db='ir', charset='utf8')
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        sku = item['sku']
        url = item['url']
        images_urls = ','.join(item['images_urls'])  ###convert list to string
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



class ZhangyuImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
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
        subdir = storage+'/zhangyu/'+item['sub_dir']

        new_paths = []
        # shutil.rmtree(subdir)
        os.mkdir(subdir)
        for x in image_paths:
            os.rename(storage +'/'+ x, subdir+'/'+x)
            new_paths.append(subdir + '/' + x)

        item['image_paths'] = new_paths
        return item

class ZhangyuJsonPipeline(object):
    def open_spider(self,spider):
        settings = get_project_settings()
        storage = settings.get('IMAGES_STORE')
        self.file = open(storage+'/zhangyuInfo.json', 'wb')
        self.exporter = JsonLinesItemExporter(self.file, encoding='utf-8')
        self.exporter.start_exporting()

    def close_spider(self,spider):
        self.exporter.finish_exporting()
        self.file.close()
        settings = get_project_settings()
        storage = settings.get('IMAGES_STORE')
        fileTime = time.strftime('%Y%m%d%H%M%S',time.localtime())
        os.rename(storage + '/zhangyuInfo.json', storage+'/zhangyu/zhangyuInfo'+fileTime+'.json')

    def process_item(self,item,spider):
        self.exporter.export_item(item)
        return item


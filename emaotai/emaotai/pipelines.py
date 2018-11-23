# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request
from scrapy.exceptions import DropItem
from scrapy.utils.project import get_project_settings
import os

class EmaotaiImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        yield Request(item['image_url'])

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
        subdir = storage+'/emaotai/'+item['name']

        new_paths = []
        # shutil.rmtree(subdir)
        os.mkdir(subdir)
        for x in image_paths:
            os.rename(storage +'/'+ x, subdir+'/1.jpg')
            # new_paths.append('/usr/local/webserver/nginx/html/pics/'+item['sku']+'/'+x)

        # item['images_urls_local'] = new_paths
        return item



class EmaotaiPipeline(object):
    def process_item(self, item, spider):
        return item

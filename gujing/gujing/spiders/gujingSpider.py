import scrapy
from urllib import request
from gujing.items import GujingItem
import re
import hashlib
from scrapy.utils.python import to_bytes


class GujingSpider(scrapy.Spider):

    custom_settings = {
        'ITEM_PIPELINES': {
            'gujing.pipelines.WinePipeline': 10,
            'gujing.pipelines.GujingImagesPipeline': 100,
            # 'maotai.pipelines.MaotaiCsvPipeline': 200,
            'gujing.pipelines.GujingMysqlPipeline': 300
        },
    }

    name = "gujing"

    def start_requests(self):
        urls = {
            # 年份原浆
            'http://www.gujing.com/product/index29.html',
            # 古井贡酒
            'http://www.gujing.com/product/index48.html',
            # 黄鹤楼
            'http://www.gujing.com/product/index56.html',
            # 古井系列
            'http://www.gujing.com/product/index52.html',
            # 37度
            'http://www.gujing.com/product/index141.html',
            # 运营商系列
            'http://www.gujing.com/product/index135.html'
        }
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        pagetitle=response.xpath('/html/head/title').extract_first()
        print("content parsing:", pagetitle)

        products = response.xpath('//*[@class="product_top"]')
        for product in products:
            if product is not None:
                page = product.xpath('./a/@href').extract_first()
                detailPage = request.urljoin(response.url, page)
                pictureUrl = product.xpath('./a/img/@src').extract_first()
                yield scrapy.Request(detailPage, callback=self.page_parse, meta={'pictureUrl': pictureUrl})

    def page_parse(self, response):
        pagetitle=response.xpath('/html/head/title').extract_first()
        print("detail parsing:", pagetitle)

        wineInfo = response.xpath('//div[@class="chanp1_rs"]')

        item = GujingItem()

        item['url'] = response.url
        item['slogan'] = ''  # slogon
        item['name'] = wineInfo.xpath('./h2/text()').extract_first() # 名称
        item['odor_type'] = wineInfo.xpath('./p[1]/em/text()').extract_first()  # 香型
        item['volume'] = wineInfo.xpath('./p[2]/em/text()').extract_first()  # 酒精度
        item['net_weight'] = wineInfo.xpath('./p[3]/em/text()').extract_first()  # 净含量
        item['general_agency'] = ''  # 总代理
        item['package'] = ''  # 包装
        item['price'] = ''  #价格


        item['sku'] = hashlib.sha1(to_bytes(item['name'])).hexdigest()
        item['images_urls_local'] = 'http://192.168.33.55/pics/' + item['sku'] + '/1.jpg'

        # pictureUrl = response.xpath('//div[@class="chanp1_lt"]/em/img/@src').extract_first()
        pictureUrl = response.meta['pictureUrl']
        item['images_urls'] = request.urljoin(response.url, pictureUrl)

        yield item

import scrapy
import re
import os
import hashlib
from scrapy.utils.python import to_bytes
from urllib import request
from emaotai.items import EmaotaiItem
from selenium import webdriver
from scrapy.http import HtmlResponse
import time
from scrapy.selector import Selector


class eMaotaiSpider(scrapy.Spider):
    custom_settings = {
        'ITEM_PIPELINES': {
            'emaotai.pipelines.EmaotaiImagesPipeline': 100,
        },
    }

    name = "emaotai"

    def start_requests(self):
        urls = {
            'https://www.emaotai.cn/smartsales-b2c-web-pc/proList?keyword=茅台',
            'https://www.emaotai.cn/smartsales-b2c-web-pc/proList?keyword=贵州大曲',
            'https://www.emaotai.cn/smartsales-b2c-web-pc/proList?keyword=习酒',
            'https://www.emaotai.cn/smartsales-b2c-web-pc/proList?keyword=赖茅',
            ##e茅台
        }
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'type': 'page'})

    # def parse(self, response):
    #     pages = response.xpath('//*[@class="cpzx-img tyyj-gy"]/a/@href').extract()
    #     # print('number of pages:', len(pages))
    #
    #     for page in pages:
    #         if page is not None:
    #             yield scrapy.Request(page, callback=self.page_parse)

    def parse(self, response):

        pagetitle = response.xpath('/html/head/title').extract_first()
        print("page title: ",pagetitle)
        #/html/body/div[4]/div[3]/div[1]/div[4]/ul/li[1]/div/a[1]/div

        html = ""
        driver = webdriver.Firefox(executable_path=r'C:\geckodriver.exe')
        driver.get(response.url)
        time.sleep(10)
        html = html + driver.page_source
        # print("访问" + request.url)
        for i in range(1, 4):
            next_page = driver.find_elements_by_xpath("//a[contains(.,'下一页')]")
            # 能找到元素，点击click，否则退出循环
            if len(next_page) > 0:
                next_page[0].click()
            else:
                break
            time.sleep(10)
            html = html + driver.page_source

        html_response = HtmlResponse(driver.current_url, body=html, encoding="utf-8", request=request)
        products = html_response.xpath('//*[@class="forjs_item"]/div')

        # name = response.xpath('//*[@class="forjs_item"]/div/a/div[@class="pro-name ellipsis "]/text()').extract()
        # price = response.xpath('//*[@class="forjs_item"]/div/a/span/text()').extract()

        fd = open('E:/wineSpider/maotaiprice.csv', 'a', encoding='utf-8')
        print(len(products))
        for product in products:
            item = EmaotaiItem()

            nameRaw = product.xpath('string(./a[1]/div[@class="pro-name ellipsis "])').extract_first()
            name = self.nameNormal(nameRaw)
            # sku = hashlib.sha1(to_bytes(name)).hexdigest()

            volume = re.search(r'..%vol', name).group()
            net_weight = name.split(' ')[-1]

            urlRaw = product.xpath('./a[1]/@href').extract_first()
            # url = request.urljoin(response.url, urlRaw)
            # print(url)
            skuRaw = re.search(r'skuId=.{19}',urlRaw).group()
            sku = re.sub(r'skuId=', '', skuRaw)
            item['name'] = sku

            image_url = product.xpath('./div[1]/div[1]/ul/li/@data-img').extract_first()
            item['image_url'] = image_url

            image_url_server = 'http://192.168.33.55/pics/' + sku + '/1.jpg'
            # print(skuId)

            price = product.xpath('./a[1]/span/text()').extract_first()

            odor_type = '酱香型'
            material = '"高粱，小麦，水"'
            manufacturer = '贵州茅台股份有限公司'

            fd.write(sku + ',' + image_url_server + ',' + name + ',' + odor_type + ',' + volume + ',' + net_weight + ',' + price + ',' + material + ',' + manufacturer + '\n')
            yield item

        # next_page = response.xpath("//a[contains(.,'下一页')]").extract()
        # # print('number of pages:', len(pages))
        #
        # if next_page is not None:
        #     yield scrapy.Request(next_page, callback=self.page_parse)

        fd.close()

    def nameNormal(self, string):
        # 【二维码】，【茅台商城】，【茅台商城预约专享】,【付款后30天内发货】
        name2 = re.sub(r'【.{3,10}】', '', string)
        # （商品编号：741）
        name3 = re.sub(r'（商品编号：.{1,3}）', '', name2)
        name4 = re.sub(r'53%vol500ml', '53%vol 500ml', name3)
        name5 = re.sub(r'53%vol50ml*4', '50ml*4', name4)
        name = re.sub(r'茅台商城', '', name5)

        return name







# //*[@id="app"]/div/div[3]/div/div[1]/div/div[1]/div/div[1]/div[2]/text()[1]

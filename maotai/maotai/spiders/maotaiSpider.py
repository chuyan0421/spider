import scrapy
import re
import hashlib
from urllib import request
from maotai.items import WineItem
from scrapy.utils.python import to_bytes

class MaotaiSpider(scrapy.Spider):

    custom_settings = {
        'ITEM_PIPELINES': {
            'maotai.pipelines.WinePipeline': 10,
            'maotai.pipelines.MaotaiImagesPipeline': 100,
            'maotai.pipelines.MaotaiCsvPipeline': 200,
            # 'maotai.pipelines.MaotaiMysqlPipeline': 300
        },
    }

    name = "maotai"

    def start_requests(self):
        urls = {
            'http://www.moutaichina.com/chanpin/index.html'
            # 'http://www.moutaichina.com/chanpin/qita/2017/213.html'
        }
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        pages = response.xpath('//*[@class="cpzx-img tyyj-gy"]/a/@href').extract()
        # print('number of pages:', len(pages))

        for page in pages:
            if page is not None:
                yield scrapy.Request(page, callback=self.page_parse)

        ##### crawl next page

        nextPage = response.xpath('//*[@id="pages"]/a/@href').extract()[-1]
        if nextPage is not None:
            nextUrl = request.urljoin(response.url, nextPage)
            # print('next page is:', nextUrl)
            yield scrapy.Request(url=nextUrl, callback=self.parse)


    def page_parse(self,response):
        # pagetitle=response.xpath('/html/head/title').extract_first()
        # print("detail parsing:", pagetitle)


        text1 = response.xpath('//*[@class="cp-js"]/p/text()').extract()
        # text2 = response.xpath('//*[@class="wz-box"]/div/p/text()').extract_first()
        item = WineItem()

        item['url'] = response.url
        item['slogan'] = re.sub(r'—*\s+', '', text1[0])  # slogon
        item['name'] = re.sub(r'：', '', text1[1])  # 名称
        item['odor_type'] = re.sub(r'：', '', text1[2])  # 香型
        item['volume'] = re.sub(r'：', '', text1[3])  # 酒精度
        item['net_weight'] = re.sub(r'：', '', text1[4])  # 净含量
        item['general_agency'] = re.sub(r'：', '', text1[5])  # 总代理
        item['package'] = re.sub(r'：', '', text1[6])  # 包装
        item['price'] = ''  # 详细说明

        item['sku'] = hashlib.sha1(to_bytes(item['name'])).hexdigest()
        item['images_urls_local'] = 'http://192.168.33.55/pics/' + item['sku'] + '/1.jpg'


        #总代理
        # print(re.sub(r'：+', '', text1[5]))

        # text2 = response.xpath('//*[@class="wz-box"]/div/p/text()').extract()
        # print(re.sub(r'\s+', '', text2))

        pictureUrls = response.xpath('//*[@class="items"]/ul/li/img/@bimg').extract()

        img_urls = []
        for picture in pictureUrls:
            pictureUrl = request.urljoin(response.url, picture)
            img_urls.append(pictureUrl)

        item['images_urls'] = img_urls


        yield item


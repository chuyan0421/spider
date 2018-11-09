import scrapy
from tianmao.items import TianmaoItem

class tianmaoSpider(scrapy.Spider):

    name = "tianmao"

    custom_settings = {
        'ITEM_PIPELINES': {
            'tianmao.pipelines.TianmaoMysqlPipeline': 300
        },
    }

    def start_requests(self):
        urls = {
            'https://www.tmall.com/'
        }
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        pagetitle = response.xpath('/html/head/title').extract_first()
        print("page title: ",pagetitle)

        # shopitems = response.xpath('//*[@class="shopHeader-info"]')
        shopitems = response.xpath('//*[@class="shopHeader"]')

        for shop in shopitems:
            # print(name)
            item = TianmaoItem()
            item['name'] = shop.xpath('string(./div[1]/a)').extract_first() ###店铺名称
            item['brands'] = shop.xpath('./div[1]/p[1]/span/text()').extract_first()  ###主营品牌
            item['address'] = shop.xpath('./div[1]/p[2]/text()').extract_first()  ###所在地
            item['products'] = shop.xpath('./div[2]/ul/li[1]/em[1]/text()').extract_first() ###产品评分
            item['service'] = shop.xpath('./div[2]/ul/li[2]/em[1]/text()').extract_first()  ###服务评分
            item['logistic'] = shop.xpath('./div[2]/ul/li[3]/em[1]/text()').extract_first()  ###物流评分
            print(item)

            yield item

            # print(shop.xpath('string(./div[1]/a)').extract_first())
            # print(shop.xpath('./div[1]/p[1]/span/text()').extract_first())
            # print(shop.xpath('./div[1]/p[2]/text()').extract_first())
            #
            # print(shop.xpath('./div[2]/ul/li[1]/em[1]/text()').extract_first())
            # print(shop.xpath('./div[2]/ul/li[2]/em[1]/text()').extract_first())
            # print(shop.xpath('./div[2]/ul/li[3]/em[1]/text()').extract_first())
            #
            #
            # print('----------分割线------------------')


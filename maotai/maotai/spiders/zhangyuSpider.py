import scrapy
from urllib import request
from maotai.items import WineItem
import hashlib
from scrapy.utils.python import to_bytes

class ZhangyuSpider(scrapy.Spider):
    name = "zhangyu"
    custom_settings = {
        'ITEM_PIPELINES': {
            'maotai.pipelines.WinePipeline': 11,
            'maotai.pipelines.ZhangyuImagesPipeline': 101,
            'maotai.pipelines.ZhangyuJsonPipeline': 201},
    }

    def start_requests(self):
        urls = {
            'http://www.changyu.com.cn/ptj/index.html'
            # 'http://www.changyu.com.cn/content/details153_2249.html'

        }
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        pages1 = response.xpath('//*[@class="ptj"]/ul/li/a/@href').extract()
        pages2 = response.xpath('//*[@class="ptj"]/ul/li/span/a/@href').extract()
        pages = pages1 + pages2
        print(len(pages))

        for page in pages:
            if page is not None:
                pageUrl = request.urljoin(response.url, page)
                yield scrapy.Request(pageUrl, callback=self.page_parse)

    def page_parse(self, response):
        # pagetitle=response.xpath('/html/head/title').extract_first()
        # print("detail parsing:", pagetitle)
        info = {}
        info['url'] = response.url
        info['名称'] = response.xpath('//*[@class="por_right"]/h2/text()').extract_first()
        # info['介绍'] = response.xpath('//*[@class="por_right"]/p/text()').extract()
        test1 = response.xpath('//*[@class = "art_txt"]/li[@class = "i2"]/text()').extract()
        if(len(test1)==2):
            info['葡萄品种'] = test1[0]
            info['酒精度'] = test1[1]
        else:
            info['葡萄品种'] = ''
            info['酒精度'] = test1[0]

        info['颜色'] = response.xpath('//*[@class = "art_txt"]/li[@class = "i3"]/text()').extract_first()
        info['香气'] = response.xpath('//*[@class = "art_txt"]/li[@class = "i4"]/text()').extract_first()
        info['口感'] = response.xpath('//*[@class = "art_txt"]/li[@class = "i5"]/text()').extract_first()
        info['适饮温度'] = response.xpath('//*[@class = "art_txt"]/li[@class = "i6"]/text()').extract_first()
        info['储存器'] = response.xpath('//*[@class = "art_txt"]/li[@class = "i7"]/text()').extract_first()

        print(info)

        item = WineItem()
        imageUrls = []
        pictureUrls = response.xpath('//*[@class="pro_img"]/ul[@class="img"]/li/img/@src').extract()
        for url in pictureUrls:
            imageUrls.append(request.urljoin(response.url,url))

        item['image_urls'] = imageUrls
        item['sub_dir'] = hashlib.sha1(to_bytes(info['名称'])).hexdigest()
        item['info'] = info
        yield item


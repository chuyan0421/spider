import scrapy


class eMaotaiSpider(scrapy.Spider):

    name = "emaotai"

    def start_requests(self):
        urls = {
            'https://www.emaotai.cn/smartsales-b2c-web-pc/proList?keyword=茅台' ##e茅台
            # 'http://www.moutaichina.com/chanpin/qita/2017/213.html'
        }
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        pagetitle = response.xpath('/html/head/title').extract_first()
        print("page title: ",pagetitle)
        #/html/body/div[4]/div[3]/div[1]/div[4]/ul/li[1]/div/a[1]/div
        name = response.xpath('//*[@class="forjs_item"]/div/a/div[@class="pro-name ellipsis "]').extract()
        price = response.xpath('//*[@class="forjs_item"]/div/a/span/text()').extract()

        fd = open('E:/wineSpider/maotaiprice.csv', 'w', encoding='utf-8')
        i = 0
        while i < len(name):
            # print(name[i]+','+price[i])
            fd.write(name[i]+','+price[i]+'\n')
            i += 1
        fd.close()






# //*[@id="app"]/div/div[3]/div/div[1]/div/div[1]/div/div[1]/div[2]/text()[1]

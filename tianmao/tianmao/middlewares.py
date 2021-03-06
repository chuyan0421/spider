# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from scrapy.http import HtmlResponse
import time

class JavaScriptMiddleware(object):
    def process_request(self, request, spider):
        if spider.name == "tianmao":
            html = ""
            # driver = webdriver.PhantomJS(executable_path=r"E:\PycharmProjects\phantomjs-2.1.1-windows\bin\phantomjs.exe")
            # options = Options()
            # options.headless = True

            driver = webdriver.Firefox(executable_path=r'C:\geckodriver.exe')
            driver.get(request.url)
            time.sleep(10)
            driver.find_element_by_xpath('//*[@class="sn-container"]/p/a[1]').click()
            print("please log in , and input message in search box ")
            print("waiting...")
            time.sleep(60)
            # driver.find_element_by_xpath('//*[@class="s-combobox-input-wrap"]/input').send_keys('茶')
            # time.sleep(10)
            # driver.find_element_by_xpath('//button[contains(.,"搜索")]').click()
            # time.sleep(10)
            # driver.find_element_by_xpath('//*[@class="main"]/div[4]/a[6]').click
            # driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[3]/div[1]/div[4]/a[6]').click
            # print("please click 店铺")
            # time.sleep(20)
            html = html + driver.page_source
            # print('访问'+request.url)
            print('finish page: 1')
            for i in range(1, 8):
                # next_page = driver.find_element_by_xpath('//a[contains(.,"下一页>>")]')
                print('click next page')
                time.sleep(30)
                # next_page.click()

                html = html + driver.page_source
                print('finish page: ' + str(i+1))
            return HtmlResponse(driver.current_url, body=html, encoding="utf-8", request=request)


class TianmaoSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class TianmaoDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

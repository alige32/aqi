# -*- coding: utf-8 -*-

import logging
from scrapy.http import HtmlResponse

import time
from selenium import webdriver
from retrying import retry


class AqiSeleniumMiddleware(object):
    def __init__(self):
        """
            创建Chrome驱动器对象
        """
        self.driver = webdriver.PhantomJS()
        #self.options = webdriver.ChromeOptions()
        #self.options.add_argument("--handless")
        #self.driver = self.webdriver.Chrome(chrome_options = self.options)

        self.num = 1

    # 最大尝试次数20次，每次间隔200毫秒，
    # 在20次尝试次数内会捕获异常，如果20次后依然有异常，则再向上一级抛出该异常
    @retry(stop_max_attempt_number=20, wait_fixed=200)
    def retry_load_page(self, request):
        try:
            # 如果没有找到数据，则抛出异常被try捕获，代码跳转到except里
            self.driver.find_element_by_xpath("//td[@align='center'][1]")
        except:
            # 打印日志信息
            logging.debug("Retry %s. (%d times)" % (request.url, self.num))
            self.num += 1
            # 因为数据未找到的异常被try捕获了，所以这里需要手动抛出异常让retry捕获，retry才能工作
            raise Exception("%s page loading failed." % request.url)

    def process_request(self, request, spider):
        if "monthdata" in request.url or "daydata" in request.url:
            self.driver.get(request.url)
            self.num = 1

            try:
                # 执行代码，如果没有异常，则代码向下执行，构建响应返回给引擎
                # 如果出现异常（必然是retry抛出的），则交给except处理
                self.retry_load_page(request)

                html = self.driver.page_source
                logging.debug("Retry %s. (Successful)" % request.url)

                # 构建响应对象，返回给引擎，引擎交给Spider处理
                return HtmlResponse(url = self.driver.current_url, body =html.encode("utf-8"), encoding="utf-8", request = request)

            except Exception as e:
                logging.error(e)

    def __del__(self):
        self.driver.quit()

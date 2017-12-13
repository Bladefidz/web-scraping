# -*- coding: utf-8 -*-
import scrapy


class FreeProxySpider(scrapy.Spider):
    name = 'free-proxy'
    allowed_domains = ['nordvpn.com/free-proxy-list']
    start_urls = ['https://nordvpn.com/wp-admin/admin-ajax.php?searchParameters%5B0%5D%5Bname%5D=proxy-country&searchParameters%5B0%5D%5Bvalue%5D=&searchParameters%5B1%5D%5Bname%5D=proxy-ports&searchParameters%5B1%5D%5Bvalue%5D=&offset=0&limit=25&action=getProxies']

    def parse(self, response):
        pass

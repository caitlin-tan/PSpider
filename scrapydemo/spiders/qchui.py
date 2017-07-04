# -*- coding: utf-8 -*-

import re
import sys
import urllib

import scrapy
from scrapy.http import Request
from bs4 import BeautifulSoup

from scrapydemo.items.qchuiProduct import QchuiProduct

class Qchui(scrapy.Spider):
    name = "qchui"

    allowed_domains = ["qchui.cn"]
    start_urls = [
        "http://www.qchui.cn/tuan"
    ]

    def parse(self, response):
        host_url = self.get_host_url(response.url)

        li_list = BeautifulSoup(response.text, 'lxml').find('ul', class_='deal_list').find_all('li')

        next_page_url = self.get_next_page_url(response);
        if (next_page_url != ''):
            yield Request(next_page_url)

        for li in li_list:
            product = QchuiProduct()

            img_div = li.div.div
            href = img_div.find('a', class_='img')['href']
            product['href'] = host_url + href

            img_url = img_div.find('img')['data-src']
            product['image_urls'] = [img_url]

            entity_id = href.split('/')[2]
            match = re.search('/(\d+)$', href)
            product['entity_id'] = match.group(1)

            name_div = li.div.find('div', class_='deal_name')
            product['name'] = name_div.a.get_text()

            desc_div = li.div.find('div', class_='deal_brief')
            product['desc'] = desc_div.a.get_text(strip=True)

            price_div = li.div.find('div', class_='deal_price')
            texts = [text for text in price_div.div.span.stripped_strings]
            product['current_price'] = texts[len(texts) - 1]

            yield product

    def get_host_url(self, url):
        url_parse = urllib.parse.urlparse(url)
        return url_parse.scheme + '://' + url_parse.hostname

    def get_next_page_url(self, response):
        a_list = BeautifulSoup(response.text, 'lxml').find('div', class_='pages').find_all('a')

        next_url = ''
        for a in a_list:
            if ('下一页' != a.get_text()):
                continue
            next_url = a['href']

        if (next_url != ''):
            host_url = self.get_host_url(response.url)
            next_url = host_url + next_url

        return next_url

from typing import Iterable
import scrapy
from scrapy.http import Request
from NhaTro.items import NhatroItem

class TestSpider(scrapy.Spider):
    name = "test"
    allowed_domains = ["timphongtro.vn"]
    start_urls = ["https://timphongtro.vn"]

    def start_requests(self):
        pages = []
        for i in range(131, 150):
            domain = "https://www.timphongtro.vn/?page={}".format(i)
            pages.append(domain)
        for page in pages:
            yield scrapy.Request(url=page, callback=self.parse_link)

    def parse_link(self, response):
        for i in range(1, 20):
            str = '#page-wrap > div.main-container > div:nth-child(4) > div > div > div > div.mbn-box-right.col-md-9.col-sm-9 > div.mbn-box-list > div:nth-child(1) > ul > li:nth-child({}) > span > span.content > span.title > span.subject > a::attr(href)'.format(i)
            link = response.css(str).extract_first()
            link  = 'https://timphongtro.vn/' + link
            yield scrapy.Request(url=link, callback=self.parse)

    def parse(self, response, **kwargs):
        item = NhatroItem()
        item['description'] = response.css('#dvContent > div.ct-body.clearfix > div:nth-child(1) > p::text').extract_first()
        item['price'] = response.css('#dvContent > div.ct-price.clearfix > div.col-md-10.col-sm-10.col-xs-9.price-value::text').extract_first()
        item['address'] = response.css( '#dvContent > div.ct-contact.clearfix > div:nth-child(3) > div.col-md-10.col-sm-10.col-xs-9.contact-name::text').extract_first()
        item['area'] = response.css( '#dvContent > div.ct-contact.clearfix > div:nth-child(1) > div.col-md-10.col-sm-10.col-xs-9.contact-name::text').extract_first()
        yield item


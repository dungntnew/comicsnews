# -*- coding: utf-8 -*-
import scrapy

from urllib.parse import urljoin
from datetime import datetime, timedelta


class NatalieSpider(scrapy.Spider):
    name = 'natalie'
    allowed_domains = ['natalie.mu']
    start_urls = ['http://natalie.mu/comic/news']

    def parse(self, response):
        for href in response.css('#NA_main ul.NA_articleList > li a::attr(href)').extract():
            yield response.follow(urljoin(response.url, href),
                                  callback=self.parse_item)

        should_next = True
        date_arr = response.css('#NA_main ul.NA_articleList > li .NA_date time::text').extract()
        try:
            latest = datetime.strptime(sorted(date_arr)[-1], '%Y年%m月%d日')
            date_N_days_ago = datetime.now() - timedelta(days=self.settings.N_DAYS_AGO)
            should_next = latest >= date_N_days_ago
        except Exception:
            pass

        next_url = response.css(".NA_pagerUnit .NA_next a::attr(href)").extract_first()
        if next_url and should_next:
            yield response.follow(urljoin(response.url, next_url), callback=self.parse)

    def parse_item(self, response):

        published_date =response.css(
                '.NA_articleUnit .NA_articleHeader .NA_attr .NA_date time::text').extract_first()
        published_date = datetime.strptime(published_date, '%Y年%m月%d日 %H:%M')

        item = {
            'url': response.url,
            'provider': 'natalie',
            'title': response.css('.NA_articleUnit .NA_articleHeader h1::text').extract_first(),
            'published_date': published_date,
            'text': ''.join(
                response.css('.NA_articleBody').xpath('.//text()').extract()).strip(),
            'tags': response.css('.NA_articleFooter .NA_relatedTag .NA_links a').xpath(
                'normalize-space(.//text())').extract(),
            'images': [],
        }

        image_list_href = response.css('.GAE_newsListImage a.NA_more::attr(href)').extract_first()
        yield scrapy.Request(url=urljoin(response.url, image_list_href),
                             callback=self.parse_image,
                             meta=dict(item=item))

    def parse_image(self, response):
        item = response.meta['item']

        item['images'].append(
            response.css('.NA_galleryBody .NA_figureUnit .GAE_galleryMainImage img::attr(src)').extract_first(),
        )

        next_image_href = response.css('.NA_galleryBody .NA_figureUnit .GAE_arrowNext a::attr(href)').extract_first()
        if next_image_href:
            yield scrapy.Request(urljoin(response.url, next_image_href),
                                 callback=self.parse_image,
                                 meta=dict(item=item))
        else:
            yield item

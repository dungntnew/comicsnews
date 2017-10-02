# -*- coding: utf-8 -*-
import scrapy

from urllib.parse import urljoin
from datetime import datetime, timedelta


class AnimeEigaSpider(scrapy.Spider):
    name = 'animeeigai'
    allowed_domains = ['anime.eiga.com']
    start_urls = ['http://anime.eiga.com/news']

    def parse(self, response):
        for href in response.css("ul.newsContainer .newsListTtl a::attr(href)").extract():
            yield response.follow(urljoin(response.url, href),
                                  callback=self.parse_item)

        should_next = True
        # date_arr = response.css('ul.newsContainer .newsListTtl span::attr(datetime)').extract()
        # try:
        #     latest = datetime.strptime(sorted(date_arr)[-1].replace('+09:00', ''), '%Y-%m-%dT%H:%M:%S')
        #     date_N_days_ago = datetime.now() - timedelta(days=self.settings.N_DAYS_AGO)
        #     should_next = latest >= date_N_days_ago
        # except Exception:
        #     pass

        next_url = response.css('.pageInfoArea .pagination .next_page::attr(href)').extract_first()
        if next_url and should_next:
            yield response.follow(urljoin(response.url, next_url), callback=self.parse)

    def parse_item(self, response):

        published_date = response.css('.headArea .newsDate::text').extract_first();
        published_date = datetime.strptime(published_date, '%Y年%m月%d日 %H:%M')

        item = {
            'url': response.url,
            'provider': 'animeeigai',
            'title': response.css('.articleContainer .headArea h1::text').extract_first(),
            'published_date': published_date,
            'text': ''.join(response.css('.newsDetailBox > p').xpath('.//text()').extract()).strip(),
            'tags': response.css('.tagList li a::text').extract(),
            'images': [],
        }

        image_list_href = response.css('.newsDetailBox .photoLarge span::attr(data-href)').extract_first()
        yield scrapy.Request(url=urljoin(response.url, image_list_href),
                             callback=self.parse_image,
                             meta=dict(item=item))

    def parse_image(self, response):
        item = response.meta['item']

        item['images'].append(
            response.css('.newsDetailBox .photoLargeArea .photoGallaryLarge img::attr(src)').extract_first(),
        )

        next_image_href = response.css('.controlBtn02 span[data-href]::attr(data-href)').extract_first()
        if next_image_href:
            yield scrapy.Request(urljoin(response.url, next_image_href),
                                 callback=self.parse_image,
                                 meta=dict(item=item))
        else:
            yield item

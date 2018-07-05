# -*- coding: utf-8 -*-
import scrapy
import os
import json
import datetime


class ScrawlerSpider(scrapy.Spider):
    name = "test"

    def __init__(self, *a, **kw):
        super(ScrawlerSpider, self).__init__(*a, **kw)

    '''
     Forked and modified code form example crawler I linked in chat before
     No need rewriting this, just updated it to work on the UK archives rather than US (Which was a pain in its own
     right.

     Start_requests, parse_year and parse_day just iterate through the levels of the archive, nothing special.
     Parse_article looks for the speciifc information in the html like atags and divs with specific classes...
     Each specific article has its own json object made
    '''

    def start_requests(self):

        base_url = 'http://www.reuters.com/resources/archive/uk/'
        # years = [2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017]
        years = [2018]

        for year in years:
            url = base_url + str(year) + '.html'
            yield scrapy.Request(url=url, callback=self.parse_year)

    def parse_year(self, response):
        days = response.xpath("//p/a[starts-with(@href, \
                              '/resources/archive/uk/')]")
        for day in days:
            day_url = day.xpath('@href').extract_first()
            date = day_url.split("/")[-1][:-5]  # e.g. 20160130
            item = {'date': date}
            yield scrapy.Request(url=response.urljoin(day_url),
                                 callback=self.parse_day, meta={'item': item})

    def parse_day(self, response):
        articles = response.xpath("//div/a[starts-with(@href, \
                              'http://UK.reuters.com/article')]")

        now = datetime.datetime.now()
        count = 0
        for article in articles:
            # Encoded from july only, need to be reset each month
            if count > now.day:
                article_link = article.xpath("@href").extract_first()
                article_title = article.xpath("text()").extract_first()
                item = response.meta['item']
                item['title'] = article_title

                yield scrapy.Request(url=response.urljoin(article_link),
                                     callback=self.parse_article,
                                     meta={'item': item})

            count += 1

    def parse_article(self, response):

        symbol = response.xpath('//a[contains(@href, "symbol")]/@href').extract_first()

        title = response.xpath('//title/text()').extract_first()
        date = response.xpath('//div[@class="date_V9eGk"]/text()').extract_first()

        # Make sure to remove all generated files because I did not include any overwriting.
        # symbol check just disregards stories without symbols, of which there are many!
        if symbol is not None:
            if not os.path.exists("./out/"):
                os.makedirs("./out/")
            with open(os.path.join("./out/", "titles_june_18.json"), 'a') as out_file:
                article = {'title': title, 'symbol': symbol, 'date': date}
                out = json.dumps(article)
                out_file.write(out + "\n")


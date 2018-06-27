# -*- coding: utf-8 -*-
import scrapy
import os
import json


class ScrawlerSpider(scrapy.Spider):
    name = "test"

    def __init__(self, *a, **kw):
        super(ScrawlerSpider, self).__init__(*a, **kw)

    def start_requests(self):
        base_url = 'http://www.reuters.com/resources/archive/uk/'
        # years = [2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017]
        years = [2018]

        for year in years:
            url = base_url+str(year)+'.html'
            yield scrapy.Request(url=url, callback=self.parse_year)

    def parse_year(self, response):
        days = response.xpath("//p/a[starts-with(@href, \
                              '/resources/archive/uk/')]")
        for day in days:
            day_url = day.xpath('@href').extract_first()
            date = day_url.split("/")[-1][:-5] # e.g. 20160130
            item = {'date':date}
            yield scrapy.Request(url=response.urljoin(day_url), \
                                 callback=self.parse_day, meta={'item':item})

    def parse_day(self, response):
        articles = response.xpath("//div/a[starts-with(@href, \
                              'http://www.reuters.com/article/')]")
        for article in articles:
            article_link = article.xpath("@href").extract_first()
            article_title = article.xpath("text()").extract_first()
            item = response.meta['item']
            item['title'] = article_title

            yield scrapy.Request(url=response.urljoin(article_link), \
                                 callback=self.parse_article, \
                                 meta={'item':item})

    def parse_article(self, response):
        item = response.meta['item']
        year = item['date'][0 : 2]
        month = item['date'][2 : 4]
        day = item['date'][4 : 6]
        formatted_date = day + '-' + month + '-' + year
        atags = response.xpath('//a[contains(@href, "symbol")]/@href').extract_first()

        #section = response.xpath("//div[contains(@class, 'ArticleHeader_channel')]\
        #                         /a/text()").extract_first().replace(" ", "_")
        title = response.xpath('//title/text()').extract_first()
        print(title + ' ' + formatted_date + ' ' + atags)
        #texts = response.xpath("//div[contains(@class, 'StandardArticleBody')]//text()").extract()
        #texts = [i.strip() for i in texts if len(i.strip()) > 0]
        section = ''
        texts = ''

        date = item['date']

        direc = date[:4]+"/"+date[4:6]+"/"
        save_path = "./crawled/"+direc # e.g. ./crawled/2011/02
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        with open(os.path.join(save_path, date[-2:]+".json"), 'a') as out_file:
            article = {
                        'title':title, 'section':section,
                        'date':date, 'text':texts
                      }
            out = json.dumps(article)
            out_file.write(out+"\n")


import scrapy
from ..items import DraftspiderItem
from datetime import datetime

class APISpider(scrapy.Spider):
    name = 'api'
    start_urls = ['http://outbreaknewstoday.com/category/headlines/']

    def parse(self, response):
        article_links = response.css('div.rightconside a ::attr(href)')
        for link in article_links:
            url = link.get()
            if url:
                yield response.follow(url=url, callback=self.parse_article)
        next_page = response.css('a.next.page-numbers').attrib['href']
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
    
    def parse_article(self, response):
        url = response.url
        # date format: 2018-11-xx 17:00:xx
        extract_datetime = response.xpath("//meta[@property='article:published_time']/@content").get()
        date_str = extract_datetime[:-6]
        date_of_publication = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
        # headline = response.css('div.posttitle h1::text').get().strip()
        headline = response.xpath('//title/text()').get()
        content = response.css('div.postcontent p::text').getall()[1:-1]
        main_text = ' '.join(content)
        report = '[<object::report>]'

        item = DraftspiderItem()
        # salmonella case -> temporary
        if 'salmonella' in headline:
            item["url"] = url
            item["date_of_publication"] = date_of_publication
            item["headline"] = headline
            item["main_text"] = main_text
            item["report"] = report
            yield item
import scrapy
from ..items import ArticleItem
from datetime import datetime

class APISpider(scrapy.Spider):
    name = 'api'
    start_urls = ['http://outbreaknewstoday.com/category/headlines/']

    def parse(self, response):
        article_links = response.css('div.posttitle a ::attr(href)')
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
        headline = response.xpath('//title/text()').get()
        content = response.css('div.postcontent p::text').getall()[1:-1]
        main_text = ' '.join(content)
        report = '[<object::report>]'
        
        articleItem = ArticleItem()
        # result = {articleItem}
        # salmonella case -> temporary
        if 'salmonella' in headline:
            articleItem["url"] = url
            articleItem["date_of_publication"] = date_of_publication
            articleItem["headline"] = headline
            articleItem["main_text"] = main_text
            # articleItem["report"] = report
            yield articleItem
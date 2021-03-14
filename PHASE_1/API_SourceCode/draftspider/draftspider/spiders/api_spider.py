import scrapy
import merpy
from ..items import ArticleItem, ReportItem, LocationItem
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
        # next_page = response.css('a.next.page-numbers').attrib['href']
        # if next_page is not None:
        #     yield response.follow(next_page, callback=self.parse)
    
    def parse_article(self, response):
        url = response.url
        # date format: 2018-11-xx 17:00:xx
        extract_datetime = response.xpath("//meta[@property='article:published_time']/@content").get()
        date_str = extract_datetime[:-6]
        if date_str is None:
            date_of_publication = "xxxx-xx-xx xx:xx:xx"
        else:
            date_of_publication = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")

        # extract information for article object
        headline = response.xpath('//title/text()').get()
        content = response.css('div.postcontent p::text').getall()[1:-1]
        main_text = ' '.join(content)
        report = '[<object::report>]'

        # integrate NLP tool to examine the headline
        # extract diseases
        merpy.process_lexicon("doid")
        di_meta = merpy.get_entities(headline, "doid")
        di_str = "<diseases>"
        if di_meta != [['']]:
            print("=======================>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<==============")
            print(di_meta)
            di_list = [ sublist[2] for sublist in di_meta ]
            di_str = ','.join(di_list)

        # placeholders for internal objects
        articleItem = ArticleItem()
        reportItem = ReportItem()
        locationItem = LocationItem()
        # location item
        locationItem["country"] = "<country>"
        locationItem["location"] = "<location>"
        # report item
        reportItem["diseases"] = di_str
        reportItem["syndromes"] = "<syndrome description>"
        reportItem["event_date"] = date_of_publication
        reportItem["location"] = [dict(locationItem)]
        # article item
        articleItem["url"] = url
        articleItem["date_of_publication"] = date_of_publication
        articleItem["headline"] = headline
        articleItem["main_text"] = main_text
        articleItem["report"] = [dict(reportItem)]


        # if 'COVID-19' in headline:
        yield articleItem
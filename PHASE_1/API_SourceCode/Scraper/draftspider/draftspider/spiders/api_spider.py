import scrapy
from ..items import ArticleItem, ReportItem, LocationItem
from datetime import datetime

class APISpider(scrapy.Spider):
    name = 'api'
    start_urls = ['http://outbreaknewstoday.com/category/headlines/']
    custom_settings = {
        "DOWNLOAD_DELAY": 1, # in case some websites prevent scraping if the time between request is too small
        "RETRY_ENABLED": True,
    }

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
        text_dirty = response.xpath('//div[@class="postcontent"]/*[self::p or self::ul or self::h3]//text()[not(parent::script)][not(parent::a/parent::strong)][not(parent::a[@href]/parent::*[not(text())])][not(parent::strong/parent::a/parent::*[not(text())])][not(parent::strong/parent::em/parent::a[not(text())])]').getall()
        # trim white spaces, \xA0 and new line characters for every element in list
        text_list = [ piece.strip().replace('\xA0', ' ') for piece in text_dirty if piece.strip()]
        text_clean = []
        for piece in text_list:
            # remove empty strings and author text
            if piece == '' or piece == 'By NewsDesk' or piece == '@bactiman63':
                continue
            text_clean.append(piece)

        # placeholders for internal objects
        articleItem = ArticleItem()
        reportItem = ReportItem()
        locationItem = LocationItem()
        # location item
        locationItem["country"] = "<country>"
        locationItem["location"] = "<location>"
        # report item
        reportItem["diseases"] = ["<diseases>"]
        reportItem["syndromes"] = ["<syndromes>"]
        reportItem["event_date"] = date_of_publication
        reportItem["locations"] = [locationItem]
        # article item
        articleItem["url"] = url
        articleItem["date_of_publication"] = date_of_publication
        articleItem["headline"] = headline
        articleItem["main_text"] = ' '.join(text_clean)
        articleItem["reports"] = [reportItem]

        yield articleItem
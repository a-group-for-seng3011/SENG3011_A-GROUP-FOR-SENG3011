import scrapy

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
        for info in response.css('div.postsingle'):
            content = info.css('div.postcontent p::text').getall()[1:-1]
            main_text = ' '.join(content)
            # salmonella case -> temp
            if 'salmonella' in main_text:
                yield {
                    'url': response.url,
                    'date_of_publication': info.css('div.datsingle::text').get(),
                    'headline': info.css('div.posttitle h1::text').get().strip(),
                    'main_text': main_text,
                    'report': '[<object::report>]'
                }
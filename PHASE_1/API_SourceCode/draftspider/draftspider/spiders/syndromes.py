import scispacy
import scrapy

import inflect
import en_ner_bc5cdr_md

from ..items import ArticleItem, ReportItem, LocationItem
from datetime import datetime

def find_syndromes(content):
    # nlp_web_sm = spacy.load('en_core_web_sm')
    nlp_bc = en_ner_bc5cdr_md.load()
    inf = inflect.engine()
    # doc_web_sm = nlp_web_sm(content)
    doc_bc = nlp_bc(content)

    # combine text with its label
    label = {}
    for token in doc_bc.ents:
        label[token.text] = token.label_
    # combine text with its pos
    pos = {}
    for token in doc_bc:
        pos[token.text] = token.pos_
    # combine text with its lemma
    lemma = {}
    for token in doc_bc:
        lemma[token.text] = token.lemma_

    
    syndromes = []
    for k, v in label.items():
        if v == "DISEASE":
            li = k.split(" ")
            noun = 0
            adj = 0
            adp = 0
            if li[-1].lower() == "coronavirus":
                continue
            for c in li:
                if "CoV" in c or c.isupper() or lemma[c] != c:
                    break

                if pos.get(c) == "ADJ":
                    adj += 1
                elif pos.get(c) == "NOUN":
                    noun += 1
                # "of" case
                elif pos.get(c) == "ADP":
                    adp += 1
            if adj == 0 and noun >= 1:
                syndromes.append(k)
            elif adj == 1 and (noun >= 1 and noun <= 2):
                syndromes.append(k)
            elif adj == 0 and noun >= 1 and adp >= 1:
                syndromes.append(k)
    return syndromes

class APISpider(scrapy.Spider):
    name = 'syndromes'
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
        if date_str is None:
            date_of_publication = "xxxx-xx-xx xx:xx:xx"
        else:
            date_of_publication = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")

        headline = response.xpath('//title/text()').get()
        content = response.css('div.postcontent p::text').getall()[1:-1]
        main_text = ' '.join(content)
        report = '[<object::report>]'
        
        articleItem = ArticleItem()
        reportItem = ReportItem()
        locationItem = LocationItem()

        # salmonella case
        if 'salmonella' in headline:
            # location item
            locationItem["country"] = "empty country"
            locationItem["location"] = "empty location"
            # report item
            reportItem["diseases"] = "salmonella"
            reportItem["syndromes"] = find_syndromes(main_text)
            reportItem["event_date"] = date_of_publication
            reportItem["location"] = [dict(locationItem)]
            # article item
            articleItem["url"] = url
            articleItem["date_of_publication"] = date_of_publication
            articleItem["headline"] = headline
            articleItem["main_text"] = main_text
            articleItem["report"] = [dict(reportItem)]
            yield articleItem
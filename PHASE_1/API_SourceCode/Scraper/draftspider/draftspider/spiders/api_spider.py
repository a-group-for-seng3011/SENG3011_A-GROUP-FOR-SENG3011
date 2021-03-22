import scrapy
from ..items import ArticleItem, ReportItem, LocationItem
from datetime import datetime

def find_location(content):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(content)
    #combine text with its label
    labl = {}
    for token in doc.ents:
        labl[token.text] = token.label_
    # combine text with its lemma
    lemma = {}
    for token in doc:
        lemma[token.text] = token.lemma_

    gpe = []
    location = []
    for wrd,lbl in labl.items():
        if lbl == "GPE":
            gpe.append(wrd)
            
    for text in gpe:
        summary = str(wikipedia.summary(text))
        if ('city' in summary):
            location.append(text)
    return location

def find_country(content):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(content)
    #combine text with its label
    ​label = {}
    for token in doc.ents:
        label[token.text] = token.label_
    # combine text with its lemma
    lemma = {}
    for token in doc:
        lemma[token.text] = token.lemma_

    gpe =[]
    country=[]
    for wrd,lbl in label.items():
        if lbl == "GPE":
            gpe.append(wrd)
            
    for text in gpe:
        summary = str(wikipedia.summary(text))
        if ('country' in summary):
            country.append(text)
    return country


def find_syndromes(diseases, content):
    diseases_list = diseases.split(',')
    # nlp_web_sm = spacy.load('en_core_web_sm')
    nlp_bc = en_ner_bc5cdr_md.load()
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
                if "CoV" in c:
                    break
                if c.isupper():
                    break
                if lemma[c] != c:
                    break
                if "disease" in c:
                    break
                if c in diseases_list:
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
    name = 'api'
    start_urls = ['http://outbreaknewstoday.com/category/headlines/']
    custom_settings = {
        "DOWNLOAD_DELAY": 2, # in case some websites prevent scraping if the time between request is too small
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
        text = [
            ' '.join(
                line.strip() 
                for line in p.xpath('.//text()[not(parent::script)]').extract() 
                if line.strip()
            ) 
            for p in response.xpath('//div[@class="postcontent"]/p')
        ]
        text_list = []
        for elem in text:
            if elem != '':
                text_list.append(elem)
        text_list.pop(0)
        # TODO: also need to remove the headline of other articles inside the main_text
        main_text = ' '.join(text_list)

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
        articleItem["main_text"] = main_text
        articleItem["reports"] = [reportItem]

        yield articleItem
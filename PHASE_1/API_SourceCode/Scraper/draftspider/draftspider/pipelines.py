# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import mymerpy
import spacy
import en_ner_bc5cdr_md
from geopy.geocoders import Nominatim
import gc
import wikipedia
from items import ArticleItem, ReportItem, LocationItem

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from .items import ArticleItem, ReportItem, LocationItem

# integrate stream editing tools to examine the headline and extract diseases
class DiseaseExtractionPipeline:
    def process_item(self, item, spider):
        meta_hl = mymerpy.get_entities(item['headline'], "doid")
        meta_ct = mymerpy.get_entities(item['main_text'], "doid")

        if meta_ct != [['']]:
            item['reports'][0]['diseases'] = [ sublist[2] for sublist in meta_ct ]

        if meta_hl != [['']]:
            item['reports'][0]['diseases'] = [ sublist[2] for sublist in meta_hl ]

        # remove duplicates
        _list = item['reports'][0]['diseases']
        item['reports'][0]['diseases'] = list(set(_list))
        return item

class SyndromeExtractionPipeline:
    def process_item(self, item, spider):
        diseases_list =  item['reports'][0]['diseases']
        nlp_bc = en_ner_bc5cdr_md.load()
        doc_bc = nlp_bc(item['main_text'])

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
        gc.collect()
        item['reports'][0]['syndromes'] = syndromes
        return item

# TODO: not yet complete
class LocationExtractionPipeline:
    def process_item(self, item, spider):
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(item['main_text'])
        #combine text with its label
        labl = {}
        for token in doc.ents:
            labl[token.text] = token.label_

        gpe = []
        # TODO: why are they lists?
        location = []
        country = []
        for wrd,lbl in labl.items():
            if lbl == "GPE":
                gpe.append(wrd)
                
        for text in gpe:
            summary = str(wikipedia.summary(text))
            if not ('country' in summary):
                location.append(text)
            if ('country' in summary):
                country.append(text)

        if len(location) > 0:
            geolocator = Nominatim(user_agent = "geoapiExercises")
            cntry = geolocator.geocode(location[0])
    
        # TODO: it's not complete, isn't it? 
        # locations --(1)--------(n)-- locationItem, which means locations = [locationItem1, locationItem2, ...]
        # locationItem = { country:<string>, location: <string> }
        # TODO: your code here is for the 'location' attribute of a locationItem, it should be **a string** rather than a list
        item['reports'][0]['locations'][0]['location'] = location[0] # TODO: why is this a list? or what does it stand for if you think it should be a list?
        # TODO: your code here is for the 'country' attribute of a locationItem, it should be **a string** rather than a list
        item['reports'][0]['locations'][0]['country'] = cntry # TODO: why is this a list? or what does it stand for if you think it should be a list?
        return item

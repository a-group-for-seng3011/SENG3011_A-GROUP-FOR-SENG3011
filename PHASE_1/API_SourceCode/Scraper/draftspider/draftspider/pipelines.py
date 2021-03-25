# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import mymerpy
import spacy
import en_ner_bc5cdr_md
import gc
import geonamescache

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
        gc.collect()
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
        gc = geonamescache.GeonamesCache()
        # gets nested dictionary for countries
        countries = gc.get_countries()
        country_list = {}
        for country in countries:
            for k, v in countries[country].items():
                if k == "name":
                    country_list[v] = country
                elif k == "iso":
                    country_list[v] = country
                    s = ".".join(v[i:i + 1] for i in range(0, len(v), 1))
                    country_list[s] = country
                elif k == "iso3":
                    country_list[v] = country
        # gets nested dictionary for cities
        cities = gc.get_cities()
        city_list = []
        city_country = []
        for elem in cities.values():
            city_list.append(elem['name'])
            city_country.append({elem['name']: elem['countrycode']})

        nlp = spacy.load("en_core_web_sm")
        doc = nlp(item['main_text'])
        country = []
        location = []
        count_country = {}
        result = []
        for ent in doc.ents:
            if ent.label_ == 'GPE':
                # find the matching country inside country_list
                find_country = country_list.get(ent.text)
                if find_country is not None and count_country.get(find_country) is None:
                    count_country[find_country] = count_country.get(find_country, 0) + 1
                    country.append(ent.text)
                elif ent.text in city_list:
                    for dict_city_country in city_country:
                        if ent.text in list(dict_city_country.keys()):
                            location.append(dict_city_country)
        for country_name in country:
            iso = country_list[country_name]
            for location_dict in location:
                if iso in list(location_dict.values()):
                    result.append({"country": country_name, "location": list(location_dict.keys()).pop(0)})
            if not any(elem["country"] == country_name for elem in result):
                result.append({"country": country_name, "location": ""})

        i = 0
        for e in result:
            if i == 0:
                item['reports'][0]['locations'][i]['location'] = e['location']
                item['reports'][0]['locations'][i]['country'] = e['country']
                i = 1
            else:
                item['reports'][0]['locations'].append(e)
        return item

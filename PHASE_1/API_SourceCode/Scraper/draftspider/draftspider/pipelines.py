# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import mymerpy
import spacy
import en_ner_bc5cdr_md
import gc
import geonamescache
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

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
                    locationItem = LocationItem()
                    locationItem["country"] = country_name
                    locationItem["location"] = list(location_dict.keys()).pop(0)
                    result.append(locationItem)
            if not any(elem["country"] == country_name for elem in result):
                result.append({"country": country_name, "location": ""})

        i = 0
        for e in result:
            item['reports'][0]['locations'].append(e)
        return item

# TODO: create requests to the GraphQL API on AWS
# TODO: DON'T FORGET to remove comment in settings.py when finished
# API URL: https://jadwqdo2anaydpf3tx4leaqvgy.appsync-api.ap-southeast-2.amazonaws.com/graphql
# API KEY: da2-q4rynvvl4vg3njaluug2tptjru
class GraphQLMutationPipeline:
    def __init__(self):
        # Select transport with our url endpoint
        # TODO: Mock api
        transport = AIOHTTPTransport(url='http://129.94.242.117:20002/graphql', headers={'x-api-key': 'da2-fakeApiId123456'})
        # self.transport = AIOHTTPTransport(url='https://jadwqdo2anaydpf3tx4leaqvgy.appsync-api.ap-southeast-2.amazonaws.com/graphql', headers={'x-api-key': 'da2-q4rynvvl4vg3njaluug2tptjru'})
        # Create a GraphQL client using the defined transport
        self.client = Client(transport=transport, fetch_schema_from_transport=True)

    def process_item(self, item, spider):
        # TODO: mock item
        item = {
            "url": "http://outbreaknewstoday.com/sexually-transmitted-infections-in-the-us-the-burden-of-stis-is-staggering-43427/",
            "date_of_publication": "2021-01-26T11:41:34.000Z",
            "headline": "some headline text",
            "main_text": "lots of text content for main text",
            "reports": [
                {
                    "diseases": [
                        "COVID-19",
                        "HPV",
                        "pelvic inflammatory disease",
                        "HIV",
                        "syphilis"
                    ],
                    "syndromes": [
                        "infection",
                        "infertility",
                        "chlamydia",
                        "gonorrhea"
                    ],
                    "event_date": "2021-01-26T11:41:34.000Z",
                    "locations": [
                        {
                            "country": "",
                            "location": ""
                        }
                    ]
                }
            ]
        }

        # create an article
        articleQuery = gql('''
            mutation articleMutation ($input: CreateArticleInput!) {
                createArticle (input: $input){id}
            }
        ''')
        articleParams = {
            'input': {
                'date_of_publication': item['date_of_publication'],
                'headline': item['headline'],
                'main_text': item['main_text'],
                'url': item['url']
            }
        }
        # TODO: Mock request
        articleID = client.execute(articleQuery, variable_values=articleParams)['createArticle']['id']
        # articleID = self.client.execute(articleQuery, variable_values=articleParams)['createArticle']['id']

        # create a report
        reportQuery = gql('''
            mutation reportMutation ($input: CreateReportInput!) {
                createReport (input: $input){id}
            }
        ''')
        reportParams = {
            'input': {
                'event_date': item['reports'][0]['event_date'],
                'articleID': articleID
            }
        }
        # TODO: Mock request
        reportID = client.execute(reportQuery, variable_values=reportParams)['createReport']['id']
        # reportID = self.client.execute(reportQuery, variable_values=reportParams)['createReport']['id']

        # create a list of diseases
        diseasesIDs = []
        for disease in item['reports'][0]['diseases']:
            diseaseQuery = gql('''
                mutation diseaseMutation ($input: CreateDiseaseInput!) {
                    createDisease (input: $input){id}
                }
            ''')
            diseaseParams = {
                'input': {
                    'name': disease,
                    'reportID': reportID
                }
            }
            # TODO: Mock request
            diseaseID = client.execute(diseaseQuery, variable_values=diseaseParams)['createDisease']['id']
            # diseaseID = self.client.execute(diseaseQuery, variable_values=diseaseParams)['createDisease']['id']
            diseasesIDs.append(diseaseID)

        # create a list of syndromes
        syndromesIDs = []
        for syndrome in item['reports'][0]['syndromes']:
            syndromeQuery = gql('''
                mutation syndromeMutation ($input: CreateSyndromeInput!) {
                    createSyndrome (input: $input){id}
                }
            ''')
            syndromeParams = {
                'input': {
                    'name': syndrome,
                    'reportID': reportID
                }
            }
            # TODO: Mock request
            syndromeID = client.execute(syndromeQuery, variable_values=syndromeParams)['createSyndrome']['id']
            # syndromeID = self.client.execute(syndromeQuery, variable_values=syndromeParams)['createSyndrome']['id']
            syndromesIDs.append(syndromeID)
        
        # create a list of locations
        locationsIDs = []
        for locationItem in item['reports'][0]['locations']:
            locationQuery = gql('''
                mutation locationMutation ($input: CreateLocationInput!) {
                    createLocation (input: $input){id}
                }
            ''')
            locationParams = {
                'input': {
                    'country': locationItem['country'],
                    'location': locationItem['location'],
                    'reportID': reportID
                }
            }
            # TODO: Mock request
            locationID = client.execute(locationQuery, variable_values=locationParams)['createLocation']['id']
            # locationID = self.client.execute(locationQuery, variable_values=locationParams)['createLocation']['id']
            locationsIDs.append(locationID)
        
        return item
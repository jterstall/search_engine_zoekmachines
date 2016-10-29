import gzip
import xmltodict, json
from xml.dom.minidom import parse, parseString
from elasticsearch import  helpers
from elasticsearch import Elasticsearch
import sys

# GET DATE FROM ARTICLE
def get_date(i):
    return o['pm:KBroot']['pm:root'][i]['pm:meta']['dc:date']['#text']

# GET TITEL FROM ARTICLE
def get_title(i):
    try:
        return o['pm:KBroot']['pm:root'][i]['pm:content']['title']['#text']
    except (KeyError):
        return ''

# GET TEXT FROM ARTICLE
def get_text(i):
    #sometimes, articles have more than 1 #text field
    try:
        return o['pm:KBroot']['pm:root'][i]['pm:content']['text']['p']['#text']
    except (TypeError):
        try:
            text = ''
            for j in range(len(o['pm:KBroot']['pm:root'][i]['pm:content']['text']['p'])):
                text = text + o['pm:KBroot']['pm:root'][i]['pm:content']['text']['p'][j]['#text']
            return text
        # in very rare cases where other errors occur, return empty string
        except (TypeError):
            return ''
    except (KeyError):
        return ''

def get_link(i):
    try:
        return o['pm:KBroot']['pm:root'][i]['pm:meta']['dc:identifier']['#text']
    except (KeyError):
        return ''


if __name__ == '__main__':
    text = input("Please input a query: ")
    HOST = 'http://localhost:9200/'
    es = Elasticsearch(hosts=[HOST])
    # query={
    #     "query": {
    #         "bool": {
    #             "must": [
    #                 { "match": {"text": text}}
    #             ]
    #         }
    #     }
    # }
    # Je kan al gekke queries doen met deze shit zoals: +japan -keizer ofzo
    # Of title:Japan, boolean, etc.
    # https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html
    query= {
        "query": {
            "query_string": {
                "default_field": "text",
                "query" : text
            }
        },
        "aggregations": {
            "wordCloudInfo" : {
                "significant_terms" : {"field": "text"}
            }
        }
    }

    # Bij het indexen worden die textvelden boven de 256 niet opgeslagen

    # Retrieve total amount of search hits, uncomment for unlimited results
    # amount_of_results = es.search(body=query, index='_all')['hits']['total']
    # Or use limited size
    amount_of_results = 100
    query = es.search(body=query, index='telegraaf', size=amount_of_results)
    print(query['aggregations'])
    # for result in query['hits']['hits']:
    #     print(result['_source']['title'] + "\n")
    #     print(result['_source']['date'] + "\n")
    #     print(result['_source']['text'] + "\n")
    #     try:
    #         print(result['_source']['link'] + "\n")
    #     except(KeyError):
    #         print("No link \n")

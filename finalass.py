import gzip
import xmltodict, json
from xml.dom.minidom import parse, parseString
from elasticsearch import  helpers
from elasticsearch import Elasticsearch
import sys

search = sys.argv[1]
title = sys.argv[2]
text = sys.argv[3]
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
    HOST = 'http://localhost:9200/'
    es = Elasticsearch(hosts=[HOST], timeout=60)
    es.indices.clear_cache(index='telegraaf')
    # Run deze twee in terminal
    # curl -XPUT 'localhost:9200/telegraaf/_mapping/article?pretty' -d'
    # {
    #   "properties": {
    #     "text": {
    #       "type":     "text",
    #       "fielddata": true
    #     }
    #   }
    # }'
    # curl -XPUT 'localhost:9200/telegraaf/_mapping/article?pretty' -d'
    # {
    #   "properties": {
    #     "title": {
    #       "type":     "text",
    #       "fielddata": true
    #     }
    #   }
    # }'

    query= {
        "query": {
            "query_string": {
                "default_field": "text",
                "query" : search
            }
        },
        "aggregations": {
            "wordCloudInfo" : {
                "significant_terms" : {"field": "title"}
            }
        }
    }
    if(title == "Yes" and text == "Yes"):
        query= {
            "query": {
                "query_string": {
                    "fields" : ['title', 'text'],
                    "query" : search
                }
            },
            "aggregations": {
                "wordCloudInfo" : {
                    "significant_terms" : {"field": "title"}
                }
            }
        }
    elif(title == "Yes" and text != "Yes"):
        query= {
            "query": {
                "query_string": {
                    "default_field": "title",
                    "query" : search
                }
            },
            "aggregations": {
                "wordCloudInfo" : {
                    "significant_terms" : {"field": "title"}
                }
            }
        }

    # https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html

    # Retrieve total amount of search hits, uncomment for unlimited results
    # amount_of_results = es.search(body=query, index='_all')['hits']['total']
    # Or use limited size
    amount_of_results = 100
    query = es.search(body=query, index='telegraaf', size=100)
    for result in query['hits']['hits']:
        print(result['_source']['title'] + "\n")
        print(result['_source']['date'] + "\n")
        print(result['_source']['text'] + "\n")
        try:
            print(result['_source']['link'] + "\n")
        except(KeyError):
            print("No link \n")
    print(query['aggregations'])

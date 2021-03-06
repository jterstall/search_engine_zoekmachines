from elasticsearch import Elasticsearch
import sys
import re

search = sys.argv[1]
title = sys.argv[2]
text = sys.argv[3]
year = sys.argv[4]

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

    if(title == "Yes" and text == "Yes"):
        field = ["text", "title"]
    elif(title == "Yes" and text == "No"):
        field = ["title"]
    elif(title == "No" and text == "Yes"):
        field = ["text"]
    else:
        field = ["text"]

    if(year != "0"):
        query= {
                "query": {
                    "bool": {
                        "must": [
                        {
                            "query_string": {
                                "fields" : field,
                                "query" : search
                            }
                        },
                        {
                            "range" : {
                                "date": {
                                    "gte": year + "||/y",
                                    "lte": year + "||/y",
                                    "format": "yyyy"
                                }
                            }
                        }
                        ]
                    }
                },
                "aggregations": {
                    "wordCloudInfo" : {
                        "significant_terms" : {"field": "title"}
                    }
                }
            }
    else:
        query = {
            "query" : {
                "query_string": {
                    "fields": field,
                    "query": search
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
    query = es.search(body=query, index='telegraaf', size=amount_of_results)
    print(("It took " + str(query['took']) + " seconds to execute the query which resulted into " + str(query['hits']['total']) + " hits </br></br>").encode('utf-8'))
    for result in query['hits']['hits']:
        title = result['_source']['title']
        if title == "":
            title = "No title"
        try:
            link = result['_source']['link']
        except(KeyError):
            link = ""
        print(("<a href=" + link + ">" + title + "</a></br>").encode('utf-8'))
        print((result['_source']['date'] + "</br>").encode('utf-8'))
        text = result['_source']['text']
        sentences = re.split('(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
        if search in text:
            for i in range(len(sentences)):
                if(search in sentences[i]):
                    sentences[i] = (re.sub(r'(?<=[\.\s]){0}(?=[\.\s])|^{0}(?=[\.\s])'.format(search), '<b>{0}</b>'.format(search), sentences[i]))
                    if i == 0:
                        serp = ' '.join(sentences[i:i+2]) + " ... </br></br>"
                    elif i == len(sentences) - 1:
                        serp = "... " + ' '.join(sentences[i-2:i]) + "</br></br>"
                    else:
                        serp = ' '.join(sentences[i-1:i+1]) + " ... </br></br>"
                    break
        else:
            serp = ' '.join(sentences[:3]) + " ... </br></br>"
        print(serp.encode('utf-8'))
    # print(query['aggregations'])

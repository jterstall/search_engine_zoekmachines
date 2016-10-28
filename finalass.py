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
	# open and read gzipped xml file
	# infile = gzip.open('telegraaf-1951.xml.gz')
	# content = infile.read()
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

	# o = xmltodict.parse(content)

	# use xmltodict to convert xml file to json (elasticsearch needs json input)
	#make json dump
	# dump = json.dumps(o) # '{"e": {"a": ["text", "text"]}}'
	#e.g. simple search for "Japan" in text
	# telegraaf = list()
	# for i in range(len(o['pm:KBroot']['pm:root'])):
	# 	telegraaf.append({'_type':'article', '_index':'telegraaf', 'id':i, 'date':get_date(i), 'title':get_title(i), 'text':get_text(i), 'link':"http://kranten.kb.nl/view/article/id/" + get_link(i)})
	# helpers.bulk(es,telegraaf)

    HOST = 'http://localhost:9200/'
    es = Elasticsearch(hosts=[HOST])
    query={
        "query": {
            "bool": {
                "must": [
                    { "match": {"text": input("Please input a query: ")}}
                ]
            }
        }
    }
    # Retrieve total amount of search hits, uncomment for unlimited results
    # amount_of_results = es.search(body=query, index='_all')['hits']['total']
    # Or use limited size
    amount_of_results = 100
    query = es.search(body=query, index='telegraaf', size=amount_of_results)
    for result in query['hits']['hits']:
        print(result['_source']['title'] + "\n")
        print(result['_source']['text'] + "\n")
        try:
            print(result['_source']['link'] + "\n")
        except(KeyError):
            print("No link \n")

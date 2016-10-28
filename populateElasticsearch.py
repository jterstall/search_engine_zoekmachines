from elasticsearch import  helpers
from elasticsearch import Elasticsearch
import json
import os


if __name__ == '__main__':
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

    # add bulk to elasticsearch
    json_folder = '/home/neoray/Documents/Zoekmachines/Week 8/telegraaf-json/'

    for filename in os.listdir(json_folder):
        if filename.endswith('.json'):
            print(filename)
            with open(json_folder + filename) as infile:
                helpers.bulk(es, json.load(infile))

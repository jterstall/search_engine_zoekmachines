
    #! /opt/python3/bin/python3.5

from xml.dom.minidom import parse, parseString
import os
import xmltodict, json

# GET DATE FROM ARTICLE
def get_date(i, o):
    return o['pm:KBroot']['pm:root'][i]['pm:meta']['dc:date']['#text']

# GET TITEL FROM ARTICLE
def get_title(i, o):
    try:
        return o['pm:KBroot']['pm:root'][i]['pm:content']['title']['#text']
    except (KeyError):
        return ''

# GET TEXT FROM ARTICLE
def get_text(i, o):
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

def get_link(i, o):
    try:
        return o['pm:KBroot']['pm:root'][i]['pm:content']['@pm:source']
    except (KeyError):
        return ''


if __name__ == '__main__':

    folder = '/home/neoray/Documents/Zoekmachines/Week 8/telegraaf/'
    destination_folder = '/home/neoray/Documents/Zoekmachines/Week 8/telegraaf-json/'

    telegraaf = []
    for fn in os.listdir(folder):
        filename = folder + fn
        if os.path.isfile(filename):
            print(fn)
            with open(filename, 'r', encoding='utf-8') as infile:
                o = xmltodict.parse(infile.read(), xml_attribs=True)
                for i in range(len(o['pm:KBroot']['pm:root'])):
                    telegraaf.append({'_type':'article', '_index':'telegraaf', 'id':i, 'date':get_date(i, o), 'title':get_title(i, o), 'text':get_text(i, o), 'link':get_link(i, o)})
            destination_file_name = destination_folder + fn.replace('.xml', '.json')
            with open(destination_file_name, 'w', encoding='utf-8') as destination:
                json.dump(telegraaf, destination, indent=4)
        telegraaf.clear()
        del o

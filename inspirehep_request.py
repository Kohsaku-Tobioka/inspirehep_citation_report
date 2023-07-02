import datetime
import requests
#import xml.etree.ElementTree as ET
import json


#https://inspirehep.net/api/literature?sort=mostrecent&size=2&page=1&q=de%20%3E%202020%20and%20refersto%3Aauthor%3AK.Tobioka.1

#search_query: de%20%3E%202020%20and%20refersto%3Aauthor%3AK.Tobioka.1

one_week_ago = (datetime.date.today() - datetime.timedelta(days=7)).strftime("%Y-%m-%d")


def create_query_url(search_query, max_results=10, page=1, sort_order='mostrecent', pastdays=7):
    base_url = 'https://inspirehep.net/api/literature?'
    
    query = f'q={search_query}'
    max_results = f'size={max_results}'
    page = f'page={page}'
    sort_order = f'sortOrder={sort_order}'
    #dates='du%20>%202022-06-30'
    day_start=(datetime.date.today() - datetime.timedelta(days=pastdays)).strftime("%Y-%m-%d")
    dates=f'du%20>%20{day_start}'

    
    url = f'{base_url}{query}&{max_results}&{page}&{sort_order}&{dates}'
    return url

def fetch_inspirehep_papers(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch papers: {response.status_code}")
    
testurl=create_query_url("de%20%3E%202020%20and%20refersto%3Aauthor%3AK.Tobioka.1")
print(testurl)


test_result=fetch_inspirehep_papers(testurl)

#print(type(test_result))

json_str = '{"test": 123}'
json_dict = json.loads(test_result)

print(json_dict["hits"]["hits"][0].keys())
print(type(json_dict))
print(type(json_dict["hits"]["hits"][0]['metadata']['authors']))

#To do for output: Extract json output in a favored way, e.g. title of the citing paper, cite papers of mine
#To do for query: (1) limit by updated dates (e.g. last week, month); exclude big papers from my paper list. 
# Implement it in Javascript and appscript. 

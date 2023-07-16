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
json_dict = json.loads(test_result)

# with open('test.json') as f:
#     data = json.load(f)
#json_dict = data 

n_paper=len(json_dict["hits"]["hits"])
print("number of citations are "+str(n_paper) +" in the last 7 days")

for i in range(n_paper):
    title_0th =json_dict["hits"]["hits"][i]['metadata']['titles'][0]['title']
    id_0th =json_dict["hits"]["hits"][i]['id']
    print("")
    print("Title: "+title_0th)
    print("Link: https://inspirehep.net/literature/"+id_0th)
    author_full_names = [author['full_name'] for author in json_dict["hits"]["hits"][i]['metadata']['authors']]
    print(author_full_names)
    

title_0th =json_dict["hits"]["hits"][0]['metadata']['titles'][0]['title']
id_0th =json_dict["hits"]["hits"][0]['id']
print("")
print("Title: "+title_0th)
print("Link: https://inspirehep.net/literature/"+id_0th)
author_full_names = [author['full_name'] for author in json_dict["hits"]["hits"][0]['metadata']['authors']]
print(author_full_names)
print("citing ref")
print(author_full_names)



#To do for output: Extract json output in a favored way, e.g. title of the citing paper, cite papers of mine
#To do for query: (1) limit by updated dates (e.g. last week, month); exclude big papers from my paper list. 
# Implement it in Javascript and appscript. 

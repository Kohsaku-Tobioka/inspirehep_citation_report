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
    
# testurl=create_query_url("de%20%3E%202020%20and%20refersto%3Aauthor%3AK.Tobioka.1")
# print(testurl)

# test_result=fetch_inspirehep_papers(testurl)
# json_dict = json.loads(test_result)

# references = json_dict["hits"]["hits"]
# n_paper=len(references)
# print("number of citations are "+str(n_paper) +" in the last 7 days")

########
# Use local file for test
with open('test.json') as f:
    data = json.load(f)

json_dict = data 
references = json_dict["hits"]["hits"]
########

# 飛岡の論文を引用している論文を調べるコード
# for reference in references:
#     title = reference['metadata']['titles'][0]['title']
#     id = reference['id']
#     print("")
#     print("Title: "+title)
#     print("Link: https://inspirehep.net/literature/"+id)
#     author_full_names = [author['full_name'] for author in reference['metadata']['authors']]
#     print(author_full_names)

# 実際に引用されている飛岡の論文がどれかを調べるコード
for ref in references[1]["metadata"]["references"]:
    # Some reference info does not include "authors" key
    if ref["reference"].get("authors"):
        if "Tobioka, K." in [author["full_name"] for author in ref["reference"]["authors"]]:
            print(ref["raw_refs"][0]["value"])

#To do for output: Extract json output in a favored way, e.g. title of the citing paper, cite papers of mine
#To do for query: (1) limit by updated dates (e.g. last week, month); exclude big papers from my paper list. 
# Implement it in Javascript and appscript. 

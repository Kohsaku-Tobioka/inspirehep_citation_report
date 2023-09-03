import datetime
import json
from urllib.parse import urlencode

import requests



def create_query_url(author_identifier, max_results=10, page=1, sort_order='mostrecent', past_days=7):
    day_start = (datetime.date.today() - datetime.timedelta(days=past_days)).strftime("%Y-%m-%d")
    params = {
        'q': f'de > {day_start} and refersto:author:{author_identifier}',
        'size': max_results,
        'page': page,
        'sort': sort_order
    }
    base_url = 'https://inspirehep.net/api/literature?'
    return f"{base_url}{urlencode(params)}"


def fetch_inspirehep_papers(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def extract_author_names_from_reference(reference):
    return [author["full_name"] for author in reference["reference"]["authors"]]


def readout_cited_paper(reference, name):
    output_myref = []
    for ref in reference["metadata"]["references"]:
        if ref["reference"].get("authors"):
            if name in extract_author_names_from_reference(ref):
                if ref["reference"].get('title'):
                    output_myref.append(f"[{ref['reference']['label']}]")
                    output_myref.append(ref["reference"]["title"]["title"])
                elif ref.get("raw_refs"):
                    output_myref.append(ref["raw_refs"][0]["value"])
                else:
                    output_myref.append("Reference title or raw_refs not found")

    return output_myref


def process_references(references, author_name):
    print(f"Number of citations are {len(references)} in the last 7 days")

    for idx, reference in enumerate(references, start=1):
        title = reference['metadata']['titles'][0]['title']
        id_ = reference['id']
        print(f"\nRef{idx}")
        print(f"Title: {title}")
        print(f"Link: https://inspirehep.net/literature/{id_}")
        
        authors = reference['metadata'].get('authors')
        corporate_author = reference['metadata'].get('corporate_author')

        if authors:
            author_full_names = [author['full_name'] for author in authors]
            print(f"Authors: {author_full_names}")
        elif corporate_author:
            print(f"Corporate_author: {corporate_author}")
        else:
            print('Keys: authors/corporate_author not found')

        cited_refs = readout_cited_paper(reference, author_name)

        if not cited_refs:
            print(f"Cited ref: {author_name} not found. Possibly a big collaboration paper.")
        else:
            print(f"Cited ref: {cited_refs}")


def main():
    author_id = "K.Tobioka.1"
    author_name = "Tobioka, K."
    url = create_query_url(author_id, past_days=70, max_results=100)
    print(url)
    result = fetch_inspirehep_papers(url)
    json_dict = json.loads(result)
    references = json_dict["hits"]["hits"]
    process_references(references, author_name)


if __name__ == "__main__":
    main()

#for improvements
# Nice to unify two inputs to one. e.g. generate Tobioka, K. from K.Tobioka.1  
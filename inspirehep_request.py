import datetime
import requests
import json

#https://inspirehep.net/authors/1198400?ui-citation-summary=true&ui-exclude-self-citations=true
def create_query_url(Author_Identifier, max_results=10, page=1, sort_order='mostrecent', pastdays=7):
    base_url = 'https://inspirehep.net/api/literature?'
    refersto = f"refersto%3Aauthor%3A{Author_Identifier}"
    max_results = f'size={max_results}'
    page = f'page={page}'
    sort_order = f'sort={sort_order}'
    day_start=(datetime.date.today() - datetime.timedelta(days=pastdays)).strftime("%Y-%m-%d")
    dates=f'q=de%20>%20{day_start}'
    url = f'{base_url}{dates}%20and%20{refersto}&{max_results}&{page}&{sort_order}'
    return url

def fetch_inspirehep_papers(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch papers: {response.status_code}")



def readout_citedpaper(reference,Name):
    output_myref =[]
    for ref in reference["metadata"]["references"]:
        if ref["reference"].get("authors"):
            if Name in [author["full_name"] for author in ref["reference"]["authors"]]:
                if ref["reference"].get('title'): 
                    output_myref.append("["+ref["reference"]["label"]+"]")
                    output_myref.append(ref["reference"]["title"]["title"])
                elif ref.get("raw_refs"):
                    output_myref.append(ref["raw_refs"][0]["value"])
                else:
                    output_myref.append("reference-title or raw_refs not found")
                

                
    return output_myref


def process_references(references):
    n_paper=len(references)
    print("Number of citations are "+str(n_paper) +" in the last 7 days")

    i=1
    for reference in references:
        title = reference['metadata']['titles'][0]['title']
        id = reference['id']
        print("\nRef"+str(i))
        print("Title: "+title)
        print("Link: https://inspirehep.net/literature/"+id)
        if reference['metadata'].get('authors'):
            author_full_names = [author['full_name'] for author in reference['metadata']['authors']] #fix next time
            print("Authors: ", author_full_names)
        elif reference['metadata'].get('corporate_author'):
            print("Corporate_author: ", reference['metadata']['corporate_author'])
        else:
            print('keys: authors/corporate_author not found')

        cited_refs = readout_citedpaper(reference,"Tobioka, K.")
        
        if cited_refs ==[]:
            print("Cited ref: ", "Tobioka, K."+" not found. Possibly a big collaboration paper. ")
        else: 
            print("Cited ref: ", cited_refs)
        
        i += 1



def main():
    url= create_query_url("K.Tobioka.1", pastdays=7)
    print(url)
    result = fetch_inspirehep_papers(url)
    json_dict = json.loads(result)
    references = json_dict["hits"]["hits"]
    
    # Save json_dict to a file
    #with open('output.json', 'w') as json_file:
    #    json.dump(json_dict, json_file, indent=4)
    ########
    # Use local file for test
    #with open('test_2023-08-13.json') as f:
    #    data = json.load(f)
    #json_dict = data 
    #references = json_dict["hits"]["hits"]
    ########

    process_references(references)


if __name__ == "__main__":
    main()


#to do
# de%20>%... query order matters? Clean up this part nex time. 
import json
import requests
from bs4 import BeautifulSoup
from serpapi.google_search_results import GoogleSearchResults

params = {
    "api_key": "df34601f332995079e44930e251d419b1a88e45c4f59aa29adb5018f32ae8dd6",
    "engine": "google_scholar",
    "q": "Hydroxychloroquine and Coronavirus",
    "hl": "en",
    "as_ylo": "2019",
    "start": "0"
}

def get_text(url):
    headers = requests.utils.default_headers()
    headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser', from_encoding="iso-8859-1")
    job_elems = soup.find_all("p")
    result = ""
    for job_elem in job_elems:
        if job_elem.string != None:
            result += job_elem.string
    return result

def build_study_object(result):
    return {
        "title": result['title'],
        "link": result['link'],
        "full text": get_text(result['link'])
    }

def get_search_results(params):
    client = GoogleSearchResults(params)
    return client.get_dict()

def read_from_file(filename):
    with open('result.json') as json_file:
        return json.load(json_file)

data = get_search_results(params)
###data = read_from_file('result.json')
output = {}
output['study'] = [] 
for result in data['organic_results']:
    try:
        link = result['link']
        print("...parsing: " + link)
        if ".pdf" not in link:
            output['study'].append(build_study_object(result))
    except KeyError:
        print("ERROR: Skipping result because it doesn't have a link " + result['title'])

outputJSON = open("parsed_results.json", "w")
outputJSON.write(json.dumps(output, indent=4))
outputJSON.close()

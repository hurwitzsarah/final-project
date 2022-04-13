import json
import requests
import matplotlib.pyplot as plt
import os
import sqlite3
import unittest

# def get_data(db_filename):
#     base_url = ""
#     params = {}
#     res = requests.get(base_url, params)
#     data = json.loads(res.text)

#     path = os.path.dirname(os.path.abspath(__file__))
#     conn = sqlite3.connect(path+'/'+db_filename)
#     cur = conn.cursor()

# def setUpDatabase(db_name):
#     path = os.path.dirname(os.path.abspath(__file__))
#     conn = sqlite3.connect(path+'/'+db_name)
#     cur = conn.cursor()
#     return cur, conn

# def readDataFromFile(filename):
#     full_path = os.path.join(os.path.dirname(__file__), filename)
#     f = open(full_path)
#     file_data = f.read()
#     f.close()
#     json_data = json.loads(file_data)
#     return json_data

def read_cache(CACHE_FNAME):
    try:
        source_dir = os.path.dirname(__file__)
        full_path = os.path.join(source_dir, CACHE_FNAME)

        file = open(full_path, 'r')
        content = file.read()
        file.close()

        json_content = json.loads(content)
        return json_content

    except:
        dict = {}
        print("Error reading cache file")
        return dict

def write_cache(CACHE_FNAME, CACHE_DICT):
    json_content = json.dumps(CACHE_DICT)
    with open(CACHE_FNAME, 'w') as outfile:
        outfile.write(json_content)

def create_request_url(page=1, limit=5):
    parms = f"page={str(page)}&limit={str(limit)}" # total pages is 9398, 12 on each page
    url = "https://api.artic.edu/api/v1/artworks?" + parms
    return url

def get_data_with_caching(CACHE_FNAME):
    try:
        request_url = create_request_url()
        dict = read_cache(CACHE_FNAME)

        if request_url in dict:
            #print(f"Using cache for {page}")
            print("using cache")
            return dict[request_url]
        
        else:
            #print(f"Fetching data for {page}")
            print("fetching data")
            r = requests.get(request_url)
            results = json.loads(r.text)
            dict[request_url] = results
            write_cache(CACHE_FNAME, dict)
    except:
        print("Exception")
        return None

# ["title"]
# ["has_not_been_viewed_much"] true
# ["date_end"] 1966
# ["place_of_origin"] united states
# ["artwork_type_title"] drawing and watercolor
# ["artist_title"] name

dir_path = os.path.dirname(os.path.realpath(__file__))
CACHE_FNAME = dir_path + '/' + "chicago_art.json"
get_data_with_caching(CACHE_FNAME)

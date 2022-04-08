import json
import requests
import matplotlib.pyplot as plt
import os
import sqlite3
import unittest

def get_data(db_filename):
    base_url = ""
    params = {}
    res = requests.get(base_url, params)
    data = json.loads(res.text)

    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

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

def readDataFromFile(filename):
    full_path = os.path.join(os.path.dirname(__file__), filename)
    f = open(full_path)
    file_data = f.read()
    f.close()
    json_data = json.loads(file_data)
    return json_data

# def spotifyAPI():
#     base = "https://api.spotify.com."

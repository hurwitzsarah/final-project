import json
import requests
import matplotlib.pyplot as plt
import os
import sqlite3
import unittest

def get_ids(query):
    search_url = "https://collectionapi.metmuseum.org/public/collection/v1/search"
    p = {"q" : query}
    res = requests.get(search_url, params = p)
    data = json.loads(res.text)
    object_ids = data['objectIDs']
    return object_ids


def add_to_database(cur, conn, query, db_filename, start, end):
    cur.execute("CREATE TABLE IF NOT EXISTS met_objects (object_id INTEGER PRIMARY KEY, is_highlight TEXT, title TEXT, artist_name TEXT, artist_enddate INTEGER, medium TEXT)")
    conn.commit()
    object_ids = get_ids(query)
    for id in object_ids[start:end]:
        try:
            object_url = "https://collectionapi.metmuseum.org/public/collection/v1/objects/" + str(id)
            res = requests.get(object_url)
            data = json.loads(res.text)
        except:
            return "Exception"
        for k, v in data.items():
            if v != '':
                object_id = int(data.get("objectID", 0))
                is_highlight = data.get("isHighlight", 0)
                title = data.get("title", 0)
                artist_name = data.get("artistDisplayName", 0)
                artist_enddate = data.get("artistEndDate", 0)
                medium = data.get("medium", 0)
                cur.execute('''INSERT or ignore INTO met_objects (object_id, title, artist_name, artist_enddate, medium, is_highlight) 
                VALUES (?,?,?,?,?,?)''',(object_id, title, artist_name, artist_enddate, medium, is_highlight,))
                conn.commit()
        

def main():
    db_filename = 'met.db'
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()
    add_to_database(cur, conn, "disease",'met.db', 0, 25)
    add_to_database(cur, conn, "disease",'met.db', 25, 50)
    add_to_database(cur, conn, "disease",'met.db', 50, 75)
    add_to_database(cur, conn, "disease",'met.db', 75, 100)

if __name__ == "__main__":
    main()
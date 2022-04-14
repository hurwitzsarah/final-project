import json
import requests
import matplotlib.pyplot as plt
import os
import sqlite3

def create_request_url(page=1, limit=5): # need to mix up data, maybe using range() with jumps
    parms = f"page={str(page)}&limit={str(limit)}" # total pages is 9398, 12 on each page
    url = "https://api.artic.edu/api/v1/artworks?" + parms
    return url

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def createTable(cur, conn):
    cur.execute("""CREATE TABLE IF NOT EXISTS chicago_objects 
                    (object_id INTEGER PRIMARY KEY, title TEXT UNIQUE, artist TEXT, date_end INTEGER, art_type TEXT, origin TEXT, popularity INTEGER)""")
    conn.commit

def get_data(cur, conn):
    request_url = create_request_url()
    r = requests.get(request_url)
    content = json.loads(r.text)
    for d in content[request_url]["data"]: # data is list of 5
        title = d["title"]
        name = d["artist_title"]
        date_complete = d["date_end"]
        art_type = d["artwork_type_title"]
        origin = d["place_of_origin"]
        popularity = d["has_not_been_viewed_much"]
        print((title, name, date_complete, art_type, origin, popularity))
        cur.execute(f"INSERT INTO chicago_objects ({object_id}, {title}, {name}, {date_complete}, {art_type}, {origin}, {popularity}) VALUES (?,?,?,?,?,?)")
    conn.commit()

def main():
    cur, conn = setUpDatabase("chicago_data.db")
    createTable(cur, conn)

# ["title"]
# ["has_not_been_viewed_much"] true
# ["date_end"] 1966
# ["place_of_origin"] united states
# ["artwork_type_title"] drawing and watercolor
# ["artist_title"] name
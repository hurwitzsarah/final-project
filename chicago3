
import json
import requests
import matplotlib.pyplot as plt
import os
import sqlite3
import unittest
import numpy as np

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def get_ids(cur, conn, query, limit = 100):
    search_url = "https://api.artic.edu/api/v1/artworks/search?"
    p = {"q" : query, "limit" : limit}
    res = requests.get(search_url, params = p)
    data = json.loads(res.text)

    object_ids = []
    for item in data['data']:
        object_ids.append(item['id'])
    cur.execute("CREATE TABLE IF NOT EXISTS object_ids (id INTEGER PRIMARY KEY, chicago_id INTEGER)")
    for i in range(len(object_ids)):
        cur.execute("INSERT OR IGNORE INTO object_ids (id,chicago_id) VALUES (?,?)",(i,object_ids[i]))
    conn.commit()
    return object_ids

def add_to_database(cur, conn, query, db_filename, start, end):
    cur.execute("CREATE TABLE IF NOT EXISTS chicago_objects (object_id INTEGER PRIMARY KEY, title TEXT, artist_name TEXT, object_enddate INTEGER, medium TEXT, origin TEXT, popularity TEXT)")
    conn.commit()
    
    object_ids = get_ids(cur, conn, query)
    for id in object_ids[start:end]:
        try:
            object_url = "https://api.artic.edu/api/v1/artworks?ids=" + str(id) 
            res = requests.get(object_url)
            data = json.loads(res.text)
            art_data = data.get("data", 0)
        
            for item in art_data:
                if "id" in item:
                    object_id = int(item.get("id", 0))
                    title = item.get("title", 0)
                    name = item.get("artist_title", 0)
                    date_complete = int(item.get("date_end", 0))
                    art_type = item.get("artwork_type_title", 0)
                    origin = item.get("place_of_origin", 0)
                    popularity = item.get("has_not_been_viewed_much", 0)
                    print((title, name, date_complete, art_type, origin, popularity))
                    cur.execute('''INSERT or ignore INTO chicago_objects (object_id, title, artist_name, object_enddate, medium, origin, popularity) 
                                VALUES (?,?,?,?,?,?,?)''',(object_id, title, name, date_complete, art_type, origin, popularity))
                conn.commit()

        except:
            print("error in add to database")

def no_repeats(cur, conn, query):

    cur.execute("CREATE TABLE IF NOT EXISTS chicago_no_repeats (object_id INTEGER PRIMARY KEY, title TEXT, artist_name TEXT, object_enddate INTEGER, medium TEXT, origin TEXT, popularity TEXT)")
    conn.commit()

    object_ids = get_ids(cur, conn, query)
    for id in object_ids:
        try:
            object_url = "https://api.artic.edu/api/v1/artworks?ids=" + str(id) 
            res = requests.get(object_url)
            data = json.loads(res.text)
            art_data = data.get("data", 0)

            for item in art_data:
                if "id" in item:
                    name = item.get("artist_title", 0)
                    art_type = item.get("artwork_type_title", 0)
                    origin = item.get("place_of_origin", 0)
                    print((name, art_type, origin))

            cur.execute("SELECT name_id FROM chicago_names WHERE artist_name = ?", (name,)) # name
            name_id = int(cur.fetchone()[0])
            cur.execute("UPDATE chicago_objects SET artist_name = ? WHERE artist_name = ?", (name_id, name))

            cur.execute("SELECT medium_id FROM chicago_mediums WHERE medium_type = ?", (art_type,)) # medium
            medium_id = int(cur.fetchone()[0])
            cur.execute("UPDATE chicago_objects SET medium = ? WHERE medium = ?", (medium_id, art_type))

            cur.execute("SELECT origin_id FROM chicago_origins WHERE origin_type = ?", (origin,)) # origin
            origin_id = int(cur.fetchone()[0])
            cur.execute("UPDATE chicago_objects SET origin = ? WHERE origin = ?", (origin_id, origin))

        except:
            print("error in no repeats")

    #UPDATE Users SET name='Charles' WHERE email='csev@umich.edu'                 

    conn.commit()


def create_name_table(cur, conn):
    cur.execute('''SELECT chicago_objects.artist_name FROM chicago_objects''')
    conn.commit()
    names = cur.fetchall()
    no_repeats_names = []
    for tup in names:
        name = tup[0]
        if name not in no_repeats_names:
            no_repeats_names.append(name)

    cur.execute("CREATE TABLE IF NOT EXISTS chicago_names (name_id INTEGER PRIMARY KEY, artist_name TEXT)")
    for i in range(len(no_repeats_names)):
        cur.execute('''INSERT or ignore INTO chicago_names (name_id, artist_name) VALUES (?,?)''',(i, no_repeats_names[i]))
    conn.commit()

def create_medium_table(cur, conn):
    cur.execute('''SELECT chicago_objects.medium FROM chicago_objects''')
    conn.commit()
    mediums = cur.fetchall()
    no_repeats_mediums = []
    for tup in mediums:
        medium = tup[0]
        if medium not in no_repeats_mediums:
            no_repeats_mediums.append(medium)

    cur.execute("CREATE TABLE IF NOT EXISTS chicago_mediums (medium_id INTEGER PRIMARY KEY, medium_type TEXT)")
    for i in range(len(no_repeats_mediums)):
        cur.execute('''INSERT or ignore INTO chicago_mediums (medium_id, medium_type) VALUES (?,?)''',(i, no_repeats_mediums[i]))
    conn.commit()

def create_origin_table(cur, conn):
    cur.execute('''SELECT chicago_objects.origin FROM chicago_objects''')
    conn.commit()
    origins = cur.fetchall()
    no_repeats_origins = []
    for tup in origins:
        origin = tup[0]
        if origin not in no_repeats_origins:
            no_repeats_origins.append(origin)

    cur.execute("CREATE TABLE IF NOT EXISTS chicago_origins (origin_id INTEGER PRIMARY KEY, origin_type TEXT)")
    for i in range(len(no_repeats_origins)):
        cur.execute('''INSERT or ignore INTO chicago_origins (origin_id, origin_type) VALUES (?,?)''',(i, no_repeats_origins[i]))
    conn.commit()

def main():
    cur, conn = setUpDatabase("chicago_data4.db")
    add_to_database(cur, conn, "activism","chicago_data4.db", 0, 25)
    # add_to_database(cur, conn, "activism","chicago_data4.db", 25, 50)
    # add_to_database(cur, conn, "activism","chicago_data4.db", 50, 75)
    # add_to_database(cur, conn, "activism","chicago_data4.db", 75, 101) # one has exception
    create_name_table(cur, conn)
    create_medium_table(cur, conn)
    create_origin_table(cur, conn)
    no_repeats(cur, conn, "activism")


if __name__ == "__main__":
    main()
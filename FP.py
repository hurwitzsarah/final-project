import json
import requests
import matplotlib.pyplot as plt
import os
import sqlite3
import unittest
import numpy as np

def get_ids(cur, conn, query):
    search_url = "https://collectionapi.metmuseum.org/public/collection/v1/search"
    p = {"q" : query}
    res = requests.get(search_url, params = p)
    data = json.loads(res.text)
    object_ids = data['objectIDs']
    cur.execute("CREATE TABLE IF NOT EXISTS object_ids (id INTEGER PRIMARY KEY, met_id INTEGER)")
    for i in range(len(object_ids)):
        cur.execute("INSERT OR IGNORE INTO object_ids (id,met_id) VALUES (?,?)",(i,object_ids[i]))
    conn.commit()
    return object_ids


def add_to_database(cur, conn, query, db_filename, start, end):
    cur.execute("CREATE TABLE IF NOT EXISTS met_objects (object_id INTEGER PRIMARY KEY, is_highlight TEXT, title TEXT, artist_name TEXT, object_enddate INTEGER, objectname TEXT, medium TEXT)")
    conn.commit()
    object_ids = get_ids(cur, conn, query)
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
                cur.execute("SELECT id FROM object_ids WHERE met_id = ?", (object_id,))
                id = int(cur.fetchone()[0])
                is_highlight = data.get("isHighlight", 0)
                title = data.get("title", 0)
                artist_name = data.get("artistDisplayName", 0)
                object_enddate = data.get("objectEndDate", 0)
                objectname = data.get("objectName", 0)
                medium = data.get("medium", 0)
                cur.execute('''INSERT or ignore INTO met_objects (object_id, title, artist_name, object_enddate, objectname, medium, is_highlight) 
                VALUES (?,?,?,?,?,?,?)''',(id, title, artist_name, object_enddate, objectname, medium, is_highlight))
            conn.commit()
        
def create_name_table(cur, conn):
    cur.execute('''SELECT met_objects.objectname FROM met_objects''')
    conn.commit()
    names = cur.fetchall()
    no_repeats_names = []
    for tup in names:
        name = tup[0]
        if name not in no_repeats_names:
            no_repeats_names.append(name)

    cur.execute("CREATE TABLE IF NOT EXISTS met_names (name_id INTEGER PRIMARY KEY, objectname TEXT)")
    for i in range(len(no_repeats_names)):
        cur.execute('''INSERT or ignore INTO met_names (name_id, objectname) VALUES (?,?)''',(i, no_repeats_names[i]))


def dates_and_highlights(cur, conn, file): 
    cur.execute('''SELECT met_objects.object_enddate, met_objects.is_highlight FROM met_objects JOIN object_ids 
    ON met_objects.object_id = object_ids.id WHERE met_objects.is_highlight = ?''', (1,))
    conn.commit()
    lst = cur.fetchall()
    highlight_counts = {}
    count = 0
    total = 0
    for tup in lst:
        year = tup[0]
        total += year
        count += 1
        highlight_counts[year] = highlight_counts.get(year, 0) + 1
    avg = int(total/count)

    f = open(file, "w")
    f.write("The average year with the most highlighted 'activism' pieces was " + str(avg) + "\n")
    f.write("The total number of highlighted 'activism' items in this sample of 100 'activism' items was " + str(count) + "\n")
    f.close()

    years = list(highlight_counts.keys())
    counts = list(highlight_counts.values())
    x1 = np.array(years)
    y1 = np.array(counts)
    plt.scatter(x1, y1)
    plt.xlabel("Year")
    plt.ylabel("Number of Highlighted Pieces")
    plt.title("Highlighted Pieces By Year at the Met")
    plt.show()

def names_and_highlights(cur, conn, file):
    #average year of when most activist pieces were created in a sample of 100 items at the met
    #count of highlights and which years had the most highlighted pieces 
    #make one more based on my data for EC
    cur.execute('''SELECT met_names.name_id, met_objects.is_highlight FROM met_objects JOIN met_names 
    ON met_objects.objectname = met_names.objectname WHERE met_objects.is_highlight = ?''', (1,))
    conn.commit()
    lst = cur.fetchall()
    object_counts = {}
    for tup in lst:
        name = tup[0]
        object_counts[name] = object_counts.get(name, 0) + 1
    sorteddic = sorted(object_counts, key = lambda k: object_counts[k], reverse = True)
    most = sorteddic[0]
    f = open(file, "a")
    f.write("The object type id with the most highlighted 'activism' pieces was " + str(most) + ", with " + str(object_counts[most]) + " higlighted pieces.\n")
    f.close()

    names = list(object_counts.keys())
    names_counts = list(object_counts.values())

    x2 = np.array(names)
    y2 = np.array(names_counts)
    plt.bar(x2, y2, color='pink')
    plt.xlabel("Object Type Ids")
    plt.xticks(list(range(0, 49, 2)))
    plt.ylabel("Number of Highlighted Pieces")
    plt.title("Highlighted Pieces By Object Type Id at the Met")
    plt.show()

def extra_credit_viz(cur, conn, file):
    cur.execute('''SELECT met_names.name_id, met_objects.medium FROM met_objects JOIN met_names 
    ON met_objects.objectname = met_names.objectname WHERE met_names.name_id = ?''', (3,))
    conn.commit()
    lst = cur.fetchall()
    medium_counts = {}
    for tup in lst:
        medium = tup[1]
        medium_counts[medium] = medium_counts.get(medium, 0) + 1
    sorteddic = sorted(medium_counts, key = lambda k: medium_counts[k], reverse = True)
    most = sorteddic[0]
    f = open(file, "a")
    f.write("Of the object type with the most highlighted 'activism' pieces, the most used medium was " + most + ".\n")
    f.close()

    y = np.array(list(medium_counts.values()))
    mediums = list(medium_counts.keys())
    mycolors = ["Plum", "PaleVioletRed", "PowderBlue", "OliveDrab", "LightCoral", "DarkSeaGreen", "DarkCyan", "CornflowerBlue", "Thistle", "RosyBrown", "PeachPuff", "LightSlateGrey", "LemonChiffon", "Lavender", "LightPink"]
    plt.pie(y, labels = mediums, colors = mycolors) 
    plt.title("'Activist' Paintings By Medium at the Met")
    plt.show()



def main():
    db_filename = 'art.db'
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()
    add_to_database(cur, conn, "activism",'art.db', 0, 25)
    add_to_database(cur, conn, "activism",'art.db', 25, 50)
    add_to_database(cur, conn, "activism",'art.db', 50, 75)
    add_to_database(cur, conn, "activism",'art.db', 75, 100)
    create_name_table(cur, conn)
    dates_and_highlights(cur, conn, 'calculations.txt')
    names_and_highlights(cur, conn, 'calculations.txt')
    extra_credit_viz(cur, conn, 'calculations.txt')

if __name__ == "__main__":
    main()
    

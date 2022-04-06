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


def visualize_results(db_filename):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()
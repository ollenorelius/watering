from app import app
from flask import render_template

import datetime
import os
import json

from app.SqlConnection import SqlConnection



DATA_PATH = '/home/pi/watering/plant_data/'

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/plant_data', methods=['GET'])
def get_plant_data():
    files = os.listdir(DATA_PATH)
    files.sort(key = lambda x: datetime.datetime.strptime(x, '%Y-%m-%d.txt'))
    newest_file_name = files[-1]
    penultimate = files[-2]
    f = open(DATA_PATH+newest_file_name, 'r')
    f2 = open(DATA_PATH+penultimate, 'r')
    data=[]
    for l in f2:
        data_point = [float(x) for x in l.strip().split('\t')]
        data.append(data_point)
    for l in f:
        data_point = [float(x) for x in l.strip().split('\t')]
        data.append(data_point)

    return json.dumps(data)

@app.route('/plant_data/<name>', methods=['GET'])
def get_plant_data_sql(name):
    sql = SqlConnection("../database.sqlite3")
    raw = sql.get_data_from_last_days(name, 2)
    return json.dumps([[x["timestamp"], x["dryness"]] for x in raw])

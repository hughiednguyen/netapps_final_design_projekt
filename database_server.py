#!/usr/bin/env python3

from pymongo import MongoClient
from flask import Flask, request, render_template, jsonify
from datetime import datetime
import time

# Instantiating a flask app
app = Flask(__name__)

# Instantiating mongodb
client = MongoClient()
db = client.test
coll = db["team7"]

# Defining ranges
LOW = 2
MEDIUM = 8
HIGH = 21


# The post function to get the dat
@app.route("/getData")
def get_data():
    latest_data = 0
    _max = -1
    # Finding the latest post in the database
    for post in coll.find():
        date = post['dt']

        # Get the date formatted for comparisons
        #print(coll.find().sort([('dt', -1)]).limit(1))
        cursor = date.year + date.month + date.day + date.hour + date.minute + date.second + date.microsecond
        
        if(cursor > _max):
            latest_data = post['count']
            _max = cursor
            latest_date = date
    print(_max)
    # Putting the recent post result into ranges: low, medium, high
    if latest_data <= LOW:
        return "low"
    elif latest_data <= MEDIUM:
        return "medium"
    else:
        return "high"


# Hello!
@app.route("/hello")
def hello():
    return "Hello World!"


# Main
if __name__ == "__main__":
    # Running the flask app
    app.run(host='0.0.0.0', port=1900)
    

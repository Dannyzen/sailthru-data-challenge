from flask import Flask, request, session, render_template, jsonify, redirect, url_for
from flask.ext.pymongo import PyMongo
from pymongo import MongoClient
import requests
import random
import urllib2

"""
This file contains all the functions and routes for our demo app.
"""
app = Flask(__name__)
mongo = PyMongo(app)
# comment out when you're done testing
app.debug = True
client = MongoClient('localhost', 27017)
db = client.test
collection = db.hackathon

numDocuments = collection.find({'geo': {'$exists':'true'}, 'browser':{'$exists':'true'}}).count()
"""
This is the function that will be called when users
visit the home page.

app.route is a function decorator. It takes a URI as an argument, and
whenever a user requests that url, the function it decorates will get called.
In this case, if your app was at www.myapp.com, then someone visiting
www.myapp.com or www.myapp.com/index.html would cause the flask app to call
the index() function. For more information about the app.route decorator
check out http://flask.pocoo.org/docs/quickstart/#routing.
"""
@app.route('/')
@app.route('/index.html')
def index():
#    mongoData = mongo.db.hackathon.find({'browser.Chrome':2})
#    asdf = collection.find_one({'browser.Chrome':3})
    numBrowsers = 0
    while numBrowsers < 2:
        asdf = collection.find({'geo': {'$exists':'true'}, 'browser':{'$exists':'true'}, 'geo.city':{'$exists':'true'}}).limit(-1).skip(random.randint(0,numDocuments)).next()
        numBrowsers = len(list(asdf['browser']))

    data = {'browsers': '\t VS. \t'.join(asdf['browser'].keys()[:2]),
            'browser1': asdf['browser'].keys()[0],
            'browser2': asdf['browser'].keys()[1],
            'browser1Score': asdf['browser'][asdf['browser'].keys()[0]],
            'browser2Score': asdf['browser'][asdf['browser'].keys()[1]],
            'stuff': asdf,
            'location': list(asdf['geo']['city'])[0],
            'consumer_id': 123,
            'access_token': "123",
            'signed_in': True}
    return render_template('index.html', data=data)


if __name__ == '__main__':
    app.run()

@app.route('/enter', methods=['POST'])
def enter():
    if request.method == 'POST':
        if request.data == "leftButton":
            urllib2.urlopen("https://agent.electricimp.com/GVdqUmVCn7W8?enter=left")
        elif request.data == "rightButton":
            urllib2.urlopen("https://agent.electricimp.com/GVdqUmVCn7W8?enter=right")

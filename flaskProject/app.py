"""
Tasks:
1. Connect Database
2. Create Queries for movies
3. Create Queries for actors
4. Get "hello world!"
5. Transition to CRUD
6.
"""
#import pymongo
#from pymongo import MongoClient

from flask import Flask, render_template, request, url_for, redirect

from bson.json_util import dumps

from bson.objectid import ObjectId

from flask import jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)
# pip install Flask pymongo
#client = MongoClient('localhost', 27017, username='movielover99', password='movielover4life')
#code below might be good
#client = pymongo.MongoClient("mongodb+srv://root:password@cluster0.d8iz1bd.mongodb.net/?retryWrites=true&w=majority")
#db = client.flask_db
#todos = db.todos

app.config['MONGO_URI'] = "mongodb+srv://movielover99:movielover4life@movies.agbzkrd.mongodb.net/movie"

mongo = PyMongo(app)


PORT = 8080
HOST = "127.0.0.1"

movie_data = [{},{},{}]

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.get("/api/v1/movies")
def get_movies():
    return jsonify("FINISH THIS METHOD!")

""" THE METHOD BELOW IS NOT READY"""
@app.post("/api/v1/movies")
def add_movie():
    if request.is_json:
        response = request.get_json()
        if 'title' in response and 'year' in response and 'director' in response:
            #response["id"] = _find_next_id(user_data)
            #user_data.append(response)
            id = mongo.db.movie.insert_one({'title':response['title'],'year':response['year'],'director':response['director']})
            return response, 201
        else:
            return {"error": "Malformed request. Missing required user fields"}, 400
    return {"error": "Request must be JSON"}, 415

# @app.route('/', methods=('GET', 'POST'))
# def index():
#     return render_template('index.html')

if __name__ == '__main__':
    app.run()


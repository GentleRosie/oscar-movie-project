"""
Tasks:
1. Connect Database
2. Create Queries for movies
3. Create Queries for actors
4. Get "hello world!"
5. Transition to CRUD
6.
"""
import json
import string
from urllib.request import urlopen
import requests
from flask import Flask, render_template, request, url_for, redirect
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify
from flask_pymongo import PyMongo
from movie import Movie

app = Flask(__name__)
# pip install Flask pymongo
# client = MongoClient('localhost', 27017, username='movielover99', password='movielover4life')
# code below might be good
# client = pymongo.MongoClient("mongodb+srv://root:password@cluster0.d8iz1bd.mongodb.net/?retryWrites=true&w=majority")
# db = client.flask_db
# todos = db.todos

# app.config['MONGO_URI'] = "mongodb+srv://movielover99:movielover4life@movies.agbzkrd.mongodb.net/movie"
app.config['MONGO_URI'] = "mongodb+srv://root:password@cluster0.d8iz1bd.mongodb.net/?retryWrites=true&w=majority"

mongo = PyMongo(app)

PORT = 8080
HOST = "127.0.0.1"

movie_data = [{}, {}, {}]


# API = 'https://www.omdbapi.com/?apikey='
# API_key = '8066aa78'


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


"""
    def __init__(self, key: str):
        self.API = f'{self.API}{key}&'

    def search(self, title: str):
        title = title.replace(' ', '+')
        self.API = f'{self.API}t={title}'
        return json.loads(urlopen(self.API).read())
"""


@app.get("/api/v1/movies/<string:movie_name>")
def get_movies(movie_name: string):     #import string to get the string from the api
    movie = Movie('8066aa78')           # goes through movie api to get movie string (in HEAP)
    data = movie.search(movie_name)
    if len(data) == 2:
        return {"error": f"No data found for movie {movie_name}"}, 404
    return data


@app.post("/api/v1/movies")
def add_movie():
    if request.is_json:
        response = request.get_json()
        if 'title' in response and 'year' in response and 'director' in response:
            # response["id"] = _find_next_id(user_data)
            # user_data.append(response)
            id = mongo.db.movie.insert_one(
                {'title': response['title'], 'year': response['year'], 'director': response['director']})
            return response, 201
        else:
            return {"error": "Malformed request. Missing required user fields"}, 400
    return {"error": "Request must be JSON"}, 415


if __name__ == '__main__':
    app.run()

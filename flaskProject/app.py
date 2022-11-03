"""
Tasks:
1. Connect Database
2. Create Queries for movies
3. Create Queries for actors
4. Get "hello world!"
5. Transition to CRUD
6.
"""
import pymongo
from pymongo import MongoClient
from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)
# pip install Flask pymongo
# client = MongoClient('localhost', 27017, username='username', password='password')
client = pymongo.MongoClient("mongodb+srv://root:password@cluster0.d8iz1bd.mongodb.net/?retryWrites=true&w=majority")
db = client.flask_db
todos = db.todos

PORT = 8080
HOST = "127.0.0.1"

movie_data = [{},{},{}]

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.get("/api/v1/movies")
def get_movies():
    return None
# @app.route('/', methods=('GET', 'POST'))
# def index():
#     return render_template('index.html')

if __name__ == '__main__':
    app.run()


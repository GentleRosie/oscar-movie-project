import json
import string
from flask import Flask, request
from flask_pymongo import PyMongo
from movie import Movie
from datapackage import Package

app = Flask(__name__)

app.config['MONGO_URI'] = "mongodb+srv://root:password@cluster0.d8iz1bd.mongodb.net/?retryWrites=true&w=majority"
mongo = PyMongo(app)

PORT = 8080
HOST = "127.0.0.1"

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.get("/api/v1/movies")
def get_movies():  # import string to get the string from the api
    arg1 = request.args['arg1']  # use ?arg1= to make request
    movie = Movie('8066aa78')  # goes through movie api to get movie string (in HEAP)
    data = movie.search(arg1)
    if len(data) == 2:
        return {"error": f"No data found for that movie"}, 404
    return data

@app.get("/api/v1/movies/<int:year>")
def get_academy_awards_nominees(year: int):
    package = Package('https://datahub.io/rufuspollock/oscars-nominees-and-winners/datapackage.json')
    for resource in package.resources:
        if resource.descriptor['datahub']['type'] == 'derived/csv':
            return resource.read()

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

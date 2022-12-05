# from math import floor
import json

from flask import Flask  # , render_template
from flask import request
from MovieAPI import MovieAPI
from json import load
# from flask import jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
# import subprocess as sp


class MyEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return super(MyEncoder, self).default(o)


app = Flask(__name__)   # , template_folder='client/public') look into what template_folder does
app.config['MONGO_URI'] = 'mongodb://localhost:27017/MovieProject'
app.json_encoder = MyEncoder
mongo = PyMongo(app)
academy_awards_file = open('new_data_json.json', encoding='utf-8')
academy_awards_data = load(academy_awards_file)
movie_api = MovieAPI('https://www.omdbapi.com/?apikey=', '8066aa78')


# @app.route('/', methods=('GET', 'POST'))
# def index():
#     movie_list = mongo.db.movies.find()
#     return render_template('index.html', list=movie_list)


# @app.get("/api/v2/movies")
# def get_all_movies():
#     result = []
#     for movie in db.find():
#         result.append({'title' : movie['title'], 'year' : movie['year'], 'director' : movie['director']})
#     return jsonify({'result' : result})
# method was used in conjunction with React JS
# @app.route('/add', methods = ['POST'])
# def add_user():
#     _json = request.json
#     _name = _json['name']
#     _email = _json['email']
#     _password = _json['password']
#
#     if _name and _email and _password and request.method == 'POST':
#         mongo.db.movies.insert_one({'name': _name, 'email': _email, 'password': _password})
#         response = jsonify('User added successfully!')
#         response.status_code = 200
#         return response
#     else:
#         return not_found()
# @app.errorhandler(404)
# def not_found(error=None):
#     message = {
#         'status': 404,
#         'message': 'Not Found' + request.url
#     }
#     response = jsonify(message)
#
#
# @app.route('/names', methods = ['GET'])
# def default():
#     return {"names": ["Alan", "Edgar", "Poe"]}


@app.get("/api/v1/omdb/movies")
def get_movie_data():
    movie_title = request.args['title']
    movie_data = movie_api.search_movie_title(movie_title)
    if len(movie_data) == 2:
        return {"error": f"No data found for movie {movie_title}"}, 404
    return {'director': movie_data['Director'], 'language': movie_data['Language'],
            'title': movie_data['Title'], 'year': movie_data['Year']}


@app.get("/api/v1/oscars/movies/<int:year>")
def get_oscar_nominees_by_year(year: int):
    if year < 1927 or year > 2019:
        return {"error": f"No data found for year {year}"}, 404

    winners_list = []
    nominees_list = []

    for award in academy_awards_data:
        if award['year'] == year:
            if award['winner']:
                winners_list.append(award)
            else:
                nominees_list.append(award)

    return {"winners": winners_list, "nominees": nominees_list}


def _helper(category: str, year: int, categories: list) -> dict:
    winners_list = []
    for award in academy_awards_data:
        if award['year'] == year and award['winner']:
            for category in categories:
                if award['category'] == category:
                    winners_list.append(award)
                    break
    winner_movie_title = winners_list[0]['film']
    winner_movie_year = winners_list[0]['year']
    print(f'{winner_movie_title}, {winner_movie_year}')
    movie_data = movie_api.search_movie_title_and_year(winner_movie_title, winner_movie_year)
    mongo.db.movies.insert_one({f'{category} of year {year}': movie_data})
    return {f'{category} of year {year}': movie_data}


@app.get("/api/v1/oscars/movies/best_picture/<int:year>")
def get_oscar_best_picture_winners_by_year(year: int):
    if year < 1927 or year > 2019:
        return {"error": f"No data found for year {year}"}, 404

    return _helper('Best Picture', year, ['OUTSTANDING PICTURE', 'OUTSTANDING PRODUCTION',
                                          'OUTSTANDING MOTION PICTURE', 'BEST MOTION PICTURE', 'BEST PICTURE'])


@app.get("/api/v1/oscars/movies/best_actor/<int:year>")
def get_oscar_best_actor_winners_by_year(year: int):
    if year < 1927 or year > 2019:
        return {"error": f"No data found for year {year}"}, 404

    return _helper('Best Actor', year, ['ACTOR', 'ACTOR IN A LEADING ROLE', 'ACTRESS IN A LEADING ROLE', 'ACTRESS'])


# @app.get("/api/v1/oscars/movies/recommendation") WORKING ON IMPLEMENTATION
# def get_movie_recommendation():
#     year_frequency = [0] * 10
#     index = None
#     test_data = [1969, 2019, 1981, 1974, 2016, 1989, 1946]
#     for year in test_data:
#         if test_data < 2000:
#             index = floor((year % 100) / 10) * 10
#         else:
#             index = 9 + floor((year % 100) / 10) * 10
#     # query database based on highest years searched then return movie


@app.get("/api/v1/user/movies")
def get_all_movies():
    response = []
    for movie_data in mongo.db.movies.find():
        response.append({'director': movie_data['director'], 'language': movie_data['language'],
                         'title': movie_data['title'], 'year': movie_data['year']})
    return {'Movies': response}


@app.get("/api/v1/user/movies/<string:movie_title>")
def get_one_movie(movie_title: str):
    movie_data = mongo.db.movies.find_one({'title': movie_title})
    response = {'director': movie_data['director'], 'language': movie_data['language'],
                'title': movie_data['title'], 'year': movie_data['year']}
    return {'Movie': response}


@app.post("/api/v1/user/movies")
def add_one_movie():
    if not request.is_json:
        return {'Error': 'Request must be JSON'}, 415

    if not ('director' in request.json and 'language' in request.json and
            'title' in request.json and 'year' in request.json):
        return {'Error': 'Malformed request. Missing required movie fields'}, 400

    response = {'director': request.json.get('director'), 'language': request.json.get('language'),
                'title': request.json.get('title'), 'year': request.json.get('year')}
    mongo.db.movies.insert_one(response)
    return response, 201


@app.put("/api/v1/user/movies/<string:movie_title>")
def edit_one_movie(movie_title: str):
    movie_format = {'title': movie_title}
    movie_data = mongo.db.movies.find_one(movie_format)

    if movie_data is None:
        return {'Error': f'No data found for movie {movie_title}'}, 404

    if not request.is_json:
        return {'Error': 'Request must be JSON'}, 415

    if not ('director' in request.json or 'language' in request.json or
            'title' in request.json or 'year' in request.json):
        return {'Error': 'Malformed request. Missing required movie fields'}, 400

    response = {'title': request.json.get('title') or movie_data['title'],
                'director': request.json.get('director') or movie_data['director'],
                'language': request.json.get('language') or movie_data['language'],
                'year': request.json.get('year') or movie_data['year']}
    mongo.db.movies.update_one(movie_format, {'$set': response})
    return response, 200


@app.delete("/api/v1/user/movies/<string:movie_title>")
def delete_one_movie(movie_title: str):
    movie_format = {"title": movie_title}
    movie_data = mongo.db.movies.find_one(movie_format)

    if movie_data is None:
        return {'Error': f'No data found for movie {movie_title}'}, 404

    mongo.db.movies.delete_one(movie_format)
    return {'director': movie_data['director'], 'language': movie_data['language'],
            'title': movie_data['title'], 'year': movie_data['year']}, 200


if __name__ == '__main__':
    app.run()

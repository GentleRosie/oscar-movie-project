from flask import Flask, jsonify  # , render_template
from flask import request
# from flask import jsonify
# import subprocess as sp
from pre_initializer import movie_api, academy_awards_data
from initializer import app, mongo
from flask import render_template

from utility import dictionary_builder, get_winners_and_nominees_of_year_dict, \
    get_category_of_winners_by_year, get_omdb_list_of_movies_by_title_and_year, rated_recommendation_list, \
    ratings_recommendation_list, genre_recommendation_list

genre_list = []
ratings_list = []
rated_list = []


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
FLASK_DEBUG = 1


@app.route('/', methods=['GET', 'POST'])
def index():
    movie_list = []

    for movies in mongo.db.omdb.find():
        movies.pop('_id')
        movie_list.append(movies)

    return render_template('table.html', list=movie_list)


# incorporate into recommendation functions
@app.get('/api/v1/omdb/movies')
def get_omdb_movie_data():
    movie_title = request.args['title']
    movie_data = movie_api.search_movie_title(movie_title)

    if len(movie_data) == 2:
        return dictionary_builder(['error'], [f'No data found for movie {movie_title}']), 404

    rated_recommendation_list(movie_data)
    ratings_recommendation_list(movie_data)
    genre_recommendation_list(movie_data)

    response = dictionary_builder(['director', 'language', 'title', 'year'],
                                  [movie_data['Director'], movie_data['Language'],
                                   movie_data['Title'], movie_data['Year']])
    mongo.db.omdb.insert_one(response)
    response.pop('_id')
    return response, 200


@app.get('/api/v1/oscars/<int:year>')
def get_oscar_nominees_by_year(year: int):
    if year < 1927 or year > 2019:
        return dictionary_builder(['error'], [f'No data found for year {year}']), 404

    response = get_winners_and_nominees_of_year_dict(academy_awards_data, year)
    response['year'] = year
    mongo.db.oscars.insert_one(response)
    response.pop('_id')
    return response, 200


# incorporate into recommendation functions
@app.get('/api/v1/oscars/best_picture/<int:year>')
def get_oscar_best_picture_winners_by_year(year: int):
    if year < 1927 or year > 2019:
        return dictionary_builder(['error'], [f'No data found for year {year}']), 404

    response = get_category_of_winners_by_year(academy_awards_data, year, 'Best Picture',
                                               ['OUTSTANDING PICTURE', 'OUTSTANDING PRODUCTION',
                                                'OUTSTANDING MOTION PICTURE', 'BEST MOTION PICTURE', 'BEST PICTURE'])
    response['omdb'] = response['omdb'] = get_omdb_list_of_movies_by_title_and_year(response['winners'])
    mongo.db.oscars.insert_one(response)
    response.pop('_id')
    return response, 200


# incorporate into recommendation functions
@app.get('/api/v1/oscars/best_actor/<int:year>')
def get_oscar_best_actor_winners_by_year(year: int):
    if year < 1927 or year > 2019:
        return dictionary_builder(['error'], [f'No data found for year {year}']), 404

    response = get_category_of_winners_by_year(academy_awards_data, year, 'Best Actors',
                                               ['ACTOR', 'ACTOR IN A LEADING ROLE',
                                                'ACTRESS IN A LEADING ROLE', 'ACTRESS'])
    response['omdb'] = get_omdb_list_of_movies_by_title_and_year(response['winners'])
    mongo.db.oscars.insert_one(response)
    response.pop('_id')
    return response, 200


# @app.get('/api/v1/oscars/recommendation') WORKING ON IMPLEMENTATION
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


@app.get('/api/v1/user/movies')
def get_all_movies():
    response = []
    for movie_data in mongo.db.user.find():
        movie_data.pop('_id')
        response.append(movie_data)
    return dictionary_builder(['movies'], [response])


# incorporate into recommendation functions
@app.get('/api/v1/user/movies/<string:movie_title>')
def get_one_movie(movie_title: str):
    movie_data = mongo.db.user.find_one(dictionary_builder(['title'], [movie_title]))

    if movie_data is None:
        return {'error': f'No data found for movie {movie_title}'}, 404

    movie_data.pop('_id')
    return movie_data


@app.post('/api/v1/user/movies')
def add_one_movie():
    if not request.is_json:
        return {'error': 'Request must be JSON'}, 415

    if not ('director' in request.json and 'language' in request.json and
            'title' in request.json and 'year' in request.json):
        return {'error': 'Malformed request. Missing required movie fields'}, 400

    response = dictionary_builder(['director', 'language', 'title', 'year'],
                                  [request.json.get('director'), request.json.get('language'),
                                   request.json.get('title'), request.json.get('year')])
    mongo.db.user.insert_one(response)
    response.pop('_id')
    return response, 201


@app.put('/api/v1/user/movies/<string:movie_title>')
def edit_one_movie(movie_title: str):
    movie_format = dictionary_builder(['title'], [movie_title]) # {'title': movie_title}
    movie_data = mongo.db.user.find_one(movie_format)

    if movie_data is None:
        return {'error': f'No data found for movie {movie_title}'}, 404

    if not request.is_json:
        return {'error': 'Request must be JSON'}, 415

    if not ('director' in request.json or 'language' in request.json or
            'title' in request.json or 'year' in request.json):
        return {'error': 'Malformed request. Missing required movie fields'}, 400

    response = dictionary_builder(['director', 'language', 'title', 'year'],
                                 [request.json.get('director') or movie_data['director'],
                                  request.json.get('language') or movie_data['language'],
                                  request.json.get('title') or movie_data['title'],
                                  request.json.get('year') or movie_data['year']])
    mongo.db.user.update_one(movie_format, {'$set': response})
    return response, 200


@app.delete('/api/v1/user/movies/<string:movie_title>')
def delete_one_movie(movie_title: str):
    movie_format = dictionary_builder(['title'], [movie_title])
    movie_data = mongo.db.user.find_one(movie_format)

    if movie_data is None:
        return {'error': f'No data found for movie {movie_title}'}, 404

    mongo.db.user.delete_one(movie_format)
    movie_data.pop('_id')
    return movie_data, 200


if __name__ == '__main__':
    app.run()

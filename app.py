from flask import request
from pre_initializer import movie_api, academy_awards_data
from initializer import app, mongo
import utility


@app.get('/api/v1/omdb/movies')
def get_omdb_movie_data():
    movie_title = request.args['title']
    movie_data = movie_api.search_movie_title(movie_title)

    if len(movie_data) == 2:
        return utility.dictionary_builder(['error'], [f'No data found for movie {movie_title}']), 404

    response = utility.dictionary_builder(['director', 'language', 'title', 'year'],
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


@app.get('/api/v1/oscars/best_picture/<int:year>')
def get_oscar_best_picture_winners_by_year(year: int):
    if year < 1927 or year > 2019:
        return dictionary_builder(['error'], [f'No data found for year {year}']), 404

    response = utility.get_category_of_winners_by_year(academy_awards_data, year, 'Best Picture',
                                                       ['OUTSTANDING PICTURE', 'OUTSTANDING PRODUCTION',
                                                        'OUTSTANDING MOTION PICTURE', 'BEST MOTION PICTURE',
                                                        'BEST PICTURE'])
    mongo.db.oscars.insert_one(response)
    response.pop('_id')
    return response, 200


@app.get('/api/v1/oscars/best_actor/<int:year>')
def get_oscar_best_actor_winners_by_year(year: int):
    if year < 1927 or year > 2019:
        return dictionary_builder(['error'], [f'No data found for year {year}']), 404

    response = utility.get_category_of_winners_by_year(academy_awards_data, year, 'Best Actors',
                                                       ['ACTOR', 'ACTOR IN A LEADING ROLE',
                                                        'ACTRESS IN A LEADING ROLE', 'ACTRESS'])
    mongo.db.oscars.insert_one(response)
    response.pop('_id')
    return response, 200


@app.get('/api/v1/oscars/categories/<int:year>')
def get_movies_categories_by_year(year: int):
    if year < 1927 or year > 2019:
        return utility.dictionary_builder(['error'], [f'No data found for year {year}']), 404

    response = utility.get_genre_by_year(academy_awards_data, year)
    mongo.db.oscars.insert_one(response)
    response.pop('_id')
    return response, 200


@app.get('/api/v1/oscars/recommendation')
def get_movie_recommendation():
    return ':)'


@app.get('/api/v1/user/movies')
def get_all_movies():
    response = []
    for movie_data in mongo.db.user.find():
        movie_data.pop('_id')
        response.append(movie_data)
    return dictionary_builder(['movies'], [response]), 200


@app.get('/api/v1/user/movies/<string:movie_title>')
def get_one_movie(movie_title: str):
    movie_data = mongo.db.user.find_one(dictionary_builder(['title'], [movie_title]))

    if movie_data is None:
        return {'error': f'No data found for movie {movie_title}'}, 404

    movie_data.pop('_id')
    return movie_data, 200


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

import utility
from flask import request
from pre_initializer import movie_api, academy_awards_data
from initializer import app, mongo


@app.get('/api/v1/omdb/movies')
def get_omdb_movie():
    movie_title = request.args['title']
    movie_data = movie_api.search_movie_title(movie_title)

    if len(movie_data) == 2:
        return utility.dictionary_builder(['error'], [f'No data found for movie {movie_title}']), 404

    response = utility.get_omdb_movie_data(movie_data, utility.Options.OMDB)
    mongo.db.omdb.insert_one(response)
    response.pop('_id')
    return response, 200


@app.get('/api/v1/oscars/<int:year>')
def get_oscar_nominees_by_year(year: int):
    if year < 1927 or year > 2019:
        return utility.dictionary_builder(['error'], [f'No data found for year {year}']), 404

    response = utility.get_winners_and_nominees_of_year_dict(academy_awards_data, year)
    response['year'] = str(year)
    mongo.db.oscars.insert_one(response)
    response.pop('_id')
    return response, 200


@app.get('/api/v1/oscars/best_picture/<int:year>')
def get_oscar_best_picture_winners_by_year(year: int):
    if year < 1927 or year > 2019:
        return utility.dictionary_builder(['error'], [f'No data found for year {year}']), 404

    response = utility.get_category_of_winners_by_year(academy_awards_data, year, 'Best Picture',
                                                       ['OUTSTANDING PICTURE', 'OUTSTANDING PRODUCTION',
                                                        'OUTSTANDING MOTION PICTURE', 'BEST MOTION PICTURE',
                                                        'BEST PICTURE'])
    response['year'] = str(year)
    mongo.db.oscars.insert_one(response)
    response.pop('_id')
    return response, 200


@app.get('/api/v1/oscars/best_actor/<int:year>')
def get_oscar_best_actor_winners_by_year(year: int):
    if year < 1927 or year > 2019:
        return utility.dictionary_builder(['error'], [f'No data found for year {year}']), 404

    response = utility.get_category_of_winners_by_year(academy_awards_data, year, 'Best Actors',
                                                       ['ACTOR', 'ACTOR IN A LEADING ROLE',
                                                        'ACTRESS IN A LEADING ROLE', 'ACTRESS'])
    response['year'] = str(year)
    mongo.db.oscars.insert_one(response)
    response.pop('_id')
    return response, 200


@app.get('/api/v1/oscars/categories/<int:year>')
def get_movie_categories_by_year(year: int):
    if year < 1927 or year > 2019:
        return utility.dictionary_builder(['error'], [f'No data found for year {year}']), 404

    response = utility.get_genre_by_year(academy_awards_data, year, 0)
    response['year'] = str(year)
    mongo.db.oscars.insert_one(response)
    response.pop('_id')
    return response, 200


@app.get('/api/v1/oscars/recommendation')
def get_movie_recommendation():
    user_omdb_dict = utility.get_movies_in_database_and_years(mongo.db.user_omdb.find())
    movies_list = user_omdb_dict['movies']
    years_list = user_omdb_dict['years']

    if len(movies_list) < 2:
        error_string = f'Create at least 3 movies; got {len(movies_list)} instead'
        return utility.dictionary_builder(['error'], [error_string]), 404

    omdb_dict = utility.get_movies_in_database_and_years(mongo.db.omdb.find())

    if len(omdb_dict['movies']) < 2:
        error_string = f'Look up at least 3 movies; got {len(movies_list)} instead'
        return utility.dictionary_builder(['error'], [error_string]), 404

    movies_list += omdb_dict['movies']
    years_list += omdb_dict['years']

    len_oscar = len(years_list)
    for oscar in mongo.db.oscars.find():
        years_list.append(int(oscar['year']))
    len_oscar = len(years_list) - len_oscar

    if len_oscar < 2:
        error_string = f'Look up at least 3 Oscars ceremonies; got {len_oscar} instead'
        return utility.dictionary_builder(['error'], [error_string]), 404

    average_year = int(round(sum(years_list) / len(years_list), 0))

    genre_list = ['Action', 'Adult', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama',
                  'Family', 'Fantasy', 'Film-Noir', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'N/A', 'News',
                  'Reality-TV', 'Romance', 'Sci-Fi', 'Short', 'Sport', 'Talk-Show', 'Thriller', 'War', 'Western']
    genre_data = [0] * len(genre_list)
    genre_dict = utility.dictionary_builder(genre_list, genre_data)

    for movie in movies_list:
        genre_list = movie['genre'].split(', ')
        for genre in genre_list:
            genre_dict[genre] += 1

    sorted_genre_list = utility.sort_dictionary(genre_dict, True, 3)
    genre_dict = utility.get_genre_by_year(academy_awards_data, average_year, 2)

    response = []
    duplicate_movies = []

    for genre in sorted_genre_list:
        temp = []
        i = 0
        while len(temp) <= 1:
            movie = genre_dict[genre][i]
            if movie['film'] and len(movie['omdb']) > 2 and float(movie['omdb']['imdbRating']) >= 7.2 and movie['film'] not in duplicate_movies:
                temp.append(movie)
                duplicate_movies.append(movie['film'])
            i += 1
        response += temp

    return response, 200


@app.get('/api/v1/user/movies')
def get_all_movies():
    response = []
    for movie_data in mongo.db.user.find():
        movie_data.pop('_id')
        response.append(movie_data)
    return utility.dictionary_builder(['movies'], [response]), 200


@app.get('/api/v1/user/movies/<string:movie_title>')
def get_one_movie(movie_title: str):
    movie_data = mongo.db.user.find_one(utility.dictionary_builder(['title'], [movie_title]))

    if movie_data is None:
        return {'error': f'No data found for movie {movie_title}'}, 404

    movie_data.pop('_id')
    return movie_data, 200


@app.post('/api/v1/user/movies')
def add_one_movie():
    if not request.is_json:
        return {'error': 'Request must be JSON'}, 415

    if not ('director' in request.json and 'genre' in request.json and
            'language' in request.json and 'title' in request.json and 'year' in request.json):
        return {'error': 'Malformed request. Missing required movie fields'}, 400

    movie_data = movie_api.search_movie_title(request.json['title'])

    if len(movie_data) > 2:
        movie_response = utility.get_omdb_movie_data(movie_data, utility.Options.OMDB)
        mongo.db.user_omdb.insert_one(movie_response)

    response = utility.get_omdb_movie_data(request.json, utility.Options.JSON)
    mongo.db.user.insert_one(response)
    response.pop('_id')
    return response, 201


@app.put('/api/v1/user/movies/<string:movie_title>')
def edit_one_movie(movie_title: str):
    movie_format = utility.dictionary_builder(['title'], [movie_title])  # {'title': movie_title}
    movie_data = mongo.db.user.find_one(movie_format)

    if movie_data is None:
        return {'error': f'No data found for movie {movie_title}'}, 404

    if not request.is_json:
        return {'error': 'Request must be JSON'}, 415

    if not ('director' in request.json or 'genre' in request.json or
            'language' in request.json or 'title' in request.json or 'year' in request.json):
        return {'error': 'Malformed request. Missing required movie fields'}, 400

    response = utility.dictionary_builder(['director', 'genre', 'language', 'title', 'year'],
                                          [request.json['director'] or movie_data['director'],
                                           request.json['language'] or movie_data['language'],
                                           request.json['genre'] or movie_data['genre'],
                                           request.json['title'] or movie_data['title'],
                                           request.json['year'] or movie_data['year']])
    mongo.db.user.update_one(movie_format, {'$set': response})
    return response, 200


@app.delete('/api/v1/user/movies/<string:movie_title>')
def delete_one_movie(movie_title: str):
    movie_format = utility.dictionary_builder(['title'], [movie_title])
    movie_data = mongo.db.user.find_one(movie_format)

    if movie_data is None:
        return {'error': f'No data found for movie {movie_title}'}, 404

    mongo.db.user.delete_one(movie_format)
    movie_data.pop('_id')
    return movie_data, 200


if __name__ == '__main__':
    app.run()

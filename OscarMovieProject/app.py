from math import floor
from flask import Flask, render_template
from flask import request
from MovieAPI import MovieAPI
from json import load
from flask import jsonify
from flask_pymongo import PyMongo
import subprocess as sp
import string

app = Flask(__name__, template_folder='client/public')

app.config['MONGO_URI'] = 'mongodb://localhost:27017/Movies'
mongo_client = PyMongo(app)
mongo_collection = mongo_client.db['movie']
db = mongo_collection
ID = 0


@app.route('/', methods=('GET', 'POST'))
def index():
    list = db.find()
    return render_template('index.html', list=list)




# @app.get("/api/v2/movies")
# def get_all_movies():
#     result = []
#     for movie in db.find():
#         result.append({'title' : movie['title'], 'year' : movie['year'], 'director' : movie['director']})
#     return jsonify({'result' : result})


@app.route('/add', methods = ['POST'])
def add_user():
    _json = request.json
    _name = _json['name']
    _email = _json['email']
    _password = _json['password']

    if _name and _email and _password and request.method == 'POST':
        db.movies.insert_one({'name': _name, 'email': _email, 'password': _password})
        response = jsonify('User added successfully!')
        response.status_code = 200
        return response
    else:
        return not_found()


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found' + request.url
    }
    response = jsonify(message)


@app.route('/names', methods = ['GET'])
def default():
    return {"names": ["Alan", "Edgar", "Poe"]}


@app.get("/api/v1/movies")
def get_movie_title():
    film = request.args['title']  # use ?title= to make request
    api = MovieAPI('https://www.omdbapi.com/?apikey=', '8066aa78')
    data = api.search_movie_title(film)
    if len(data) == 2:
        return {"error": f"No data found for movie {film}"}, 404
    return {"director": data["Director"], "langauge": data["Language"], "title": data["Title"], "year": data["Year"]}


@app.get("/api/v1/movies/oscars/<int:year>")
def get_oscar_nominees_by_year(year: int):
    if year < 1927 or year > 2019:
        return {"error": f"No data found for year {year}"}, 404

    academy_awards_file = open('new_data_json.json', encoding='utf-8')
    academy_awards_data = load(academy_awards_file)
    winners_list = []
    nominees_list = []

    for award in academy_awards_data:
        if award['year'] == year:
            if award['winner']:
                winners_list.append(award)
            else:
                nominees_list.append(award)

    academy_awards_file.close()
    return {"winners": winners_list, "nominees": nominees_list}


def _helper(academy_awards_data: list, year: int, categories: list) -> list:
    winners_list = []
    for award in academy_awards_data:
        if award['year'] == year and award['winner']:
            for category in categories:
                if award['category'] == category:
                    winners_list.append(award)
                    break
    return winners_list


@app.get("/api/v1/movies/oscars/best_picture/<int:year>")
def get_oscar_best_picture_winners_by_year(year: int):
    if year < 1927 or year > 2019:
        return {"error": f"No data found for year {year}"}, 404

    academy_awards_file = open('new_data_json.json', encoding='utf-8')
    academy_awards_data = load(academy_awards_file)
    winners_list = _helper(academy_awards_data, year, ['OUTSTANDING PICTURE','OUTSTANDING PRODUCTION',
                                                       'OUTSTANDING MOTION PICTURE','BEST MOTION PICTURE',
                                                       'BEST PICTURE'])
    academy_awards_file.close()
    # global ID
    # api = MovieAPI('https://www.omdbapi.com/?apikey=', '8066aa78')
    # movie = winners_list[0]['film']
    # year = winners_list[0]['year']
    # data = api.search_movie_title_and_year(movie, year)
    # print(data)
    # db.movies.insert_one({'id': ID, 'data': data})
    # ID = ID + 1
    return winners_list


@app.get("/api/v1/movies/oscars/best_actor/<int:year>")
def get_oscar_best_actor_winners_by_year(year: int):
    if year < 1927 or year > 2019:
        return {"error": f"No data found for year {year}"}, 404

    academy_awards_file = open('new_data_json.json', encoding='utf-8')
    academy_awards_data = load(academy_awards_file)
    winners_list = _helper(academy_awards_data, year, ['ACTOR','ACTOR IN A LEADING ROLE',
                                                       'ACTRESS IN A LEADING ROLE','ACTRESS'])
    academy_awards_file.close()
    return winners_list


@app.get("/api/v1/movies/recommendation")
def get_movie_recommendation():
    year_frequency = [0] * 10
    index = None
    test_data = [1969, 2019, 1981, 1974, 2016, 1989, 1946]
    for year in test_data:
        if test_data < 2000:
            index = floor((year % 100) / 10) * 10
        else:
            index = 9 + floor((year % 100) / 10) * 10
    # query database based on highest years searched then return movie


@app.get("/api/v2/movies")
def get_all_movies():
    result = []
    for movie in db.find():
        result.append({'title' : movie['title'], 'year' : movie['year'], 'director' : movie['director']})
    return jsonify({'result' : result})


@app.get("/api/v2/movies/<string:movie_title>")
def get_one_movie(movie_title: string):
    movie = db.find_one({'title' : movie_title})
    result = []
    result.append({'title' : movie['title'], 'year' : movie['year'], 'director' : movie['director']})
    return jsonify({'result' : result})


@app.post("/api/v2/movies/")
def add_movie():
    if request.is_json:
        response = request.get_json()
        if 'title' in response and 'year' in response and 'director' in response:
            #response["id"] = _find_next_id(user_data)
            #user_data.append(response)
            id = db.insert_one({'title':response['title'],'year':response['year'],'director':response['director']})
            return response, 201
        else:
            return {"error": "Malformed request. Missing required user fields"}, 400
    return {"error": "Request must be JSON"}, 415


@app.put("/api/v2/movies/<string:movie_title>")
def edit_movie_data(movie_title: string):
    if request.is_json:
        if 'title' in request.json or 'year' in request.json or 'director' in request.json:
            myquery = {'title' : movie_title}
            newvalues = { "$set": { "title": request.json.get('title'), "year": request.json.get('year'), "director": request.json.get('director') } }
            db.update_one(myquery, newvalues)
            return jsonify("done!"), 200
        else:
            return {"error": "Malformed request. Missing required user fields"}, 400
    return {"error": "Request must be JSON"}, 415


@app.delete("/api/v2/movies/<string:movie_title>")
def delete_user(movie_title: string):
    myquery = {"title": movie_title}
    movie = db.find_one(myquery)
    db.delete_one(myquery)
    return jsonify({'title' : movie['title'], 'year' : movie['year'], 'director' : movie['director']}), 200


if __name__ == '__main__':
    app.run()

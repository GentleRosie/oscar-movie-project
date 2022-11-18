from flask import Flask
from flask import request
from MovieAPI import MovieAPI
from json import load
from flask_pymongo import PyMongo

app = Flask(__name__)

# app.config['MONGO_URI'] = 'mongodb://localhost:27017/MovieProject'
# mongo_client = PyMongo(app)
# db = mongo_client.db
#
# @app.route('/add', methods = ['POST'])
# def add_user():
#     _json = request.json
#     _name = _json['name']
#     _email = _json['email']
#     _password = _json['password']
#
#     if _name and _email and _password and request.method == 'POST':
#         db.movies.insert_one({'name': _name, 'email': _email, 'password': _password})
#         response = jsonify('User added successfully!')
#         response.status_code = 200
#         return response
#     else:
#         return not_found()
#
#
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


@app.get("/api/v1/movies")
def get_movie_title():
    title = request.args['title']  # use ?title= to make request
    api = MovieAPI('https://www.omdbapi.com/?apikey=', '8066aa78&')
    data = api.search_movie_title(title)
    if len(data) == 2:
        return {"error": f"No data found for movie {title}"}, 404
    return {"director": data["Director"], "langauge": data["Language", "title": data["Title"], "year": data["Year"]]}


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
    winners_list = _helper(academy_awards_data, year, ['OUTSTANDING PICTURE','OUTSTANDING PRODUCTION','OUTSTANDING MOTION PICTURE','BEST MOTION PICTURE','BEST PICTURE'])
    academy_awards_file.close()

    return winners_list


@app.get("/api/v1/movies/oscars/best_actor/<int:year>")
def get_oscar_best_actor_winners_by_year(year: int):
    if year < 1927 or year > 2019:
        return {"error": f"No data found for year {year}"}, 404

    academy_awards_file = open('new_data_json.json', encoding='utf-8')
    academy_awards_data = load(academy_awards_file)
    winners_list = _helper(academy_awards_data, year, ['ACTOR','ACTOR IN A LEADING ROLE','ACTRESS IN A LEADING ROLE','ACTRESS'])
    academy_awards_file.close()

    return winners_list


if __name__ == '__main__':
    app.run()

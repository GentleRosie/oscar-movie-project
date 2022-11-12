from flask import Flask
from flask import jsonify, request
from flask_pymongo import PyMongo

app = Flask(__name__)
# app.config['MONGO_URI'] = 'mongodb://localhost:27017/MovieProject'
# mongo_client = PyMongo(app)
# db = mongo_client.db

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


if __name__ == '__main__':
    app.run()
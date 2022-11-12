from flask import Flask
from flask_pymongo import PyMongo


def main():
    flask_server = Flask('MovieProject')
    flask_server.config['MONGO_URI'] = 'mongodb://localhost:27017/'
    mongo_client = PyMongo(flask_server)
    db = mongo_client.MovieProject


if __name__ == '__main__':
    main()
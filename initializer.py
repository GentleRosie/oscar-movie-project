from flask import Flask
from flask_pymongo import PyMongo
from utility import CustomJsonEncoder

app = Flask(__name__, template_folder='client/public')
app.config['MONGO_URI'] = 'mongodb://localhost:27017/MovieProject'
app.json_encoder = CustomJsonEncoder
mongo = PyMongo(app)


#  use single file and convert to Singleton!
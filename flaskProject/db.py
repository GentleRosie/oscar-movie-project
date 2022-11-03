"""
client = pymongo.MongoClient("mongodb+srv://root:password@cluster0.d8iz1bd.mongodb.net/?retryWrites=true&w=majority")
db = client.test
DANNY do this
pip install Flask pymongo
"""


import sqlite3

import click
from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
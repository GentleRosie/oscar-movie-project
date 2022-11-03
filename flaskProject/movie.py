from urllib.request import urlopen
import json


class Movie:
    API = 'https://www.omdbapi.com/?apikey='

    def __init__(self, key: str):
        self.API = f'{self.API}{key}&'

    def search(self, title: str):
        title = title.replace(' ', '+')
        self.API = f'{self.API}t={title}'
        return json.loads(urlopen(self.API).read())
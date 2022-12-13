from urllib.request import urlopen
from rest_api import RestAPI
from json import loads
from unidecode import unidecode


class MovieAPI(RestAPI):
    def __init__(self, url: str, key: str):
        super().__init__(url, key)
        self.api_url = f'{self.api_url}&'
        self.api_request = None

    def search_movie_title(self, title: str):
        decoded_title = unidecode(title)
        decoded_title = decoded_title.replace(' ', '+')
        self.api_request = f'{self.api_url}t={decoded_title}'
        return loads(urlopen(self.api_request).read())

    def search_movie_title_and_year(self, title: str, year: int):
        decoded_title = unidecode(title)
        decoded_title = decoded_title.replace(' ', '+')
        self.api_request = f'{self.api_url}t={decoded_title}&y={year}'
        return loads(urlopen(self.api_request).read())

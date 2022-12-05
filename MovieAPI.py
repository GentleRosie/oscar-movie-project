from urllib.request import urlopen
from RestAPI import RestAPI
from json import loads


class MovieAPI(RestAPI):
    def __init__(self, url: str, key: str):
        super().__init__(url, key)
        self.api_request = None

    def search_movie_title(self, title: str):
        title = title.replace(' ', '+')
        self.api_request = f'{self.api}t={title}'
        return loads(urlopen(self.api_request).read())

    def search_movie_title_and_year(self, title: str, year: int):
        title = title.replace(' ', '+')
        self.api_request = f'{self.api}t={title}&y={year}'
        return loads(urlopen(self.api_request).read())

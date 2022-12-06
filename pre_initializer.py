from movie_api import MovieAPI
from json import load

academy_awards_file = open('new_data_json.json', encoding='utf-8')
academy_awards_data = load(academy_awards_file)
movie_api = MovieAPI('https://www.omdbapi.com/?apikey=', '902f9339')
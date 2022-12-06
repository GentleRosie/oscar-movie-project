from json import JSONEncoder
from bson.objectid import ObjectId
from pre_initializer import movie_api

class CustomJsonEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return super(CustomJsonEncoder, self).default(o)


class Error(Exception):
    pass


class IncorrectValueListError(Error):
    pass


class IncorrectKeyListError(Error):
    pass


def dictionary_builder(keys: list, values: list) -> dict:
    if len(keys) > len(values):
        raise IncorrectValueListError(f'Length of values list should be {len(keys)}; got {len(values)} instead')
    elif len(keys) < len(values):
        raise IncorrectKeyListError(f'Length of keys list should be {len(keys)}; got {len(values)} instead')

    temp = {}
    for i in range(len(keys)):
        key = keys[i]
        value = values[i]
        temp[f'{key}'] = value

    return temp


def get_winners_and_nominees_of_year_dict(academy_awards_data: list, year: int) -> dict:
    winners_list = []
    nominees_list = []

    for award in academy_awards_data:
        if award['year'] == year:
            winners_list.append(award) if award['winner'] else nominees_list.append(award)

    return dictionary_builder(['nominees', 'winners'], [nominees_list, winners_list])


def get_category_of_winners_by_year(academy_awards_data: list, year: int, category: str, categories: list) -> dict:
    winners_and_nominees_dict = get_winners_and_nominees_of_year_dict(academy_awards_data, year)
    winners_list = winners_and_nominees_dict['winners']
    winners_category = []

    for winner in winners_list:
        if winner['category'] in categories:
            winners_category.append(winner)

    return dictionary_builder(['category', 'omdb', 'winners'], [f'{category}', None, winners_category])


def get_omdb_list_of_movies_by_title_and_year(movie_data: list) -> list:
    omdb_list = []

    for index in range(len(movie_data)):
        movie_title = movie_data[index]['film']
        movie_year = str(movie_data[index]['year'])
        omdb_list.append(movie_api.search_movie_title_and_year(movie_title, movie_year))

    return omdb_list

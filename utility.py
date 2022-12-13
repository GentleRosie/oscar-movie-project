from json import JSONEncoder
from bson.objectid import ObjectId


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

    for award in academy_awards_data[str(year)]:
        winners_list.append(award) if award['winner'] else nominees_list.append(award)

    return dictionary_builder(['nominees', 'winners'], [nominees_list, winners_list])


def get_category_of_winners_by_year(academy_awards_data: list, year: int, category: str, categories: list) -> dict:
    winners_and_nominees_dict = get_winners_and_nominees_of_year_dict(academy_awards_data, year)
    winners_list = winners_and_nominees_dict['winners']
    winners_category = []

    for winner in winners_list:
        if winner['category'] in categories:
            winners_category.append(winner)

    return dictionary_builder(['category', 'winners'], [f'{category}', winners_category])


def get_genre_by_year(academy_awards_data: list, year: int):
    genre_list = ['Action', 'Adult', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama',
                  'Family', 'Fantasy', 'Film-Noir', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'N/A', 'News',
                  'Reality-TV', 'Romance', 'Sci-Fi', 'Short', 'Sport', 'Talk-Show', 'Thriller', 'War', 'Western']
    genre_data = []

    for genre in genre_list:
        genre_data.append([])

    genre_dict = dictionary_builder(genre_list, genre_data)

    for data in academy_awards_data[str(year)]:
        if data['film'] is None or len(data['omdb']) == 2:
            genre_dict['N/A'].append(data)
        else:
            genre_list = data['omdb']['Genre'].split(', ')
            for genre in genre_list:
                genre_dict[genre].append(data)

    genre_dict['year'] = year

    return genre_dict

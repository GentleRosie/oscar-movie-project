from json import JSONEncoder
from bson.objectid import ObjectId

import app
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


def rated_recommendation_list(movie_data: dict):
    rated_list = app.rated_list
    rated = movie_data['Rated']
    if len(rated_list) == 0:
        rated_list.insert(0, [rated, 1])
    else:
        for i in range(len(rated_list)):
            if rated_list[i][0] == rated:
                rated_list[i][1] += 1
                break
            if i == len(rated_list) - 1:
                rated_list.insert(0, [rated, 1])
    # sort rated_list based on frequency so movie rating with the highest frequency is first
    print(rated_list)


def ratings_recommendation_list(movie_data: dict):
    ratings_list = app.ratings_list
    ratings = movie_data['Ratings']
    rotten_tomatoes = None
    imdb = None
    metacritic = None
    for i in range(len(ratings)):
        if ratings[i]['Source'] == "Rotten Tomatoes":
            rotten_tomatoes = ratings[i]['Value']
            rotten_tomatoes = int(rotten_tomatoes[0: -1])
        if ratings[i]['Source'] == "Internet Movie Database":
            imdb = ratings[i]['Value']
            temp = imdb.split('/')
            imdb = int(float(temp[0]) * 10)
        if ratings[i]['Source'] == "Metacritic":
            metacritic = ratings[i]['Value']
            temp = metacritic.split('/')
            metacritic = int(temp[0])
    print(ratings)
    print("ratings:", rotten_tomatoes, metacritic, imdb)

    temp_list = [rotten_tomatoes, metacritic, imdb]
    average = 0
    counter = 0
    for i in range(len(temp_list)):
        if temp_list[i]:
            counter += 1
            average += temp_list[i]
    average = average / counter
    print("rating average:", int(round(average, 0)))


def genre_recommendation_list(movie_data: dict):
    genre_list = app.genre_list
    genres = movie_data['Genre'].split(',')
    for i in range(1, len(genres)):
        genres[i] = genres[i][1:len(genres[i])]
    print(genres)

    if len(genre_list) == 0:
        for genre in genres:
            genre_list.insert(0, [genre, 1])
    else:
        for i in range(len(genres)):
            for j in range(len(genre_list)):
                if genre_list[j][0] == genres[i]:
                    genre_list[j][1] += 1
                    break
                if j == len(genre_list) - 1:
                    genre_list.insert(0, [genres[i], 1])

    print(genre_list)

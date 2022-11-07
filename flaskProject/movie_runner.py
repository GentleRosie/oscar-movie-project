from movie import Movie


def main():
    movie = Movie('8066aa78')
    response = input("Please enter a movie name: ")
    data = movie.search(response)

    print(data)
    # no error check when movie
    print(f"Title: {data['Title']}\nYear: {data['Year']}\nDirector: {data['Director']}")


if __name__ == "__main__":
    main()

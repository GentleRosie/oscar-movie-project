from movie import Movie


def main():
    movie = Movie('8066aa78')
    response = input("Please enter a movie name: ")
    print(movie.search(response))


if __name__ == "__main__":
    main()

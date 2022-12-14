#### Oscar Movie Project Release Notes
##### Krabby Daddies
Mohammed Chalabi, Jacob Correa, Kiranjot Kaur, Brandon Kmiec, Jose Martinez, Branden Nguyen, Danny Zhou

Oscar Movie Project
Date of Release/Distribution: December 14, 2022


# The Oscar Movie Project - 131
____
### Release Notes
After weeks of work and progress, the Movie Oscar Project presented by the Krabby Daddies is finally available! Version 1.0 will be available for release on December 14, 2022. 

##### Overview
Movie software application that takes movies across databases and allows queries to be made to find certain movies based off certain criteria. The queries are stored in a local database, and movies in the local database may be retrieved, added, edited, deleted.
##### Purpose
The purpose of the product is to make the idea of querying movies easier by collecting data across multiple movie databases and putting them all into one application.
Feature Summary
-	Full CRUD operations supported!
    - Create: Ability to add new movies
    - Read: Ability to query a specific movie
    - Update: Ability to update an existing movie in the database
    - Delete: Ability to delete a movie in the database
-	Queries to search for a movie
    - Query by movie title: Gain information about a movie by query using its title
    - Query by Academy Awards Oscars Nominees: Gain information about academy award nominees by query using the year of the awards ceremony
    - Query by Best Picture: Gain information about “Best Picture” category winners by query using the year of the awards ceremony
    - Query by Best Actor: Gain information about “Best Actor” category winners by query using the year of the awards ceremony
    - Query by genre: Gain information about the movies, sorted by genre by query using the year of the awards ceremony (extra credit query)
    - Query by recommendation: Gain information about movies that the user may enjoy based off on previous searches that have been made
-	Front end operational
    - Query by OMBD, displays movie poster and info upon searched movie title

##### Issue Summary
- Issue with cloning repo 
- Issue with MongoDB
- Issue with pip
##### Steps to Reproduce
- Repo: Delete existing program and create new one with flask settings
- MongoDB: Make sure terminal commands are inserted (mongod and mongosh) and connect with compass
- Pip: Reconfigure PyCharm or reinstall PyCharm 
##### End-User Impact
List of specific actions needed by users or functionality impacted by the changes. (to be worked on -Branden)
-	Do not copy and paste code onto files without installing needed packages and modules, cloning repository will have least number of errors.

##### Installation (WILL ADD MORE DETAIL TO INSTALLATION TMRW -BRANDEN)
###### 1. Install Python and a Python IDE (PyCharm recommended) to run the python files
To ensure that the program runs properly, one must adjust their Python settings.
Python Packages (must be installed):
- Pymongo
- Flask
- Unidecode

The configuration must be edited:
- Add a “Flask Server” configuration
- Change the target type of configuration to a “Script path”
- The “Target” path must path to the location of app.py
Install necessary modules:

###### 2. Install MongoDB Community Server and MongoDB Shell to run the database
- Download the MongoDB Community Server and MongoDB Shell
- ENSURE that MongoDBCompass is installed when using the installer. MongoDBCompass is used to view the different databases
- In your 'main' drive (C: drive, D: drive, etc.) make a folder called 'data' and within that folder make another folder called 'db'
- Download MongoDB shell and move folder into 'main' drive
- Edit the Environment variable called 'Path' where the bin of MongoDB is located and MongoDB shell
    - To properly edit the environment variables, search “Environmental Variables” on the system. Under the “System variables” tab, click on the ‘PATH’ variable and edit it. Add new paths to the MongoDB ‘bin’ folder and the Mongosh ‘bin’ folder
- Open two command prompts and type the following: mongod for one prompt, mongosh for the other
- Open MongoDBCompass and connect to the local host URI once everything is installed successfully; as the user uses the queries or CRUD functionalities, the database should update after refreshing
###### 3. Install an API client (Insomnia recommended) to ensure that the REST API endpoints are working properly
- Install NodeJS


3. Install an API client (Insomnia recommended) to ensure that the REST API endpoints are working properly
-Install NodeJS

#### REST API Endpoints 
____
#### **ROOT: http://127.0.0.1:5000**
#
#### get_omdb_movie
**URL:** /api/v1/omdb/movies?title=
**Method:** `GET`
**URL Params:** `title = [string]`
##### Success Response: 
**Code:** 200 <br />
**Content:**
`{
"director": "Chris Buck, Jennifer Lee",
"genre": "Animation, Adventure, Comedy",
"language": "English, Norwegian",
"title": "Frozen",
"year": "2013"
}`
##### Error Response: 
Code: 404 NOT FOUND <br />
**Content:** 
`{
"error": "No data found for movie frozenfrozenfrozen"
}`

##### Sample Call: 
`curl --request GET \
  --url 'http://127.0.0.1:5000/api/v1/omdb/movies?title=Frozen'`
**Notes:** This query queries the OMDB API and returns the director, genre, language, title, and year of the movie.

#### get_oscar_nominees_by_year
**URL:** /api/v1/oscars/<int:year>
**Method:** `GET`
**URL Params:** `year = [integer]`
###### Success Response: 
**Code:** 200 <br />
**Content:**
`{
"nominees": [ 79 ],
"winners": [ 25 ],
"year": "1972"
}`
##### Error Response: 
**Code:** 404 RESPONSE NOT FOUND <br />
**Content:**
`{"error": "No data found for year 2022"}`
##### Sample Call: 
**Notes:** This query parses the Oscars data and returns the nominees and winners of the entered year in two lists (both lists can be expanded to give information about the movies)

##### get_oscar_best_picture_winners_by_year
**URL:** /api/v1/oscars/best_picture/<int:year>
**Method:** GET
**URL Params:** year = [integer]
##### Success Response:
**Code:** 200
**Content:**
`{
"category": "Best Picture",
"winners": [
{
"category": "BEST PICTURE",
"film": "The Godfather",
"omdb": {
"Actors": "Marlon Brando, Al Pacino, James Caan",
"Awards": "Won 3 Oscars. 32 wins & 30 nominations total",
"BoxOffice": "$136,381,073",
"Country": "United States",
"DVD": "11 May 2004",
"Director": "Francis Ford Coppola",
"Genre": "Crime, Drama",
"Language": "English, Italian, Latin",
"Metascore": "100",
"Plot": "The aging patriarch of an organized crime dynasty in postwar New York City transfers control of his clandestine empire to his reluctant youngest son.",
"Poster": "https://m.media-amazon.com/images/M/MV5BM2MyNjYxNmUtYTAwNi00MTYxLWJmNWYtYzZlODY3ZTk3OTFlXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_SX300.jpg",
"Production": "N/A",
"Rated": "R",
"Ratings": [
{
"Source": "Internet Movie Database",
"Value": "9.2/10"
},
{
"Source": "Rotten Tomatoes",
"Value": "97%"=
},
{
"Source": "Metacritic",
"Value": "100/100"
}
],
"Released": "24 Mar 1972",
"Response": "True",
"Runtime": "175 min",
"Title": "The Godfather",
"Type": "movie",
"Website": "N/A",
"Writer": "Mario Puzo, Francis Ford Coppola",
"Year": "1972",
"imdbID": "tt0068646",
"imdbRating": "9.2",
"imdbVotes": "1,847,150"
},
"winner": true
}
],
"year": "1972"
}`
##### Error Response: 
**Code:** 404 NOT FOUND <br />
**Content:**
`{
"error": "No data found for year 2023"
}`
##### Sample Call: 
**Notes:** This query parses the Oscars data and returns full information on the best picture winner for the year entered.
##### get_oscar_best_actor_winners_by_year
**URL:** /api/v1/oscars/best_actor/<int:year>
**Method:** `GET`
**URL Params:** `year = [integer]`
###### Success Response: 
**Code:** 200 <br />
**Content:**
`{
"category": "Best Actors",
"winners": [
{
"category": "ACTOR IN A LEADING ROLE",
"film": "Gladiator",
"omdb": {
"Actors": "Russell Crowe, Joaquin Phoenix, Connie Nielsen",
"Awards": "Won 5 Oscars. 60 wins & 106 nominations total",
"BoxOffice": "$187,705,427",
"Country": "United States, United Kingdom, Malta, Morocco",
"DVD": "26 Sep 2000",
"Director": "Ridley Scott",
"Genre": "Action, Adventure, Drama",
"Language": "English",
"Metascore": "67",
"Plot": "A former Roman General sets out to exact vengeance against the corrupt emperor who murdered his family and sent him into slavery.",
"Poster": "https://m.media-amazon.com/images/M/MV5BMDliMmNhNDEtODUyOS00MjNlLTgxODEtN2U3NzIxMGVkZTA1L2ltYWdlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_SX300.jpg",
"Production": "N/A",
"Rated": "R",
"Ratings": [
{
"Source": "Internet Movie Database",
"Value": "8.5/10"
},
{
"Source": "Rotten Tomatoes",
"Value": "79%"
},
{
"Source": "Metacritic",
"Value": "67/100"
}
],
"Released": "05 May 2000",
"Response": "True",
"Runtime": "155 min",
"Title": "Gladiator",
"Type": "movie",
"Website": "N/A",
"Writer": "David Franzoni, John Logan, William Nicholson",
"Year": "2000",
"imdbID": "tt0172495",
"imdbRating": "8.5",
"imdbVotes": "1,493,754"
},
"winner": true
},
{
"category": "ACTRESS IN A LEADING ROLE",
"film": "Erin Brockovich",
"omdb": {
"Actors": "Julia Roberts, Albert Finney, David Brisbin",
"Awards": "Won 1 Oscar. 33 wins & 59 nominations total",
"BoxOffice": "$125,595,205",
"Country": "United States",
"DVD": "15 Aug 2000",
"Director": "Steven Soderbergh",
"Genre": "Biography, Drama",
"Language": "English",
"Metascore": "73",
"Plot": "An unemployed single mother becomes a legal assistant and almost single-handedly brings down a California power company accused of polluting a city's water supply.",
"Poster": "https://m.media-amazon.com/images/M/MV5BYTA1NWRkNTktNDMxNS00NjE4LWEzMDAtNzA3YzlhYzRhNDA4L2ltYWdlXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg",
"Production": "N/A",
"Rated": "R",
"Ratings": [
{
"Source": "Internet Movie Database",
"Value": "7.4/10"
},
{
"Source": "Rotten Tomatoes",
"Value": "85%"
},
{
"Source": "Metacritic",
"Value": "73/100"
}
],
"Released": "17 Mar 2000",
"Response": "True",
"Runtime": "131 min",
"Title": "Erin Brockovich",
"Type": "movie",
"Website": "N/A",
"Writer": "Susannah Grant",
"Year": "2000",
"imdbID": "tt0195685",
"imdbRating": "7.4",
"imdbVotes": "199,378"
},
"winner": true
}
],
"year": "2000"
}
Error Response: 
Code: 404
Content:
{
"error": "No data found for year 2024"
}`
##### Sample Call: 
**Notes:** This query parses the Oscars data and returns full information on the best actor winner(s) for the year entered.

##### get_movie_genres_by_year
**URL:** /api/v1/oscars/genres/<int:year>
**Method:** `GET`
**URL Params:** `year = [integer]`
##### Success Response: 
**Code:** 200 <br />
**Content:**
`{
"Action": [ 16 ],
"Adult": [],
"Adventure": [ 19 ],
"Animation": [ 8 ],
"Biography": [ 24 ],
"Comedy": [ 13 ],
"Crime": [ 13 ],
"Documentary": [ 9 ],
"Drama": [ 81 ],
"Family": [ 8 ],
"Fantasy": [ 5 ],
"Film-Noir": [],
"History": [ 14 ],
"Horror": [],
"Music": [ 16 ],
"Musical": [],
"Mystery": [ 5 ],
"N/A": [ 3 ],
"News": [],
"Reality-TV": [],
"Romance": [ 26 ],
"Sci-Fi": [ 3 ],
"Short": [ 18 ],
"Sport": [ 1 ],
"Talk-Show": [],
"Thriller": [ 4 ],
"War": [],
"Western": [],
"year": "2005"
}`
##### Error Response: 
**Code:** 404 NOT FOUND <br />
**Content:**
`{
"error": "No data found for year 1920"
}`
##### Sample Call: 
**Notes:** This query parses the Oscars data and returns full information on the movies sorted in specific genre lists and an average rating for the year entered.

#### get_movie_recommendation
**URL:** /api/v1/oscars/recommendation
**Method:** `GET`
**URL Params:** `N/A`
##### Success Response: 
**Code:** 200 <br />
**Content:**
`Too much information to paste on the document. It will recommend five movies and it will display full information for all five of the movies`
##### Error Response: 
**Code:** 404 NOT FOUND <br />
**Content:**
`{
"error": "Create at least 3 movies; got 0 instead"
}`
`{
"error": "Look up at least 3 movies; got 0 instead"
}`
`{
"error": "Look up at least 3 Oscars ceremonies; got 0 instead"
}`
##### Sample Call: 
``curl --request GET \
  --url http://127.0.0.1:5000/api/v1/oscars/recommendation``
**Notes:** This method returns a list of movie recommendations. The method gets an average year and the top three genres searched up. Then, it returns two movies that are higher than the average ratings for the top two genres and one for the third highest  genre.

##### get_all_movies
**URL:** /user/movies
**Method:** `GET`
**URL Params:** `N/A`
##### Success Response: 
**Code:** 200 <br />
**Content:**
`[
{
"director": "James Cameron",
"genre": "Drama, Romance",
"language": "English, Swedish, Italian, French",
"title": "Titanic",
"year": "1997"
}
]`
##### Error Response: 
**Code:** 404 NOT FOUND <br />
**Content:**
##### Sample Call: 
**Notes:** This CRUD method returns all movies that is stored in the user database.

##### get_one_movie
**URL:** /api/v1/user/movies/<string:movie_title>
**Method:** `GET`
**URL Params:** `movie_title = [string]`
##### Success Response: 
**Code:** 200 <br />
**Content:**
`{
"director": "James Cameron",
"genre": "Drama, Romance",
"language": "English, Swedish, Italian, French",
"title": "Titanic",
"year": "1997"
}`
##### Error Response: 
**Code:** 200 <br />
**Content:** `[] (empty list)`
##### Sample Call: 
`curl --request GET \
  --url http://127.0.0.1:5000/api/v1/user/movies/`
**Notes:** This CRUD method return one single and specific movie from the User database.

##### add_one_movie
**URL:** /api/v1/user/movies
**Method:** `POST`
**URL Params:** 
##### Success Response: 
**Code:** 200 <br />
**Content:**
`{
"director": "James Cameron",
"genre": "Drama, Romance",
"language": "English, Swedish, Italian, French",
"title": "Titanic",
"year": "1997"
}`
##### Error Response: 
**Code:** 200 <br />
**Content:** `[] (empty list)`
**Payload: **
`{
"director": "",
"genre": "",
"language": "",
"title": "",
"year": ""
}`
##### Sample Call: 
**Notes:** This CRUD method adds a movie of the user’s choice to the User database.

##### edit_one_movie
**URL:** /api/v1/user/movies/<string:movie_title>
**Method:** `PUT`
**URL Params:** `movie_title = [string]`
##### Success Response: 
**Code:** 200
**Content:**
**Error Response: **
**Code:** 404 NOT FOUND <br />
**Content:** `Movie not found`
**Payload:**
`{
"director": "",
"genre": "",
"language": "",
"title": "",
"year": ""
}`
##### Sample Call: 
**Notes:** This CRUD method allows the user to edit fields of a movie in User database by editing the movie details with JSON.

##### delete_one_movie
**URL:** /api/v1/user/movies/<string:movie_title>
**Method:** `DELETE`
**URL Params:** `movie_title = [string]`
**Success Response:**
**Code:** 200 <br />
**Content:**
`{
"director": "James Cameron",
"genre": "Drama, Romance",
"language": "English, Swedish, Italian, French",
"title": "Titanic",
"year": "1997"
}`
**Error Response: **
**Code:** 404 NOT FOUND <br />
**Content:** `Movie not found`
##### Sample Call: 
**Notes:** This CRUD method allows the user to delete a movie from the User database by searching the movie title.

### Disclaimers
This product was made by college students and not professional software engineers. The product may contain bugs or errors that college students are prone to make.

#### Contact
 Please contact the Krabby Daddies via Sac State email for any inquiries.
> Jacob Correa (Scrum Master) jccorrea@csus.edu
> Danny Zhou (Development Team) dannyzhou@csus.edu
> Mohammed Al Chalabi (Development Team) mohammedalchalabi@csus.edu 
> Kiranjot Kaur (Development Team) kiranjotkaur@csus.edu
> Jose Martinez (Development Team) jjmartinez@csus.edu
> Branden Nguyen (Development Team) brandenmnguyen@csus.edu
> Brandon Kmiec (Development Team) bkmiec@csus.edu

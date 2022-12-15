import { useState, useEffect } from "react";
import "./App.css";
import styled from "styled-components";
import 'bootstrap/dist/css/bootstrap.min.css';

// const SearchBox = styled.div`
//   display: flex;
//   // flex-direction: row;
//   padding: 20px 20px;
//   border-radius: 10px;
//   margin-left: 555px;
//   width: 24.5%;
//   background-color: lightblue;
//   color: lightgrey;
//
// `;

// const SearchInput = styled.input`
//   color: pink;
//   background-color: white;
//   font-size: 20px;
//   font-weight: bold;
//   // border: none;
//   // outline: none;
//   margin-left: 20px;
// `

const MovieListHeading = (props) => {
	return (
		<div className='col'>
			<h1>{props.heading}</h1>
		</div>
	);
};

const MovieList = (props) => {
	return (
		<>
			{props.movies.map((movie, index) => (
				<div className='image-container d-flex justify-content-start m-3'>
					<img src={movie.Poster} alt='movie'></img>
				</div>
			))}
		</>
	);
};

const SearchBox = (props) => {
	return (
		<div className='col col-sm-4'>
			<input
				className='form-control'
				value={props.value}
				onChange={(event) => props.setSearchValue(event.target.value)}
				placeholder='Type to search...'
			></input>
		</div>
	);
};



function Tabs() {
  const [toggleState, setToggleState] = useState(1);
  const [searchQuery, updateSearchQuery, setLoading] = useState("");
  const [movieList, updateMovieList] = useState([]);
  const [selectedMovie, onMovieSelect] = useState();
  const [movies, setMovies] = useState([]);
  const [searchValue, setSearchValue] = useState('');

  const [timeoutId, updateTimeoutId] = useState();

  const [data, setData] = useState([{}])
  // figure out how to hook custom functions for dynamic uri on fetch line (

  const getMovieRequest = async (searchValue) => {
		// const url = `/api/v1/user/movies?title=${searchValue}`;
		const url = `http://www.omdbapi.com/?s=${searchValue}&apikey=263d22d8`;

		const response = await fetch(url);
		const responseJson = await response.json();

		if (responseJson.Search) {
			setMovies(responseJson.Search);
		}
	};

  useEffect(() => {
		getMovieRequest(searchValue);
	}, [searchValue]);


  const toggleTab = (index) => {
    setToggleState(index);
  };
 const onTextChange = (e) => {
    onMovieSelect("")
    clearTimeout(timeoutId);
    updateSearchQuery(e.target.value);
    const timeout = setTimeout(() => setData(e.target.value), 100000);
    updateTimeoutId(timeout);
  };
  return (
    <div className="container-fluid">
      <div className="bloc-tabs">
        <button
          className={toggleState === 1 ? "tabs active-tabs" : "tabs"}
          onClick={() => toggleTab(1)}
        >
          OMDB
        </button>
        <button
          className={toggleState === 2 ? "tabs active-tabs" : "tabs"}
          onClick={() => toggleTab(2)}
        >
          Oscars
        </button>
        <button
          className={toggleState === 3 ? "tabs active-tabs" : "tabs"}
          onClick={() => toggleTab(3)}
        >
          User
        </button>
      </div>

      <div className="content-tabs">
        <div
          className={toggleState === 1 ? "content  active-content" : "content"}
        >
          <h2>Please Enter Movie Title: </h2>
          <p>

				<MovieListHeading heading='Movies' />
				<SearchBox searchValue={searchValue} setSearchValue={setSearchValue} />

			<div className='row'>
				<MovieList movies={movies} />
			</div>

          </p>
        </div>

        <div className={toggleState === 2 ? "content  active-content" : "content"}>
          <h2>Content 2</h2>
          <p>
            krabbydaddiesfighting
          </p>
        </div>

        <div
          className={toggleState === 3 ? "content  active-content" : "content"}
        >
          <h2>Content 3</h2>
          <p>
            deez nuts
              {
            (typeof data === 'undefined') ? (<p>Loading . . .</p>) : (data.map((movie, i) => (<p key={i}>{JSON.stringify(movie)}</p>)))
            }
          </p>
        </div>
      </div>
    </div>
  );
}

export default Tabs;
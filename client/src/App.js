import React, {useState, useEffect} from 'react';

function App()
{
  const [data, setData] = useState([{}])
  // figure out how to hook custom functions for dynamic uri on fetch line (
  useEffect(() => {
    fetch('/api/v1/user/movies').then(
      jsonResponse => jsonResponse.json()
    ).then(
      data => {
        setData(data)
      }
    )
  }, []);

  return (
    <div>
      {
        (typeof data === 'undefined') ? (<p>Loading . . .</p>) : (data.map((movie, i) => (<p key={i}>{JSON.stringify(movie)}</p>)))
      }
      {
        (typeof data === 'undefined') ? (<p>Loading . . .</p>) : (data.map((movie, i) => (<p key={i}>{JSON.parse(JSON.stringify(movie)).director}</p>)))
      }
      {
        (typeof data === 'undefined') ? (<p>Loading . . .</p>) : (data.map((movie, i) => (<p key={i}>{JSON.parse(JSON.stringify(movie)).genre}</p>)))
      }
      {
        (typeof data === 'undefined') ? (<p>Loading . . .</p>) : (data.map((movie, i) => (<p key={i}>{JSON.parse(JSON.stringify(movie)).language}</p>)))
      }
      {
        (typeof data === 'undefined') ? (<p>Loading . . .</p>) : (data.map((movie, i) => (<p key={i}>{JSON.parse(JSON.stringify(movie)).title}</p>)))
      }
      {
        (typeof data === 'undefined') ? (<p>Loading . . .</p>) : (data.map((movie, i) => (<p key={i}>{JSON.parse(JSON.stringify(movie)).year}</p>)))
      }
    </div>
  )
}

export default App
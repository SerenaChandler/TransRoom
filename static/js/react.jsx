
const button = document.querySelector('#pals')


function SearchBar() {
  return (
    <div>
        <h1>search for a restroom!</h1>
      <form action="/handle-search" id="search-form">
        <p className="searchBarElement">
          Search: <input id="search-text" type="text" name="search"></input>
        </p>
        <input
          className="searchBarElement"
          type="checkbox"
          name="ada"
          value="True"
        ></input>
        <label>ADA accessible</label>

        <p className="searchBarElement">
          <input
            value="Find a restroom!"
            id="search-button"
            type="submit"
          ></input>
        </p>
      </form>
    </div>
  );
}


function GetSearchResults() {

    return(
        <div>

        </div>

    )
}



function DisplayPage() {
  return (
    <React.Fragment>
      {/* <NavBar /> */}
      <SearchBar />
    </React.Fragment>
  );
}

ReactDOM.render(<DisplayPage />, document.querySelector("#ReactApp"));

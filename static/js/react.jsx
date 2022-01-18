// function NavBar() {
//   return (
//     <header className="header">
//       <nav id="navbar">
//         <div>
//           <a href="/">
//             <img
//               id="flag"
//               src={"static/img/transflagsimple.png"}
//               alt="image of the trans pride flad"
//             />
//           </a>
//         </div>

//         <div id="navtext">
//           <h2 className="navtext">
//             <a href="/add">Add a Restroom</a>
//           </h2>
//           <h2 className="navtext">
//             <a href="/user">User Profile</a>
//           </h2>
//           <h2 className="navtext">
//             <a href="/login">Login</a>
//           </h2>
//           <h2 className="navtext">
//             <a href="/logout">Logout</a>
//           </h2>
//         </div>
//       </nav>
//     </header>
//   );
// }

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

function DisplayPage() {
  return (
    <React.Fragment>
      {/* <NavBar /> */}
      <SearchBar />
    </React.Fragment>
  );
}

ReactDOM.render(<DisplayPage />, document.querySelector("#ReactApp"));

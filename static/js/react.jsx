function NavBar() {
  return (
    <header className="header">
      <nav id="navbar">
        <div>
          <a href="/">
            <img
              id="flag"
              src={"static/img/transflagsimple.png"}
              alt="image of the trans pride flad"
            />
          </a>
        </div>

        <div id="navtext">
          <h2 className="navtext">
            <a href="/add">Add a Restroom</a>
          </h2>
          <h2 className="navtext">
            <a href="/user">User Profile</a>
          </h2>
          <h2 className="navtext">
            <a href="/login">Login</a>
          </h2>
          <h2 className="navtext">
            <a href="/logout">Logout</a>
          </h2>
        </div>
      </nav>
    </header>
  );
}

ReactDOM.render(<NavBar />, document.querySelector("#ReactApp"));

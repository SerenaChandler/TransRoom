function App() {
  const [matchesData, setMatchesData] = React.useState([]);
  const [displayMatches, setDisplayMatches] = React.useState([]);

  function MatchCard(props) {
    return (
      <div className="match">
        <p>Username: {props.username}</p>
        <form action="/add-friend">
          <input className="button" type="submit" id={props.id} value={'add friend'} onClick={addFriend}/>
        </form>
      </div>
    );
  }

  function addFriend(evt) {
    evt.preventDefault()
    const formInputs = {
      id: evt.target['id'],
    };
    console.log(evt.target['id']);
    fetch(`/add-friend`, {
      method: "POST",
      body: JSON.stringify(formInputs),
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((res) => res.json())
      .then(data => alert(data.status))
  }

  function MatchContainer() {
    return <div className="matchBox">{displayMatches}</div>;
  }

  React.useEffect(() => {
    fetch("/find-pals")
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
        setMatchesData(data);
      });
  }, []);

  function showMatches() {
    const matchList = [];
    for (let match of matchesData) {
      matchList.push(
        <MatchCard key={match.id} username={match.username} id={match.id} />
      );
    }
    setDisplayMatches(matchList);
  }

  return (
    <React.Fragment>
      <MatchButton seeFriends={showMatches} />
      <MatchContainer />
    </React.Fragment>
  );
}

function MatchButton(props) {
  return <button id="find-friends" onClick={props.seeFriends}>Find Your Bowlmate</button>;
}

ReactDOM.render(<App />, document.querySelector("#ReactApp"));

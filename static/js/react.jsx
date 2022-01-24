function App() {
  const [matchesData, setMatchesData] = React.useState([]);
  const [displayMatches, setDisplayMatches] = React.useState([]);

  function MatchCard(props) {
    return (
      <div className="match">
        <p>Username: {props.username}</p>
        <button onClick={addFriend} id="comments-button">
          Add Friend
        </button>
        <form action="/add-friend">
          <input type="submit" id={props.id} value={'add friend'} onClick={addFriend}/>
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
      .then(data => console.log(data))
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
  return <button onClick={props.seeFriends}>Click Here</button>;
}

ReactDOM.render(<App />, document.querySelector("#ReactApp"));

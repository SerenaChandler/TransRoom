function App() {
  const [matchesData, setMatchesData] = React.useState([]);
  const [displayMatches, setDisplayMatches] = React.useState([]);

  function MatchCard(props) {
    return (
      <div className="match">
        <p>Username: {props.username}</p>
        <button id="comments-button">Add Friend</button>
      </div>
    );
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
      matchList.push(<MatchCard key={match.id} username={match.username} />);
    }
    setDisplayMatches(matchList);
  }

  return (
    <React.Fragment>
      <MatchButton checkState={showMatches} />
      <MatchContainer />
    </React.Fragment>
  );
}

function MatchButton(props) {
  return <button onClick={props.checkState}>Click Here</button>;
}

ReactDOM.render(<App />, document.querySelector("#ReactApp"));

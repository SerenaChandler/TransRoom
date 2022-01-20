function App() {
  function MatchCard(props) {
    return (
      <div className="match">
        <p>Username: {props.username}</p>
      </div>
    );
  }

  const FindMatches = () => {
    const [matchesData, setMatchesData] = React.useState([]);

    React.useEffect(() => {
      fetch("/find-pals")
        .then((res) => res.json())
        .then((data) => setMatchesData(data));
    }, []);

    const matches = [];
    function makeMatches() {
    for (let match of matchesData) {
      console.log(match);
      matches.push(<MatchCard key={match.id} username={match.username} />);
    }}

    if (matches.length < 1) {
    return (
      <React.Fragment>
        <button onClick={makeMatches}>click here</button>
      </React.Fragment>
    );
  }else{
    return (
      <React.Fragment>
        <div>{matches}</div>
      </React.Fragment>
    );
    }

  };

  return (
    <React.Fragment>
      <FindMatches />
    </React.Fragment>
  );
}

ReactDOM.render(<App />, document.querySelector("#ReactApp"));

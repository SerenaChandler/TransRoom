function App() {
  const [matchesData, setMatchesData] = React.useState([]);
  const [displayMatches, setDisplayMatches] = React.useState([]);

  function MatchCard(props) {
    return (
      <div className="match">
        <p>Username: {props.username}</p>
      </div>
    );
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
    const matchList = []
    for (let match of matchesData){
      matchList.push(
        <MatchCard
        key={match.id}
        username={match.username}

        />
      )
    }
    setDisplayMatches(matchList)

  }




  function checkState() {
    console.log(matchesData);
  }

  return (
    <React.Fragment>
      <MatchButton checkState={showMatches}  />
    </React.Fragment>
  );
}

function MatchButton(props) {
  return <button onClick={props.checkState}>Click Here</button>;
}

ReactDOM.render(<App />, document.querySelector("#ReactApp"));

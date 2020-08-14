import React, { Component } from "react";
import Title from "./components/title";
import Description from "./components/description";
import Button from "./components/button";
import Select from "./components/select";
import GithubCorner from "react-github-corner";

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      fighters: [],
      fighter1: null,
      fighter2: null,
      prediction: null,
      shouldShowPrediction: false,
    };
  }

  componentDidMount = () => {
    this.getFighters();
  };

  getFighters = async () => {
    const query = "https://bjj.ryanlongtran.com/fighters";
    const res = await fetch(query);

    // Get all fighters in alphabetical
    res.json().then((res) => {
      res.sort((a, b) => a["first_name"].localeCompare(b["first_name"]));
      this.setState({ fighters: res, fighter1: res[0], fighter2: res[0] });
    });
  };

  handleSelect = (e) => {
    // Update fighter info based on selection and hide prediction results
    this.setState({
      [e.target.id]: this.state.fighters[e.target.selectedIndex],
      shouldShowPrediction: false,
    });
  };

  predict = async (e) => {
    e.target.blur();

    const query =
      "https://bjj.ryanlongtran.com/predict?id_1=" +
      this.state.fighter1["id"] +
      "&id_2=" +
      this.state.fighter2["id"];
    const res = await fetch(query);

    // Get prediction and show it
    res.json().then((res) => {
      this.setState({
        prediction: res,
        shouldShowPrediction: true,
      });
    });
  };

  getFighterInfo = (fighter) => {
    let fighterInfo = <React.Fragment></React.Fragment>;

    // Fighter is not null
    if (fighter) {
      const firstName = fighter["first_name"];
      const nickname = fighter["nickname"];
      const lastName = fighter["last_name"];
      const team = fighter["team"];
      const wins = fighter["wins"];
      const winsBySub = fighter["wins_by_sub"];
      const losses = fighter["losses"];
      const lossesBySub = fighter["losses_by_sub"];

      const winsBySubPercent =
        wins > 0 ? ((winsBySub / wins) * 100).toFixed(1) : 0;
      const lossesBySubPercent =
        losses > 0 ? ((lossesBySub / losses) * 100).toFixed(1) : 0;
      const winRate = ((100 * wins) / (wins + losses)).toFixed(1);

      fighterInfo = (
        <React.Fragment>
          <a
            rel="noopener noreferrer"
            target="_blank"
            href={"https://www.bjjheroes.com/bjj-fighters/?p=" + fighter["id"]}
          >
            <h4 className="font-weight-bold">
              {firstName}
              {nickname ? ' "' + nickname + '"' : ""}
              {" " + lastName}
            </h4>
          </a>
          <h5>{team ? team : ""}</h5>
          <h5>
            {wins} wins, {winsBySub} by submission ({winsBySubPercent}%)
          </h5>
          <h5>
            {losses} losses, {lossesBySub} by submission ({lossesBySubPercent}%)
          </h5>
          <h5>{winRate}% win rate</h5>
        </React.Fragment>
      );
    }
    return fighterInfo;
  };

  getFighterNameStr = (fighter) => {
    return (
      fighter["first_name"] +
      (fighter["nickname"] ? ' "' + fighter["nickname"] + '"' : "") +
      " " +
      fighter["last_name"]
    );
  };

  getFighterLink = (fighter) => {
    return (
      <a
        rel="noopener noreferrer"
        target="_blank"
        href={"https://www.bjjheroes.com/bjj-fighters/?p=" + fighter["id"]}
      >
        {this.getFighterNameStr(fighter)}
      </a>
    );
  };

  getPredictionInfo = () => {
    let predictionInfo = <div className="pb-5"></div>;

    // Prediction is not null
    if (this.state.shouldShowPrediction) {
      // Results are with respect to the fighter 1
      const vsHistory = this.state.prediction["vs_history"];

      let winBySub = parseFloat(this.state.prediction["win_by_sub"]);
      let winByOther = parseFloat(this.state.prediction["win_by_other"]);
      let totalWin = winBySub + winByOther;

      let lossBySub = parseFloat(this.state.prediction["loss_by_sub"]);
      let lossByOther = parseFloat(this.state.prediction["loss_by_other"]);
      let totalLoss = lossBySub + lossByOther;

      let draw = parseFloat(this.state.prediction["draw"]);

      let winner;
      if (draw >= totalWin && draw >= totalLoss) {
        winner = (
          <React.Fragment>
            DRAW (the following probabilities are for{" "}
            {this.getFighterLink(this.state.fighter1)})
          </React.Fragment>
        );
      } else if (totalWin > totalLoss) {
        winner = this.getFighterLink(this.state.fighter1);
      } else {
        winner = this.getFighterLink(this.state.fighter2);

        // Swap stats because fighter 2 is winner
        let temp = totalWin;
        totalWin = totalLoss;
        totalLoss = temp;

        temp = winBySub;
        winBySub = lossBySub;
        lossBySub = temp;

        temp = winByOther;
        winByOther = lossByOther;
        lossByOther = temp;
      }

      // Format to percentages with one decimal
      totalWin = (totalWin * 100).toFixed(1);
      winBySub = (winBySub * 100).toFixed(1);
      winByOther = (winByOther * 100).toFixed(1);
      totalLoss = (totalLoss * 100).toFixed(1);
      lossBySub = (lossBySub * 100).toFixed(1);
      lossByOther = (lossByOther * 100).toFixed(1);
      draw = (draw * 100).toFixed(1);

      // VS history
      let vsWins = 0;
      let vsLosses = 0;
      let vsDraws = 0;

      let history = <React.Fragment></React.Fragment>;
      if (vsHistory.length > 0) {
        // Sort history by competition year
        vsHistory.sort((a, b) => a["year"].localeCompare(b["year"]));

        history = vsHistory.map((fight) => {
          let fightWinner;
          if (fight["win_loss"] === "W") {
            fightWinner = this.getFighterLink(this.state.fighter1);
            vsWins++;
          } else if (fight["win_loss"] === "L") {
            fightWinner = this.getFighterLink(this.state.fighter2);
            vsLosses++;
          } else {
            fightWinner = "DRAW";
            vsDraws++;
          }

          return (
            <tr key={fight["competition"] + fight["year"]}>
              <td>{fightWinner}</td>
              <td>{fight["method"]}</td>
              <td>{fight["competition"]}</td>
              <td>{fight["weight"]}</td>
              <td>{fight["stage"]}</td>
              <td>{fight["year"]}</td>
            </tr>
          );
        });
      }

      let historySummary;
      if (vsHistory.length === 0) {
        historySummary = "No VS history";
      } else {
        if (vsWins === vsLosses) {
          historySummary =
            "Fighters are tied " +
            vsWins +
            "-" +
            vsLosses +
            "-" +
            vsDraws +
            " (W-L-D)";
        } else {
          historySummary = (
            <span>
              {this.getFighterLink(
                vsWins > vsLosses ? this.state.fighter1 : this.state.fighter2
              )}{" "}
              leads{" "}
              {this.getFighterLink(
                vsWins > vsLosses ? this.state.fighter2 : this.state.fighter1
              )}{" "}
              {vsWins > vsLosses ? vsWins : vsLosses}-
              {vsWins > vsLosses ? vsLosses : vsWins}-{vsDraws} (W-L-D)
            </span>
          );
        }
      }

      predictionInfo = (
        <React.Fragment>
          <div className="row justify-content-center pt-5">
            <div className="col">
              <h4 className="font-weight-bold">Winner: {winner}</h4>
            </div>
          </div>
          <div className="row justify-content-center pt-3">
            <div className="col col-lg-6 col-12">
              <h5>P(win): {totalWin}%</h5>
              <h5>P(win by submission): {winBySub}%</h5>
              <h5>P(win by other): {winByOther}%</h5>
            </div>
            <div className="col col-lg-6 col-12">
              <h5>P(lose): {totalLoss}%</h5>
              <h5>P(lose by submission): {lossBySub}%</h5>
              <h5>P(lose by other): {lossByOther}%</h5>
            </div>
          </div>
          <div className="row justify-content-center">
            <div className="col">
              <h5>P(draw): {draw}%</h5>
            </div>
          </div>
          <div className="row justify-content-center pt-5 pb-3">
            <div className="col">
              <h5>{historySummary}</h5>
            </div>
          </div>
          <div className="row justify-content-center pb-5">
            <div className="col">
              <div className="table-responsive">
                <table className="table table-striped table-hover text-left">
                  <thead>
                    <tr>
                      <th>Winner</th>
                      <th>Method</th>
                      <th>Competition</th>
                      <th>Weight</th>
                      <th>Stage</th>
                      <th>Year</th>
                    </tr>
                  </thead>
                  <tbody>{history}</tbody>
                </table>
              </div>
            </div>
          </div>
        </React.Fragment>
      );
    }
    return predictionInfo;
  };

  render() {
    return (
      <div className="App container text-center pt-5">
        <div className="row">
          <div className="col">
            <Title text="BJJ Predictor" />
          </div>
        </div>
        <div className="row">
          <div className="col">
            <Description
              text={
                "Choose two fighters and predict who would win in a BJJ match!"
              }
            />
          </div>
        </div>
        <div className="row justify-content-center pt-5">
          <div className="col col-lg-4 col-12">
            <div className="row">
              <div className="col">
                <Select
                  fighters={this.state.fighters}
                  onChange={this.handleSelect}
                  id="fighter1"
                />
              </div>
            </div>
            <div className="row pt-3">
              <div className="col">
                {this.getFighterInfo(this.state.fighter1)}
              </div>
            </div>
          </div>
          <div className="col col-lg-1 col-12 align-self-center">
            <h1 className="font-weight-bold">VS</h1>
          </div>
          <div className="col col-lg-4 col-12">
            <div className="row">
              <div className="col">
                <Select
                  fighters={this.state.fighters}
                  onChange={this.handleSelect}
                  id="fighter2"
                />
              </div>
            </div>
            <div className="row pt-3">
              <div className="col">
                {this.getFighterInfo(this.state.fighter2)}
              </div>
            </div>
          </div>
        </div>
        <div className="row justify-content-center pt-3">
          <div className="col">
            <Button value="Predict" onClick={this.predict} />
          </div>
        </div>
        {this.getPredictionInfo()}
        <GithubCorner
          href="https://github.com/ryantran2165/bjj-predictor"
          bannerColor="#222"
          octoColor="#7fffd4"
          target="_blank"
        />
      </div>
    );
  }
}

export default App;

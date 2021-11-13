import "./styles/index.scss";
import React, { Router } from "@reach/router";
import Homepage from "./views/Homepage";
import Result from "./views/Result";

function App() {
  return (
    <div className="App">
      <Router>
        <Homepage path="/" />
        <Result path="/result" to="/" />
      </Router>
    </div>
  );
}

export default App;

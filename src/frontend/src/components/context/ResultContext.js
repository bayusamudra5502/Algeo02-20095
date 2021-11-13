import React, { createContext, useState } from "react";

const ResultContext = createContext();

export function ResultProvider({ children }) {
  const [level, setLevel] = useState(100);
  const [alpha, setAlpha] = useState(false);
  const [tiles, setTiles] = useState(false);

  return (
    <ResultContext.Provider
      value={{ level, setLevel, alpha, setAlpha, tiles, setTiles }}
    >
      {children}
    </ResultContext.Provider>
  );
}

export default ResultContext;

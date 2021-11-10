import React, { createContext, useState } from "react";

const ConnectionContext = createContext();

export function ConnectionProvider({ children }) {
  const [isConnected, setConnect] = useState(false);
  const [serverState, setServerState] = useState({});

  return (
    <ConnectionContext.Provider
      value={{ isConnected, setConnect, serverState, setServerState }}
    >
      {children}
    </ConnectionContext.Provider>
  );
}

export default ConnectionContext;

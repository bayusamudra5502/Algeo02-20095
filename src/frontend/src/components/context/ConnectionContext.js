import React, { createContext, useState } from "react";

const ConnectionContext = createContext();

export function ConnectionProvider({ children }) {
  const [isConnected, setConnect] = useState(false);

  return (
    <ConnectionContext.Provider value={{ isConnected, setConnect }}>
      {children}
    </ConnectionContext.Provider>
  );
}

export default ConnectionContext;

import React, { createContext, useContext, useEffect, useReducer } from "react";
import ConnectionContext from "../../components/context/ConnectionContext";

const SocketContext = createContext();

function reducer(state, action) {
  return { ...state, ...action };
}

export function SocketProvider({ children }) {
  const [connectState, dispatchConnect] = useReducer(reducer, {
    connected: false,
  });
  const { setConnect } = useContext(ConnectionContext);

  useEffect(() => {
    setConnect(!!connectState?.connected);
  }, [connectState, setConnect]);

  return (
    <SocketContext.Provider value={{ connectState, dispatchConnect }}>
      {children}
    </SocketContext.Provider>
  );
}

export default SocketContext;

import React, { createContext, useState } from "react";

const ProcessContext = createContext();

export function ProcessProvider({ children }) {
  const [compressState, setCompressState] = useState({
    isCompressing: false,
    progress: 0,
  });

  return (
    <ProcessContext.Provider value={{ compressState, setCompressState }}>
      {children}
    </ProcessContext.Provider>
  );
}

export default ProcessContext;

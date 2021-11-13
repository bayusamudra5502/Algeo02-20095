import React, { createContext, useState } from "react";

const UploadContext = createContext();

export function UploadProvider({ children }) {
  const [isCacheAlpha, setCacheAlpha] = useState(false);

  return (
    <UploadContext.Provider value={{ isCacheAlpha, setCacheAlpha }}>
      {children}
    </UploadContext.Provider>
  );
}

export default UploadContext;

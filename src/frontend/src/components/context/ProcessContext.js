import React, { createContext, useState } from "react";

const ProcessContext = createContext();

export function ProcessProvider({ children }) {
  const [isUploading, setUploadState] = useState(false);
  const [compressState, setCompressState] = useState({
    isCompressing: false,
    progress: 0,
  });

  return (
    <ProcessContext.Provider
      value={{ isUploading, setUploadState, compressState, setCompressState }}
    >
      {children}
    </ProcessContext.Provider>
  );
}

export default ProcessContext;

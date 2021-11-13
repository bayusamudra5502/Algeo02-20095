import React, { createContext, useReducer } from "react";

const ProcessContext = createContext();

function reducer(state, action) {
  return { ...state, ...action };
}

export function ProcessProvider({ children }) {
  const [uploadState, setUploadState] = useReducer(reducer, {
    isUploadComplete: false,
    isUploading: false,
    progress: 0,
  });

  const [compressState, setCompressState] = useReducer(reducer, {
    isCompressing: false,
    isCompressComplete: false,
    progress: 0,
  });

  const resetUpload = () => {
    setUploadState({
      isUploadComplete: false,
      isUploading: false,
      progress: 0,
    });
  };

  const resetCompress = () => {
    setCompressState({
      isCompressing: false,
      isCompressComplete: false,
      progress: 0,
    });
  };

  return (
    <ProcessContext.Provider
      value={{
        uploadState,
        setUploadState,
        compressState,
        setCompressState,
        resetUpload,
        resetCompress,
      }}
    >
      {children}
    </ProcessContext.Provider>
  );
}

export default ProcessContext;

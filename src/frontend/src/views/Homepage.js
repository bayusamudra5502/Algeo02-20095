import React, { useContext } from "react";
import ProcessContext from "../components/context/ProcessContext";
import Decomposition from "../components/Decomposition";
import Title from "../components/Title";
import UploadArea from "../components/UploaderArea";

export default function Homepage() {
  const { uploadState } = useContext(ProcessContext);
  return (
    <main>
      <Title></Title>
      <UploadArea />
      {uploadState.isUploadComplete && <Decomposition />}
    </main>
  );
}

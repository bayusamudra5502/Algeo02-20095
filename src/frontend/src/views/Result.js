import React, { useContext, useEffect } from "react";
import Image from "../components/Image";
import Settings from "../components/Settings";
import ResultContext from "../components/context/ResultContext";
import SocketContext from "../service/context/SocketContext";
import ProcessContext from "../components/context/ProcessContext";
import ConnectionContext from "../components/context/ConnectionContext";
import { navigate } from "@reach/router";

export default function Result() {
  const { alpha, level } = useContext(ResultContext);
  const { compressState } = useContext(ProcessContext);
  const { isConnected } = useContext(ConnectionContext);
  const {
    connectState: { server },
  } = useContext(SocketContext);

  const imageUrl = () => {
    if (alpha) {
      return `${server}/compress/${level}/?alpha=1`;
    } else {
      return `${server}/compress/${level}/`;
    }
  };

  useEffect(() => {
    if (!compressState?.isCompressComplete && !isConnected) {
      navigate("/");
    }
  }, [compressState, isConnected]);

  return (
    <main style={{ flexDirection: "column" }}>
      <Settings />
      <div className="result-container">
        <Image
          src={`${server}/compress/100/`}
          alt="Original"
          grid={true}
          title="Original"
        />
        <Image
          src={imageUrl()}
          alt="Hasil Kompresi"
          grid={true}
          title="Hasil Kompresi"
        />
      </div>
    </main>
  );
}

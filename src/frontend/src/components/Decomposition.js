import { navigate } from "@reach/router";
import React, { useContext, useEffect, useRef, useState } from "react";
import { BsGear } from "react-icons/bs";
import { CSSTransition } from "react-transition-group";
import SocketContext from "../service/context/SocketContext";
import MessageContext from "./context/MessageContext";
import ProcessContext from "./context/ProcessContext";
import Progress from "./Progress";

export default function Decomposition() {
  const { uploadState, compressState, setCompressState, resetCompress } =
    useContext(ProcessContext);

  const { showMessage } = useContext(MessageContext);

  const rgba = useRef({
    R: 0,
    G: 0,
    B: 0,
    A: 0,
  });

  const [text, setText] = useState("Menunggu proses dimulai...");

  const {
    connectState: {
      helper: { buildMatrix },
      progress = {},
    },
  } = useContext(SocketContext);

  useEffect(() => {
    setTimeout(() => {
      if (!compressState.isCompressing) {
        resetCompress();
        buildMatrix();
        setCompressState({
          isCompressing: true,
        });
      }
    }, 500);
  }, []);

  useEffect(() => {
    if (progress.value) {
      const { value, comment } = progress;
      setText(comment);

      if (value.func === 0) {
        if (value.progress < 1) {
          setCompressState({
            progress: value.progress,
          });
        } else {
          setCompressState({
            isCompressing: false,
            progress: value.progress,
            isCompressComplete: true,
          });

          showMessage("Gambar berhasil didekomposisi", "success");

          navigate("/result");
        }
      } else {
        rgba.current[value.channel] = value.value;

        const sum =
          rgba.current["R"] +
          rgba.current["G"] +
          rgba.current["B"] +
          rgba.current["A"];

        setCompressState({
          progress: 0.1 + 0.9 * (sum / 4),
        });
      }
    }
  }, [progress]);

  return (
    <CSSTransition
      in={uploadState.isUploadComplete}
      timeout={300}
      classNames="fade"
      unmountOnExit
    >
      <div className="right-container">
        <div className="icon spinning">
          <BsGear />
        </div>
        <p className="h5">Membentuk Matriks</p>
        <p>Tunggu yaa, kita lagi buat dekomposisinya dulu</p>
        <div className="progress-bar-container">
          <Progress value={compressState.progress} animated={true} />
          <div className="d-flex justify-content-between mt-2">
            <p>{text}</p>
            <p>{(compressState.progress * 100).toFixed(2)}%</p>
          </div>
        </div>
      </div>
    </CSSTransition>
  );
}

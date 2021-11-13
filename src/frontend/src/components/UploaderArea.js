import React, { useContext, useMemo } from "react";
import { useDropzone } from "react-dropzone";
import { FiInbox, FiAlertOctagon, FiArrowDown } from "react-icons/fi";
import { BsCloudSlash } from "react-icons/bs";
import ConnectionContext from "./context/ConnectionContext";
import ProcessContext from "./context/ProcessContext";
import { AiOutlineCloudUpload } from "react-icons/ai";
import Progress from "./Progress";
import { sendImage } from "../service";
import SocketContext from "../service/context/SocketContext";
import MessageContext from "./context/MessageContext";
import { CSSTransition } from "react-transition-group";

export default function UploadArea() {
  const { uploadState, setUploadState, resetUpload } =
    useContext(ProcessContext);
  const {
    connectState: { server, userid },
  } = useContext(SocketContext);
  const { showMessage } = useContext(MessageContext);

  const onDropAccepted = function (acceptedFile) {
    resetUpload();

    console.log(server);

    sendImage(server, userid, acceptedFile[0], (progress) => {
      setUploadState({
        progress,
      });
    })
      .then((result) => {
        if (result) {
          setUploadState({
            isUploading: false,
            isUploadComplete: true,
          });

          showMessage("Gambar berhasil diupload", "success");
        } else {
          setUploadState({
            isUploading: false,
            isUploadComplete: false,
          });

          showMessage("Terjadi kesalahan saat mengupload", "error");
        }
      })
      .catch(() => {
        setUploadState({
          isUploading: false,
          isUploadComplete: false,
        });

        showMessage("Terjadi kesalahan saat mengupload", "error");
      });
  };

  const { isConnected } = useContext(ConnectionContext);

  const { getRootProps, getInputProps, isDragActive, isDragReject } =
    useDropzone({
      onDropAccepted,
      accept: "image/png, image/jpeg, image/jpg",
      maxFiles: 1,
    });

  const className = useMemo(() => {
    if (isDragReject) {
      return "uploader-container drag-reject";
    } else if (isDragActive) {
      return "uploader-container drag-active";
    } else {
      return "uploader-container";
    }
  }, [isDragActive, isDragReject]);

  const pesan = useMemo(() => {
    if (isDragReject) {
      return (
        <>
          <div className="icon">
            <FiAlertOctagon />
          </div>
          <p className="h6">Format file tidak diizinikan.</p>
          <p>
            Masukan yang diperbolehkan hanya file <code>.jpg</code>,{" "}
            <code>.jpeg</code>, atau <code>.png</code>
          </p>
        </>
      );
    } else if (isDragActive) {
      return (
        <>
          <div className="icon">
            <FiArrowDown />
          </div>
          <p className="h5">Lepas file disini</p>
        </>
      );
    } else {
      return (
        <>
          <div className="icon">
            <FiInbox />
          </div>
          <p className="h5">Letakan file disini...</p>
          <p>atau kalau mau klik disini juga boleh</p>
        </>
      );
    }
  }, [isDragActive, isDragReject]);

  return (
    <div className="upload-container-outer">
      {!(uploadState.isUploading || uploadState.isUploadComplete) && (
        <>
          <CSSTransition
            in={!isConnected}
            timeout={300}
            classNames="no-connection"
            unmountOnExit
          >
            <div className="overlay">
              <div className="text">
                <div className="icon">
                  <BsCloudSlash />
                </div>
                <p className="h5">Anda belum tersambung</p>
                <p>Silahkan sambungkan program ini sebelum mengupload gambar</p>
              </div>
            </div>
          </CSSTransition>

          <div {...getRootProps({ className })}>
            <input {...getInputProps()} />
            {pesan}
          </div>
        </>
      )}
      <CSSTransition
        in={uploadState.isUploading}
        timeout={300}
        classNames="fade"
        unmountOnExit
      >
        <div className="right-container">
          <div className="icon">
            <AiOutlineCloudUpload />
          </div>
          <p className="h5">Sedang megupload</p>
          <p>Tunggu yaa, kita lagi mengupload dulu..</p>
          <div className="progress-bar-container">
            <Progress value={uploadState.progress} animated={true} />
            <div className="d-flex justify-content-between mt-2">
              <p>
                {uploadState.progress < 1
                  ? "Mengupload Gambar..."
                  : "Mengkonversi gambar menjadi matriks..."}
              </p>
              <p>{(uploadState.progress * 100).toFixed(2)}%</p>
            </div>
          </div>
        </div>
      </CSSTransition>
    </div>
  );
}

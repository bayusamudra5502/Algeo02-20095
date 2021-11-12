import { useContext, useMemo } from "react";
import { useDropzone } from "react-dropzone";
import { FiInbox, FiAlertOctagon, FiArrowDown } from "react-icons/fi";
import { BsCloudSlash } from "react-icons/bs";
import ConnectionContext from "./context/ConnectionContext";

export default function UploadArea({ onFileLoaded }) {
  const onDropAccepted = function (acceptedFile) {
    console.dir(acceptedFile);
    onFileLoaded && onFileLoaded(acceptedFile[0]);
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
      {!isConnected && (
        <div className="overlay">
          <div className="text">
            <div className="icon">
              <BsCloudSlash />
            </div>
            <p className="h5">Anda belum tersambung</p>
            <p>Silahkan sambungkan program ini sebelum mengupload gambar</p>
          </div>
        </div>
      )}
      <div {...getRootProps({ className })}>
        <input {...getInputProps()} />
        {pesan}
      </div>
    </div>
  );
}

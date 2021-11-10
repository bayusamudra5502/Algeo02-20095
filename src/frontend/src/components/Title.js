import picture from "../assets/pictures.png";
import Progress from "./Progress";
import { Modal } from "react-bootstrap";
import { useContext, useState } from "react";
import ConnectionContext from "./context/ConnectionContext";
import ProcessContext from "./context/ProcessContext";
import ConnectComponent from "./Connect";

export default function Title() {
  const [showAbout, setAbout] = useState(false);
  const { isConnected, setConnect } = useContext(ConnectionContext);
  const { compressState } = useContext(ProcessContext);

  const handleClose = () => setAbout(false);
  const handleOpen = () => setAbout(true);

  const onConnected = () => {
    setConnect(true);
  };

  return (
    <>
      <div className="title">
        <div className="picture">
          <img src={picture} alt="Gambar"></img>
        </div>
        <div>
          <h1 className="h2">Image Compressor</h1>
          <p>Yuk buat ukuran file gambar lebih kecil</p>
        </div>
        <div className="status">
          <h2 className="sub-judul">Koneksi</h2>
          <div>
            <span
              className={
                "statusbar " + (isConnected ? "connected" : "disconnected")
              }
            ></span>
            {isConnected ? "Tersambung" : "Tidak Tersambung"}
            {!isConnected ? <ConnectComponent onConnected={onConnected} /> : ""}
          </div>
        </div>
        {compressState.isCompressing ? (
          <div>
            <h2 className="sub-judul">Proses Kompresi</h2>
            <Progress value={compressState.progress} animated={true}></Progress>
          </div>
        ) : (
          ""
        )}
        <div className="bottom">
          <h2 className="sub-judul">Tentang Program ini</h2>
          <p>Program ini dibuat oleh kelompok X</p>
          <p>
            Lihat informasi lengkap{" "}
            <button className="button-link" onClick={handleOpen}>
              disini
            </button>
            .
          </p>
        </div>
      </div>
      <Modal show={showAbout} centered onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>Tentang Kami</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <div className="header">
            <div className="picture">
              <img src={picture} alt="Gambar"></img>
            </div>
            <h1 className="h2 text-center my-2">Image Compressor</h1>
            <p className="h5 text-center text-muted">Versi 1.0.0</p>
          </div>
          <div className="kontributor">
            <h2 className="sub-judul">Kontributor</h2>
            <ul>
              <li>Firizky Ardiansyah (13520095)</li>
              <li>Bayu Samudra (13520128)</li>
              <li>Ikmal Alfaozi (13520125)</li>
            </ul>
          </div>
          <div>
            <h2 className="sub-judul">Deskripsi Singkat</h2>
            <p>
              Kompresi gambar merupakan suatu tipe kompresi data yang dilakukan
              pada gambar digital. Dengan kompresi gambar, suatu file gambar
              digital dapat dikurangi ukuran filenya dengan baik tanpa
              mempengaruhi kualitas gambar secara signifikan. Terdapat berbagai
              metode dan algoritma yang digunakan untuk kompresi gambar pada
              zaman modern ini
            </p>
            <p>
              {" "}
              Salah satu algoritma yang dapat digunakan untuk kompresi gambar
              adalah algoritma SVD (Singular Value Decomposition). Algoritma SVD
              didasarkan pada teorema dalam aljabar linier yang menyatakan bahwa
              sebuah matriks dua dimensi dapat dipecah menjadi hasil perkalian
              dari 3 sub-matriks yaitu matriks ortogonal U, matriks diagonal S,
              dan transpose dari matriks ortogonal V.{" "}
            </p>
          </div>
        </Modal.Body>
      </Modal>
    </>
  );
}

import React, { useContext, useState } from "react";
import { Modal } from "react-bootstrap";
import { AiOutlineExpand } from "react-icons/ai";
import ResultContext from "./context/ResultContext";

export default function Image({ src, alt, title }) {
  const { tiles: grid } = useContext(ResultContext);
  const [showModal, setShowModal] = useState(false);

  return (
    <>
      <div className="display-image">
        <div>
          <h2 className="sub-judul">{title}</h2>
        </div>
        <div className={"image" + (grid ? " show-grid" : "")}>
          <div>
            <img src={src} alt={alt} />
          </div>
          <button className="layer" onClick={() => setShowModal(true)}>
            <div className="icon">
              <AiOutlineExpand />
            </div>
            <p className="h4">Tampilkan ukuran asli</p>
          </button>
        </div>
      </div>
      <Modal
        show={showModal}
        fullscreen={true}
        onHide={() => setShowModal(false)}
      >
        <Modal.Header closeButton>
          <Modal.Title>Gambar ukuran asli</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <div
            className={
              "d-flex w-100 align-item-center h-100 justify-content-center" +
              (grid ? " show-grid" : "")
            }
          >
            <img src={src} alt={alt} />
          </div>
        </Modal.Body>
      </Modal>
    </>
  );
}

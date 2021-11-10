import { useState } from "react";
import { Form, Modal, OverlayTrigger, Tooltip } from "react-bootstrap";
import plug from "../assets/plug.png";

export default function ConnectComponent({ onConnected }) {
  const [isOpened, setOpen] = useState(false);
  const [ipaddr, setIpAddr] = useState("");
  const [port, setPort] = useState("");

  const onConnecting = async function (e) {
    e.preventDefault();
    const serverData = { ip: ipaddr, port };

    console.dir(serverData);

    onConnected && onConnected();
    onClose();
    return true;
  };

  function onClose() {
    setPort("");
    setIpAddr("");
    setOpen(false);
  }

  return (
    <>
      <OverlayTrigger
        placement="bottom"
        overlay={<Tooltip id="connect-tooltip">Sambungkan Koneksi</Tooltip>}
      >
        <button className="connect-plug" onClick={() => setOpen(true)}>
          <img src={plug} alt="Connection Plug"></img>
        </button>
      </OverlayTrigger>
      <Modal show={isOpened} centered onHide={onClose}>
        <Modal.Header closeButton>
          <Modal.Title>Server Config</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <p>Silahkan masukan konfigurasi server anda</p>
          <div>
            <Form onSubmit={onConnecting}>
              <Form.Group className="mb-3">
                <Form.Label>IP Address</Form.Label>
                <Form.Control
                  placeholder="127.0.0.1"
                  required
                  value={ipaddr}
                  onInput={(e) => {
                    setIpAddr(e.target.value);
                  }}
                />
              </Form.Group>
              <Form.Group className="mb-3">
                <Form.Label>Port</Form.Label>
                <Form.Control
                  type="number"
                  placeholder="5502"
                  required
                  value={port}
                  onInput={(e) => {
                    setPort(e.target.value);
                  }}
                />
              </Form.Group>
              <Form.Group>
                <button className="btn btn-primary">Submit</button>
              </Form.Group>
            </Form>
          </div>
        </Modal.Body>
      </Modal>
    </>
  );
}

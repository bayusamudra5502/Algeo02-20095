import React, { useContext, useEffect, useState } from "react";
import {
  Alert,
  Col,
  FloatingLabel,
  Form,
  Modal,
  OverlayTrigger,
  Row,
  Tooltip,
} from "react-bootstrap";
import plug from "../assets/plug.png";
import { defaultServer } from "../config.json";
import { getStatus } from "../service";
import SocketContext from "../service/context/SocketContext";
import MessageContext from "./context/MessageContext";
import connectSocket from "../service/socket";

export default function ConnectComponent({ onConnected }) {
  const [isOpened, setOpen] = useState(false);
  const [isLoading, setLoading] = useState(false);
  const [ipaddr, setIpAddr] = useState("");
  const [port, setPort] = useState("");
  const [option, setOption] = useState(-1);
  const [serverState, setServerState] = useState(0);

  const { dispatchConnect } = useContext(SocketContext);

  const { showMessage } = useContext(MessageContext);

  function onClose() {
    setPort("");
    setIpAddr("");
    setOpen(false);
  }

  function onOptionChange(value) {
    setOption(value);

    if (value === 0) {
      setPort("443");
      setIpAddr(defaultServer);
    } else {
      setPort("");
      setIpAddr("");
    }
  }

  const onConnecting = async function (e) {
    setLoading(true);
    e.preventDefault();

    const regex = /https?:\/\/.*/;
    let url = ipaddr;

    if (!regex.test(url)) {
      url = "http://" + url;
    }

    if (await getStatus(`${url}:${port}`)) {
      await connectSocket(`${url}:${port}`, dispatchConnect, (response) => {
        if (response.success) {
          onConnected && onConnected();
          showMessage("Berhasil tersambung", "success");
        } else {
          showMessage("Gagal menyambungkan socket", "error");
        }
      });

      onClose();
    } else {
      showMessage("Server saat ini tidak bisa digunakan", "error");
    }

    setLoading(false);
    return true;
  };

  useEffect(() => {
    if (isOpened) {
      (async () => {
        setServerState(0);
        const serverState = await getStatus(defaultServer + ":443");

        if (serverState) {
          setServerState(1);
        } else {
          setServerState(-1);
        }
      })();
    }
  }, [isOpened]);

  function overlayStatus() {
    if (serverState === 0) {
      return (
        <Tooltip id="isConnecting-tooltip">Menghubungkan ke server...</Tooltip>
      );
    } else if (serverState === 1) {
      return <Tooltip id="isAvailable-tooltip">Server tersedia</Tooltip>;
    } else {
      return (
        <Tooltip id="isNotAvailable-tooltip">Server tidak tersedia</Tooltip>
      );
    }
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

      {/* Bootstap Modal */}
      <Modal show={isOpened} centered onHide={onClose}>
        <Modal.Header closeButton>
          <Modal.Title>Konfigurasi Server</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Alert variant="info">
            Server lokal bisa anda dapatkan{" "}
            <a
              href="https://github.com/bayusamudra5502/Algeo02-20095"
              target="_blank"
              rel="noreferrer"
            >
              disini
            </a>
          </Alert>
          <div className="mb-3">
            <h2 className="h6">Pilihan server</h2>
            <Form.Check
              type="radio"
              id="default"
              name="server"
              value={0}
              disabled={serverState === -1}
              onChange={() => onOptionChange(0)}
              checked={option === 0}
              label={
                <>
                  Gunakan server default{" "}
                  <OverlayTrigger placement="bottom" overlay={overlayStatus()}>
                    <span
                      className={(() => {
                        if (serverState === 0) {
                          return "connecting connect-status";
                        } else if (serverState === -1) {
                          return "disconnected connect-status";
                        } else {
                          return "connected connect-status";
                        }
                      })()}
                    ></span>
                  </OverlayTrigger>
                </>
              }
            />
            <Form.Check
              type="radio"
              name="server"
              id="local"
              value={1}
              checked={option === 1}
              onChange={() => onOptionChange(1)}
              label="Gunakan server lokal"
            />
          </div>
          <div>
            <Form onSubmit={onConnecting}>
              {option === 1 && (
                <>
                  <h2 className="h6">Konfigurasi server lokal</h2>
                  <Form.Group className="mb-4">
                    <Row>
                      <Col>
                        <FloatingLabel label="Server">
                          <Form.Control
                            placeholder="127.0.0.1"
                            pattern="(https?://)?[A-Za-z0-9.]+"
                            required
                            value={ipaddr}
                            onInput={(e) => {
                              setIpAddr(e.target.value);
                            }}
                          />
                        </FloatingLabel>
                      </Col>
                      <Col xs={4}>
                        <FloatingLabel label="Port">
                          <Form.Control
                            type="number"
                            placeholder="8080"
                            required
                            value={port}
                            onInput={(e) => {
                              setPort(e.target.value);
                            }}
                          />
                        </FloatingLabel>
                      </Col>
                    </Row>
                  </Form.Group>
                </>
              )}
              <Form.Group>
                <button disabled={isLoading} className="btn btn-success">
                  Connect
                </button>
              </Form.Group>
            </Form>
          </div>
        </Modal.Body>
      </Modal>
    </>
  );
}

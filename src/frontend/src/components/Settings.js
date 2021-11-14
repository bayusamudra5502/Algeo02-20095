import React, { useContext, useEffect, useState } from "react";
import { Col, Form, Row } from "react-bootstrap";
import picture from "../assets/pictures.png";
import { getStatusCompress } from "../service";
import SocketContext from "../service/context/SocketContext";
import ConnectionContext from "./context/ConnectionContext";
import ResultContext from "./context/ResultContext";
import UploadContext from "./context/UploadContext";

export default function Settings() {
  const { isConnected } = useContext(ConnectionContext);
  const { level, setLevel, alpha, setAlpha, tiles, setTiles } =
    useContext(ResultContext);
  const {
    connectState: { server },
  } = useContext(SocketContext);

  const [executionTime, setExecutionTime] = useState(0);
  const [compressLevel, setCompressLevel] = useState(0);

  const { isCacheAlpha } = useContext(UploadContext);

  const imageUrl = () => {
    if (alpha) {
      return `${server}/compress/${level}/download?alpha=1`;
    } else {
      return `${server}/compress/${level}/download`;
    }
  };

  useEffect(() => {
    (async function () {
      const { executionTime, compress } = await getStatusCompress(
        server,
        level
      );
      console.log(executionTime);
      console.log(compress);

      setExecutionTime(executionTime);
      setCompressLevel(compress);
    })();
  }, [level]);

  function getTime() {
    if (executionTime < 1_000_000) {
      return `${executionTime} ns`;
    } else if (executionTime < 1_000_000_000) {
      const time = executionTime / 1_000_000;
      return `${time.toFixed(3)} ms`;
    } else if (executionTime < 1_000_000_000 * 60) {
      const time = executionTime / 1_000_000_000;
      return `${time.toFixed(3)} detik`;
    } else if (executionTime < 1_000_000_000 * 3600) {
      const s = Math.round(executionTime / 1_000_000_000);
      const m = Math.floor(s / 60);
      return `${m} menit ${s % 60} detik`;
    } else {
      const s = Math.round(executionTime / 1_000_000_000);
      const h = Math.floor(s / 3600);
      const m = Math.floor((s % 3600) / 60);
      return `${h} jam ${m} menit ${s} detik `;
    }
  }

  return (
    <div className="result">
      <div className="title-result">
        <div className="picture">
          <img src={picture} alt="Gambar"></img>
        </div>
        <div>
          <h1 className="h4">Image Compressor</h1>
          <p>Yuk lihat hasil kompresi gambarnya</p>
        </div>
      </div>
      <div className="configuration">
        <div>
          <div className="status mb-2">
            <h2 className="sub-judul">Koneksi</h2>
            <div>
              <span
                className={
                  "statusbar " + (isConnected ? "connected" : "disconnected")
                }
              ></span>
              {isConnected ? "Tersambung" : "Tidak Tersambung"}
            </div>
          </div>
          <div className="mb-2">
            <h2 className="sub-judul">Data Eksekusi</h2>
            <div>
              <div className="fst-italic">Waktu Kompresi</div>
              <p>{getTime()}</p>
            </div>
            <div>
              <div className="fst-italic">Persentase Kompresi</div>
              <p>{(compressLevel * 100).toFixed(2)}%</p>
            </div>
          </div>
        </div>

        <div>
          <div className="mb-2">
            <h2 className="sub-judul">Tingkat Kompresi</h2>
            <Row>
              <Col className="d-flex align-items-center">
                <Form.Range
                  max={100}
                  min={0}
                  value={level}
                  onChange={(e) => {
                    setLevel(parseInt(e.target.value));
                  }}
                />
              </Col>
              <Col xs={4}>
                <Form.Control
                  type="number"
                  value={level}
                  min={0}
                  max={100}
                  onChange={(e) => {
                    setLevel(
                      parseInt(Math.max(0, Math.min(e.target.value, 100)))
                    );
                  }}
                  placeholder="%"
                ></Form.Control>
              </Col>
            </Row>
          </div>
          <div>
            <h2 className="sub-judul">Pengaturan Lainnya</h2>
            <Form.Check
              type="checkbox"
              id="alpha"
              label="Compress kanal alpha"
              checked={alpha}
              disabled={!isCacheAlpha}
              onChange={() => {
                setAlpha(!alpha);
              }}
            ></Form.Check>
            <Form.Check
              type="checkbox"
              id="tiles"
              label="Gunakan background tiles"
              checked={tiles}
              onChange={() => {
                setTiles(!tiles);
              }}
            ></Form.Check>
          </div>
        </div>
        <div style={{ textAlign: "center" }}>
          <h2 className="sub-judul">Unduh gambar</h2>
          <a
            className="btn btn-success mb-2 mt-3"
            href={imageUrl()}
            target="_blank"
            rel="noreferrer"
          >
            Unduh
          </a>
        </div>
      </div>
    </div>
  );
}

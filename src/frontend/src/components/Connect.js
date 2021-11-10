import { OverlayTrigger, Tooltip } from "react-bootstrap";
import plug from "../assets/plug.png";

export default function ConnectComponent() {
  return (
    <OverlayTrigger
      placement="bottom"
      overlay={<Tooltip id="connect-tooltip">Sambungkan Koneksi</Tooltip>}
    >
      <button className="connect-plug">
        <img src={plug} alt="Connection Plug"></img>
      </button>
    </OverlayTrigger>
  );
}

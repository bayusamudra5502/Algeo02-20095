import picture from "../assets/pictures.png";
import plug from "../assets/plug.png";
import Progress from "./Progress";

export default function Title() {
  return (
    <>
      <div className="title">
        <div className="picture">
          <img src={picture} alt="Gambar"></img>
        </div>
        <div>
          <h1 className="h2">Image Compressor</h1>
          <p>Yuk buat gambar lebih kecil</p>
        </div>
        <div className="status">
          <h2 className="sub-judul">Status Koneksi</h2>
          <div>
            <span className="statusbar connected"></span>Connected
          </div>
          <div>
            <span className="statusbar disconnected"></span>Disconnected
            <button className="connect-plug" title="Sambungkan Koneksi">
              <img src={plug} alt="Connection Plug"></img>
            </button>
          </div>
        </div>
        <div>
          <h2 className="sub-judul">Proses Kompresi</h2>
          <Progress value={0.3} animated={true}></Progress>
        </div>
        <div className="bottom">
          <h2 className="sub-judul">Tentang Program ini</h2>
          <p>Program ini dibuat oleh kelompok X</p>
          <p>
            Lihat informasi lengkap <button class="button-link">disini</button>.
          </p>
        </div>
      </div>
    </>
  );
}

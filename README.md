<img src="src/frontend/src/assets/pictures.png" alt="Gambar Ilustrasi" width="120">

# Image Compressor

### IF2123 Aljabar Linear dan Geometri

<i>Gambar diatas diambil dari Flaticon</i>

Kompresi gambar merupakan suatu tipe kompresi data yang dilakukan pada gambar digital. Salah satu algoritma yang dapat digunakan untuk kompresi gambar adalah algoritma SVD (Singular Value Decomposition). Program ini memanfaatkan SVD dalam melakukan kompresi gambar.

## Deployment

Program ini dideploy pada [http://compress.bayusamudra.my.id](http://compress.bayusamudra.my.id). Backend yang digunakan adalah memanfaatkan Heroku.

## Struktur Folder

Berikut ini adalah struktur folder dari project ini:

- Folder `test` berisi gambar uji yang digunakan
- Folder `doc` berisi laporan tugas ini
- Folder `src` berisi source program. Pada folder ini terdiri atas:
  - Folder `backend` berisi program backend. Pada bagian ini berisi algoritma kompresi dan api.
  - Folder `frontend` berisi program frontend. Pada bagian ini berisi pengaturan tampilan dan lainnya.

## Teknologi

Pada project ini, teknologi yang digunakan adalah

- FastAPI
- React
- Socket.IO
- Python
- Scipy dan Numpy

## Cara menggunakan

Untuk menggunakan program ini, anda dapat menggunakan backend yang telah disediakan ataupun menggunakan backend lokal. Frontend dapat anda akses pada [http://compress.bayusamudra.my.id](http://compress.bayusamudra.my.id).

### Backend Lokal

> <b>Notes :</b>
> Backend terkadang belum stabil. Bila anda mengalami kegagalan saat menggunakan windows, silahkan gunakan WSL.

Untuk menjalankan server lokal, lakukanlah langkah berikut:

1. Unduh python dan pip versi terbaru. Jika anda menggunakan linux, anda dapat menjalankan perintah berikut

```shell
sudo apt install python3 python3-pip python3-virtualenv
```

2. Buatlah virtualenv dan aktifkan virtualenv.

```shell
virtualenv venv
source ./venv/bin/activate
```

3. Install semua dependency

```shell
pip install -r requirements.txt
```

4. Jalankan backend. Unutk melakukan hal ini, anda dapat menjalankan perintah berikut:

```shell
python ./src/backend/main.py
```

Jika anda ingin menggunakan port selain `80`, anda dapat menjalankan dengan perintah berikut:

```shell
python ./src/backend/main.py <PORT>
```

### Backend Docker

Anda juga dapat menggunakan docker untuk menjalankan backend. Berikut ini adalah langkah-langkahnya:

1. Unduh Docker terlebih dahulu
2. Jika sudah terinstall, jjalankan perintah berikut:

```shell
docker build --tag algeo:1.0.0 .
```

3. Jalankan docker-compose up

```shell
docker-compose up
```

### Frontend Lokal

Bila anda ingin menjalankan frontend lokal, anda dapat melakukan langkah berikut

1. Install Node.JS versi LTS
2. Bukalah folder `./src/frontend` pada terminal anda.
3. Jalankan perintah berikut untuk menginstall depedency

```shell
npm i
```

4. Jalankan perintah tersebut untuk memulai server frontend

```shell
npm start
```

5. Bukalah browser pada `http://localhost:3000`

### Prosedur Kompresi

1. Bukalah [http://compress.bayusamudra.my.id](http://compress.bayusamudra.my.id) pada browser.
2. Koneksikan backend dengan menekan icon colokan.
3. Masukanlah data server. Anda dapat menggunakan server lokal dan juga server yang telah disediakan. Sebagai catatan, jangan gunakan alamat `127.0.0.1` ataupun ` localhost`. Hal ini dapat anda capai dengan mengubah konfigurasi [file hosts](<https://en.wikipedia.org/wiki/Hosts_(file)>).
4. Bila telah tersambung ke server, drop gambar pada tempat yang telah disediakan.
5. Tunggu hingga proses selesai.
6. Anda dapat mengatur tingkat kompresi setelah proses dekomposisi selesai

### Catatan

1. Server hanya dapat menggunakan satu koneksi
2. Bila anda ingin membatalkan proses, anda dapat melakukan restart browser. Selain itu, anda juga harus melakukan restart backend agar proses yang akan selanjutnya dilakukan tidak terganggu dengan proses sebelumnya.
3. Bila anda tidak bisa terkoneksi ke server lokal, anda dapat mematikan sementara flag `chrome://flags/#block-insecure-private-network-requests` pada browser anda.
   Untuk selengkapnya, anda dapat lihat pada [laman ini](https://stackoverflow.com/questions/66534759/chrome-cors-error-on-request-to-localhost-dev-server-from-remote-site).

import axios from "axios";

export async function getStatus(server) {
  try {
    const { data } = await axios.get(`${server}/status`);
    return !!data.isReady;
  } catch (err) {
    console.error(err);
    return false;
  }
}

export async function sendImage(
  server,
  token,
  image,
  cacheAlpha,
  updater = () => {}
) {
  const payload = new FormData();

  payload.append("token", token);
  payload.append("file", image);
  payload.append("alpha", cacheAlpha ? 1 : 0);

  try {
    await axios.post(`${server}/upload`, payload, {
      onUploadProgress: function (e) {
        updater(e.loaded / e.total);
      },
    });

    return true;
  } catch (err) {
    console.error(err);
    return false;
  }
}

export async function getStatusCompress(server, level) {
  try {
    const { data } = await axios.get(`${server}/compress/${level}/status`);

    return data;
  } catch (err) {
    console.error(err);
    return null;
  }
}

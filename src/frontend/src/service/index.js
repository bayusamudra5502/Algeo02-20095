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

export async function sendImage(server, token, image, updater = () => {}) {
  const payload = new FormData();

  payload.append("token", token);
  payload.append("image", image);

  try {
    await axios.post(`${server}/upload`, payload, {
      onUploadProgress: function (e) {
        updater((e.loaded * 100) / e.total);
      },
    });

    return true;
  } catch (err) {
    console.error(err);
    return false;
  }
}

export async function getActualCompress(server, level) {
  try {
    const { data } = await axios.get(`${server}/compress/${level}/status`);

    return data.compress;
  } catch (err) {
    console.error(err);
    return null;
  }
}

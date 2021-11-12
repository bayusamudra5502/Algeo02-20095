import io from "socket.io-client";
import data from "../config.json";
import { getStatus } from ".";

export default async function connectSocket(
  server = data.defaultServer,
  callback
) {
  const socket = io(`${server}`, { path: "/ws/socket.io" });

  if (await getStatus(server)) {
    callback({ server });

    socket.on("connect", () => {
      callback({ error: { error: false } });
      callback({ connected: socket.connected });
      callback({ userid: socket.id });
      subscribe();
    });

    socket.on("connect_failed", () => {
      callback({ error: { error: true, message: "Koneksi websocket error" } });
    });

    socket.on("disconnect", () => {
      callback({ connected: socket.connected });
      callback({ userid: null });
    });

    socket.on("response", (data) => {
      callback({ response: data });
    });

    socket.on("progress", (data) => {
      callback({ progress: data });
    });

    function subscribe() {
      socket.emit("subscribe", {});
    }

    function unsubscribe() {
      socket.emit("unsubscribe", {});
    }

    function buildMatrix() {
      socket.emit("build-matrix", {});
    }

    callback({ helper: { subscribe, unsubscribe, buildMatrix } });

    socket.connect();

    return true;
  } else {
    callback({ error: { error: true, message: "Server sedang sibuk" } });
    return false;
  }
}

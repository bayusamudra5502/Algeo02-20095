import React from "react";
import ReactDOM from "react-dom";
import App from "./App";
import reportWebVitals from "./reportWebVitals";

import { ConnectionProvider } from "./components/context/ConnectionContext";
import { ProcessProvider } from "./components/context/ProcessContext";
import { SocketProvider } from "./service/context/SocketContext";
import { MessageProvider } from "./components/context/MessageContext";
import { ResultProvider } from "./components/context/ResultContext";
import { UploadProvider } from "./components/context/UploadContext";

import "bootstrap/scss/bootstrap.scss";
import "./styles/index.scss";

ReactDOM.render(
  <React.StrictMode>
    <MessageProvider>
      <ConnectionProvider>
        <SocketProvider>
          <ProcessProvider>
            <ResultProvider>
              <UploadProvider>
                <App />
              </UploadProvider>
            </ResultProvider>
          </ProcessProvider>
        </SocketProvider>
      </ConnectionProvider>
    </MessageProvider>
  </React.StrictMode>,
  document.getElementById("root")
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();

import React, { createContext, useState } from "react";
import { Toast, ToastContainer } from "react-bootstrap";
import {
  AiFillCheckCircle,
  AiFillCloseCircle,
  AiFillExclamationCircle,
} from "react-icons/ai";

const MessageContext = createContext();

export function MessageProvider({ children }) {
  const [visibility, setVisibility] = useState(false);
  const [type, setType] = useState("success");
  const [text, setText] = useState("");

  function showMessage(message, type) {
    setType(type);
    setText(message);
    setVisibility(true);
  }

  function circle() {
    if (type === "warning") {
      return (
        <span className="text text-yellow">
          <AiFillExclamationCircle />
        </span>
      );
    } else if (type === "error") {
      return (
        <span className="text text-red">
          <AiFillCloseCircle />
        </span>
      );
    } else if (type === "success") {
      return (
        <span className="text text-green">
          <AiFillCheckCircle></AiFillCheckCircle>
        </span>
      );
    } else {
      return <span></span>;
    }
  }

  return (
    <>
      <MessageContext.Provider value={{ showMessage }}>
        {children}
      </MessageContext.Provider>
      <ToastContainer
        position="top-end"
        style={{ margin: "10px", zIndex: "5000" }}
      >
        <Toast
          onClose={() => setVisibility(false)}
          show={visibility}
          delay={3000}
          autohide
        >
          <Toast.Body>
            <div>
              {circle()}
              {text}
            </div>
          </Toast.Body>
        </Toast>
      </ToastContainer>
    </>
  );
}

export default MessageContext;

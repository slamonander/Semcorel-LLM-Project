// src/components/ChatPage.js
import React, { useState, useRef, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./ChatPage.css";
import Avatar from "../components/Avatar";

const ChatPage = () => {
  const [message, setMessage] = useState("");
  const [chatLog, setChatLog] = useState([]);
  const navigate = useNavigate();
  const chatLogRef = useRef(null);
  const inputRef = useRef(null);

  const handleSendMessage = () => {
    if (message.trim() !== "") {
      setChatLog([...chatLog, { text: message, sender: "user" }]);
      setMessage(""); // Clear the input
    }
  };

  const handleBack = () => {
    navigate("/");
  };

  // Scroll to the top of the chat log after any interaction
  useEffect(() => {
    if (chatLogRef.current) {
      chatLogRef.current.scrollTo(0, 0);
    }
  }, [chatLog]);

  // Prevent iOS keyboard from scrolling the page
  useEffect(() => {
    const handleFocus = () => {
      document.body.style.position = "fixed";
      document.body.style.overflow = "hidden";
      document.body.style.width = "100%";
    };

    const handleBlur = () => {
      document.body.style.position = "";
      document.body.style.overflow = "";
      document.body.style.width = "";
    };

    const inputElement = inputRef.current;
    inputElement?.addEventListener("focus", handleFocus);
    inputElement?.addEventListener("blur", handleBlur);

    return () => {
      inputElement?.removeEventListener("focus", handleFocus);
      inputElement?.removeEventListener("blur", handleBlur);
    };
  }, []);

  return (
    <div className="chat-page">
      <button className="back-button" onClick={handleBack}>
        ⬅ Back
      </button>

      <div className="chat-container">
        <Avatar /> {/* Render the Avatar component */}
        <div className="chat-log" ref={chatLogRef}>
          {chatLog.map((chat, index) => (
            <div key={index} className={`chat-message ${chat.sender}`}>
              {chat.text}
            </div>
          ))}
        </div>
        <div className="chat-input-container">
          <input
            ref={inputRef}
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Type your question ..."
            className="chat-input"
          />
          <button onClick={handleSendMessage} className="send-button">
            Send
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatPage;

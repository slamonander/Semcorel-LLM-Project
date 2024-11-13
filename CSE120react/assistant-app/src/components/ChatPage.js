// src/components/ChatPage.js
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./ChatPage.css";
import Avatar from "../components/Avatar";

const ChatPage = () => {
  const [message, setMessage] = useState("");
  const [chatLog, setChatLog] = useState([]);
  const navigate = useNavigate();

  const handleSendMessage = () => {
    if (message.trim() !== "") {
      setChatLog([...chatLog, { text: message, sender: "user" }]);
      setMessage(""); // Clear the input
    }
  };

  const handleBack = () => {
    navigate("/");
  };

  return (
    <div className="chat-page">
      <button className="back-button" onClick={handleBack}>
        ⬅ Back
      </button>

      <div className="chat-container">
        <Avatar /> {/* Render the Avatar component */}
        <div className="chat-log">
          {chatLog.map((chat, index) => (
            <div key={index} className={`chat-message ${chat.sender}`}>
              {chat.text}
            </div>
          ))} 
        </div>
        <div className="chat-input-container ">
          <input
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

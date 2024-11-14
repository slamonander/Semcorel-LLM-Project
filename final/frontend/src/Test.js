// src/Test.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Coco from './Coco';
import './Test.css';

const Test = () => {
  const [userInput, setUserInput] = useState('');
  const [conversationHistory, setConversationHistory] = useState([]);
  const [messages, setMessages] = useState([]);
  const navigate = useNavigate();

  const addMessage = (content, className) => {
    setMessages((prevMessages) => [
      ...prevMessages,
      { content, className },
    ]);
  };

  const sendMessage = async () => {
    if (!userInput.trim()) return;

    // Display user message
    addMessage(userInput, 'user-message');
    setConversationHistory((prevHistory) => [
      ...prevHistory,
      { role: 'user', content: userInput },
    ]);
    setUserInput('');

    try {
      // Prepare JSON data
      const payload = {
        userInput: userInput,
        history: JSON.stringify(conversationHistory),
      };

      // Send message to the server
      const response = await fetch('/submit', { // Specify full URL
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      // Display bot response
      addMessage(data.response, 'bot-message');
      setConversationHistory((prevHistory) => [
        ...prevHistory,
        { role: 'assistant', content: data.response },
      ]);
    } catch (error) {
      console.error('Error:', error);
      addMessage('An error occurred while sending your message.', 'bot-message');
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === 'Enter') {
      sendMessage();
    }
  };

  return (
    <div className="container">
        <div className="triangle-container">
          <svg className="triangle" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" preserveAspectRatio="none">
            <path className="wave" d="M 0,100 Q 20,75 45,85 T 100,15 L 100,0 L 0,0 Z" fill="#5A9BFF" transform="skewY(-25)"/>
          </svg>
                <button className="btn-invis" onClick={() => navigate('/')}>
                <span className="material-icons invis">arrow_back_ios</span>
                </button>
            <div className="coco-container">
                <Coco className="coco-small" />
            </div>
        </div>

      {/* Chat container */}
      <div className="chat-container">
        <div id="chat-box" className="chat-box">
          {messages.map((msg, index) => (
            <div key={index} className={`chat-message ${msg.className}`}>
              {msg.content}
            </div>
          ))}
        </div>
        <div className="input-container">
          <input
            type="text"
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Type a message..."
          />
          <button onClick={sendMessage}>
          <span className="material-icons icon-send">send</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default Test;

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Coco from './Coco';
import './TypePage.css';

const TypePage = () => {
  const [userInput, setUserInput] = useState('');
  const [conversationHistory, setConversationHistory] = useState([]);
  const [messages, setMessages] = useState([]);
  const [isTyping, setIsTyping] = useState(false);
  const [fontSize, setFontSize] = useState(19); // Default font size
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
      setIsTyping(true); // Show typing animation

      // Prepare JSON data
      const payload = {
        userInput: userInput,
        history: JSON.stringify(conversationHistory),
      };

      // Send message to the server
      const response = await fetch('/submit', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      setIsTyping(false); // Hide typing animation

      // Display bot response
      addMessage(data.response, 'bot-message');
      setConversationHistory((prevHistory) => [
        ...prevHistory,
        { role: 'assistant', content: data.response },
      ]);
    } catch (error) {
      console.error('Error:', error);
      setIsTyping(false); // Hide typing animation
      addMessage('An error occurred while sending your message.', 'bot-message');
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === 'Enter') {
      sendMessage();
    }
  };

  const changeFontSize = (adjustment) => {
    setFontSize((prevSize) => Math.max(12, Math.min(36, prevSize + adjustment))); // Restrict between 12px and 36px
  };

  return (
    <div className="container">
      <div className="triangle-container">
        <svg className="triangle" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 125" preserveAspectRatio="none">
            <path className="wave" d="M 0,50 Q 20,35 45,40 T 100,15 L 100,0 L 0,0 Z" fill="#5A9BFF" transform="skewY(-15)" />
        </svg>
        <button className="btn-invis" onClick={() => navigate('/')}>
          <span className="material-icons invis">arrow_back_ios</span>
        </button>
        <div className="coco-container">
          <Coco className="coco-small" />
        </div>
      </div>

      <div className="font-size-buttons">
        <button onClick={() => changeFontSize(-2)}>A-</button>
        <button onClick={() => changeFontSize(2)}>A+</button>
      </div>

      {/* Chat container */}
      <div className="chat-container">
        <div id="chat-box" className="chat-box">
          {messages.map((msg, index) => (
            <div key={index} className={`chat-message ${msg.className}`} style={{ fontSize: `${fontSize}px` }}> 
            {msg.content}
          </div>
          ))}
          {isTyping && (
            <div className="chat-message bot-message typing-animation">
              <span>.</span>
              <span>.</span>
              <span>.</span>
            </div>
          )}
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

export default TypePage;

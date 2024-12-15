import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import Coco from './Coco';
import './TypePage.css';

// Font: Roboto
<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet"></link>

const TypePage = () => {
  const [userInput, setUserInput] = useState('');
  const [conversationHistory, setConversationHistory] = useState([]);
  const [messages, setMessages] = useState([]);
  const [isTyping, setIsTyping] = useState(false);
  const [fontSize, setFontSize] = useState(19); // Default font size
  const navigate = useNavigate();
  const chatBoxRef = useRef(null); // Ref for chat box container

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

  // Automatically scroll to the bottom of the chat box
  useEffect(() => {
    if (chatBoxRef.current) {
      chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
    }
  }, [messages, isTyping]);

  return (
    <div className="container">
      <div className="triangle-container">
        <svg className="triangle" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 200" preserveAspectRatio="none">
        <g className="parallax">
          <path
              className="wave wave1"
              d="M-160 56c30 0 58 18 88 18s 58-18 88-18 58 18 88 18 58-18 88-18 58-18 88-18 v-44h-352z"
              fill="rgba(90, 155, 255, 0.7)"
            />
            <path
              className="wave wave2"
              d="M-160 56c30 0 58 18 88 18s 58-18 88-18 58 18 88 18 58-18 88-18 58-18 88-18 v-44h-352z"
              fill="rgba(90, 155, 255, 0.5)"
            />
            <path
              className="wave wave3"
              d="M-160 56c30 0 58 18 88 18s 58-18 88-18 58 18 88 18 58-18 88-18 58-18 88-18 v-44h-352z"
              fill="rgba(90, 155, 255, 0.3)"
            />
          </g>
        </svg>
        <button className="btn-invis" onClick={() => navigate('/')}>
          <span className="material-icons invis">arrow_back_ios</span>
        </button>
        <div className="coco-container">
          <Coco className="coco-small" />
        </div>
      </div>

      <div className="font-size-buttons">
  <button 
    style={{ fontSize: '19px' }} 
    onClick={() => changeFontSize(-2)}
  >
    A-
  </button>
  <button 
    style={{ fontSize: '21px' }} 
    onClick={() => changeFontSize(2)}
  >
    A+
  </button>
</div>

      {/* Chat container */}
      <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&icon_names=arrow_upward" />
      <div className="chat-container">
        <div id="chat-box" className="chat-box" ref={chatBoxRef}>
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
            <span className="material-symbols-outlined">arrow_upward</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default TypePage;

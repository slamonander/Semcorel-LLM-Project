import React, { useState } from 'react';
import './TypePage.css'; // Assuming you will move your CSS into this file

const TypePage = () => {
  const [userInput, setUserInput] = useState('');
  const [conversationHistory, setConversationHistory] = useState([]);
  const [messages, setMessages] = useState([]);

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
      const response = await fetch('http://localhost:8080/submit', { // Specify full URL
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
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
};

export default TypePage;

// src/SpeakPage.js
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Coco from './Coco';
import './SpeakPage.css';

const SpeakPage = () => {
  const [conversationHistory, setConversationHistory] = useState([]);
  const [messages, setMessages] = useState([]);
  const [isTyping, setIsTyping] = useState(false);
  const [fontSize, setFontSize] = useState(19); // Default font size
  const [isListening, setIsListening] = useState(false);
  const [voices, setVoices] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    // Load available voices for Safari fix
    if ('speechSynthesis' in window) {
      const loadVoices = () => {
        const availableVoices = window.speechSynthesis.getVoices();
        setVoices(availableVoices);
      };
      loadVoices();
      window.speechSynthesis.onvoiceschanged = loadVoices;
    }
  }, []);

  const addMessage = (content, className) => {
    setMessages((prevMessages) => [
      ...prevMessages,
      { content, className },
    ]);
  };

  const sendMessage = async (messageContent) => {
    if (!messageContent.trim()) return;

    // Display user message
    addMessage(messageContent, 'user-message');
    setConversationHistory((prevHistory) => [
      ...prevHistory,
      { role: 'user', content: messageContent },
    ]);

    try {
      setIsTyping(true); // Show typing animation

      // Prepare JSON data
      const payload = {
        userInput: messageContent,
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

      // Speak the bot's response
      if ('speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(data.response);
        utterance.lang = 'en-US';
        utterance.voice = voices.find((voice) => voice.lang === 'en-US') || null; // Use an English voice if available
        window.speechSynthesis.speak(utterance);
      } else {
        console.warn('Text-to-speech is not supported in this browser.');
      }
    } catch (error) {
      console.error('Error:', error);
      setIsTyping(false); // Hide typing animation
      addMessage('An error occurred while sending your message.', 'bot-message');
    }
  };

  const handleSpeechToText = () => {
    if (!('webkitSpeechRecognition' in window)) {
      alert('Speech recognition is not supported in this browser.');
      return;
    }

    const recognition = new window.webkitSpeechRecognition();
    recognition.lang = 'en-US';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.onstart = () => setIsListening(true);
    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      setIsListening(false);
      sendMessage(transcript);
    };
    recognition.onerror = (event) => {
      console.error('Speech recognition error', event.error);
      setIsListening(false);
    };
    recognition.onend = () => setIsListening(false);

    recognition.start();
  };

  const changeFontSize = (adjustment) => {
    setFontSize((prevSize) => Math.max(12, Math.min(36, prevSize + adjustment))); // Restrict between 12px and 36px
  };

  const enableSpeechSynthesis = () => {
    // Ensure speech synthesis is enabled on Safari
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance('Speech synthesis is now enabled.');
      utterance.lang = 'en-US';
      window.speechSynthesis.speak(utterance);
    }
  };

  return (
    <div className="container">
      <div className="triangle-container">
        <svg
          className="triangle"
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 100 100"
          preserveAspectRatio="none"
        >
          <path
            className="wave"
            d="M 0,100 Q 20,75 45,85 T 100,15 L 100,0 L 0,0 Z"
            fill="#5A9BFF"
            transform="skewY(-25)"
          />
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
        <button onClick={enableSpeechSynthesis}>Enable Speech</button>
      </div>

      {/* Chat container */}
      <div className="chat-container">
        <div id="chat-box" className="chat-box">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`chat-message ${msg.className}`}
              style={{ fontSize: `${fontSize}px` }}
            >
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
          <button
            onClick={handleSpeechToText}
            className="speech-button"
            disabled={isListening}
          >
            {isListening ? 'Listening...' : 'Start Speaking'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default SpeakPage;

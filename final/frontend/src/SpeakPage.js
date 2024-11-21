// // speakpage.js
// import React, { useState } from "react";
// import { useNavigate } from "react-router-dom";
// import "./SpeakPage.css"; // Import the CSS file here
// import Avatar from "./Avatar";

// function SpeakPage() {
//   const [transcript, setTranscript] = useState("");
//   const [textInput, setTextInput] = useState("");
//   const [isListening, setIsListening] = useState(false);
//   const navigate = useNavigate();

//   // Function for handling Speech-to-Text
//   const handleSpeechToText = () => {
//     if (!("webkitSpeechRecognition" in window)) {
//       alert("Speech recognition is not supported in this browser.");
//       return;
//     }

//     const recognition = new window.webkitSpeechRecognition();
//     recognition.lang = "en-US";
//     recognition.interimResults = false;
//     recognition.maxAlternatives = 1;

//     recognition.onstart = () => setIsListening(true);
//     recognition.onresult = (event) => {
//       setTranscript(event.results[0][0].transcript);
//       setIsListening(false);
//     };
//     recognition.onerror = (event) => {
//       console.error("Speech recognition error", event.error);
//       setIsListening(false);
//     };
//     recognition.onend = () => setIsListening(false);

//     recognition.start();
//   };

//   // Function for handling Text-to-Speech
//   const handleTextToSpeech = () => {
//     if (!("speechSynthesis" in window)) {
//       alert("Text-to-speech is not supported in this browser.");
//       return;
//     }

//     const utterance = new SpeechSynthesisUtterance(textInput);
//     utterance.lang = "en-US";
//     window.speechSynthesis.speak(utterance);
//   };

//   const handleBack = () => {
//     navigate("/");
//   };

//   return (
//     <div className="speak-container">
//       <h1>Speech-to-Text and Text-to-Speech</h1>

//       {/* Speech-to-Text Section */}
//       <div style={{ margin: "20px 0" }}>
//         <button className="back-button" onClick={handleBack}>
//           ⬅ Back
//         </button>
//         <Avatar /> {/* Render the Avatar component */}
//         <button
//           onClick={handleSpeechToText}
//           className="speech-button"
//           disabled={isListening}
//         >
//           {isListening ? "Listening..." : "Start Speaking"}
//         </button>
//         <p className="transcript">Transcript: {transcript}</p>
//       </div>
 
//       {/* Text-to-Speech Section */}
//       <div style={{ margin: "20px 0" }}>
//         <textarea
//           rows="4"
//           className="text-area"
//           value={textInput}
//           onChange={(e) => setTextInput(e.target.value)}
//           placeholder="Enter text to read out loud"
//         />
//         <br />
//         <button onClick={handleTextToSpeech} className="text-to-speech-button">
//           Read Text Aloud
//         </button>
//       </div>
//     </div>
//   );
// }

// export default SpeakPage;

// src/SpeakPage.js
// src/SpeakPage.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Coco from './Coco';
import './SpeakPage.css';

const SpeakPage = () => {
  const [conversationHistory, setConversationHistory] = useState([]);
  const [messages, setMessages] = useState([]);
  const [fontSize, setFontSize] = useState(19); // Default font size
  const [isListening, setIsListening] = useState(false);
  const navigate = useNavigate();

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
      // Prepare JSON data
      const payload = {
        userInput: messageContent,
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

      // Speak the bot's response
      if ('speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(data.response);
        utterance.lang = 'en-US';
        window.speechSynthesis.speak(utterance);
      } else {
        console.warn('Text-to-speech is not supported in this browser.');
      }
    } catch (error) {
      console.error('Error:', error);
      addMessage('An error occurred while sending your message.', 'bot-message');
    }
  };

  // Function for handling Speech-to-Text
  const handleSpeechToText = () => {
    if (!("webkitSpeechRecognition" in window)) {
      alert("Speech recognition is not supported in this browser.");
      return;
    }

    const recognition = new window.webkitSpeechRecognition();
    recognition.lang = "en-US";
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.onstart = () => setIsListening(true);
    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      setIsListening(false);
      sendMessage(transcript);
    };
    recognition.onerror = (event) => {
      console.error("Speech recognition error", event.error);
      setIsListening(false);
    };
    recognition.onend = () => setIsListening(false);

    recognition.start();
  };

  const changeFontSize = (adjustment) => {
    setFontSize((prevSize) => Math.max(12, Math.min(36, prevSize + adjustment))); // Restrict between 12px and 36px
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

      <div className="font-size-buttons">
        <button onClick={() => changeFontSize(-2)}>A-</button>
        <button onClick={() => changeFontSize(2)}>A+</button>
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
        </div>
        <div className="input-container">
          <button
            onClick={handleSpeechToText}
            className="speech-button"
            disabled={isListening}
          >
            {isListening ? "Listening..." : "Start Speaking"}
          </button>
        </div>
      </div>
    </div>
  );
};

export default SpeakPage;
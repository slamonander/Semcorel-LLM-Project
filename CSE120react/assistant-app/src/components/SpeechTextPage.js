import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./SpeechTextPage.css"; // Import the CSS file here
import Avatar from "../components/Avatar";

function SpeechTextPage() {
  const [transcript, setTranscript] = useState("");
  const [textInput, setTextInput] = useState("");
  const [isListening, setIsListening] = useState(false);
  const [voices, setVoices] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    // Load available voices and update state
    const loadVoices = () => {
      const availableVoices = window.speechSynthesis.getVoices();
      setVoices(availableVoices);
    };

    loadVoices();

    if (typeof window.speechSynthesis !== "undefined") {
      window.speechSynthesis.onvoiceschanged = loadVoices;
    }
  }, []);

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
      setTranscript(event.results[0][0].transcript);
      setIsListening(false);
    };
    recognition.onerror = (event) => {
      console.error("Speech recognition error", event.error);
      setIsListening(false);
    };
    recognition.onend = () => setIsListening(false);

    recognition.start();
  };

  // Function for handling Text-to-Speech
  const handleTextToSpeech = () => {
    if (!("speechSynthesis" in window)) {
      alert("Text-to-speech is not supported in this browser.");
      return;
    }

    const utterance = new SpeechSynthesisUtterance(textInput);
    utterance.lang = "en-GB"; // Set language to British English

    // Set voice to 'Daniel' for iOS or fallback to the default voice
    const selectedVoice = voices.find((voice) => voice.name === "Daniel");
    if (selectedVoice) {
      utterance.voice = selectedVoice;
    } else {
      console.warn("Voice 'Daniel' not found. Using default voice.");
    }

    window.speechSynthesis.speak(utterance);
  };

  const handleBack = () => {
    navigate("/");
  };

  return (
    <div className="container">
      <h1>Speech-to-Text and Text-to-Speech</h1>

      {/* Speech-to-Text Section */}
      <div style={{ margin: "20px 0" }}>
        <button className="back-button" onClick={handleBack}>
          ⬅ Back
        </button>
        <Avatar /> {/* Render the Avatar component */}
        <button
          onClick={handleSpeechToText}
          className="speech-button"
          disabled={isListening}
        >
          {isListening ? "Listening..." : "Start Speaking"}
        </button>
        <p className="transcript">Transcript: {transcript}</p>
      </div>

      {/* Text-to-Speech Section */}
      <div style={{ margin: "20px 0" }}>
        <textarea
          rows="4"
          className="text-area"
          value={textInput}
          onChange={(e) => setTextInput(e.target.value)}
          placeholder="Enter text to read out loud"
        />
        <br />
        <button onClick={handleTextToSpeech} className="text-to-speech-button">
          Read Text Aloud
        </button>
      </div>
    </div>
  );
}

export default SpeechTextPage;

// src/App.js
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Greeting from "./components/Greeting";
import Avatar from "./components/Avatar";
import ActionButtons from "./components/ActionButtons";
import SpeechTextPage from "./components/SpeechTextPage";
import ChatPage from "./components/ChatPage";
import "./App.css";
function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route
            path="/"
            element={
              <>
                <Greeting />
                <Avatar />
                <ActionButtons />
              </>
            }
          />
          <Route path="/chat" element={<ChatPage />} />
          <Route path="/speech-text" element={<SpeechTextPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;

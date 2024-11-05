////
////  ContentView.swift
////  webViewer
////
////  Created by Kavin Rajasekaran on 9/26/24.
////
//
//import SwiftUI
//import SwiftData
//import UIKit
//
//
//struct ContentView: View {
//    var body: some View {
//        WebView(htmlContent: """
//            <!DOCTYPE html>
//            <html lang="en">
//            <head>
//                <meta charset="UTF-8">
//                <title>CoCo Assistant</title>
//                <meta name="viewport" content="width=device-width, initial-scale=1.0">
//                <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
//                <!-- Google Fonts -->
//                <link href="https://fonts.googleapis.com/css?family=Roboto:400,500,700&display=swap" rel="stylesheet">
//                <style>
//                    /* Reset and basic styling */
//                    * {
//                        margin: 0;
//                        padding: 0;
//                        box-sizing: border-box;
//                    }
//
//                    body {
//                        font-family: 'Roboto', sans-serif;
//                        background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
//                        color: #333;
//                        display: flex;
//                        align-items: center;
//                        justify-content: center;
//                        min-height: 100vh;
//                    }
//
//                    .container {
//                        width: 90%;
//                        max-width: 400px;
//                        background-color: rgba(255, 255, 255, 0.85);
//                        padding: 30px 20px;
//                        border-radius: 20px;
//                        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
//                        text-align: center;
//                        backdrop-filter: blur(10px);
//                    }
//
//                    .logo {
//                        width: 80px;
//                        margin-bottom: 20px;
//                        animation: float 3s ease-in-out infinite;
//                    }
//
//                    @keyframes float {
//                        0%, 100% {
//                            transform: translateY(0);
//                        }
//                        50% {
//                            transform: translateY(-10px);
//                        }
//                    }
//
//                    h1 {
//                        font-size: 32px;
//                        margin-bottom: 10px;
//                        color: #007bff;
//                        font-weight: 700;
//                    }
//
//                    p {
//                        font-size: 18px;
//                        margin-bottom: 30px;
//                        color: #555;
//                    }
//
//                    .input-group {
//                        position: relative;
//                        margin-bottom: 25px;
//                    }
//
//                    input[type="text"] {
//                        width: 100%;
//                        padding: 15px 50px 15px 20px;
//                        border: none;
//                        border-radius: 30px;
//                        font-size: 16px;
//                        outline: none;
//                        background-color: #f1f3f5;
//                        transition: background-color 0.3s;
//                    }
//
//                    input[type="text"]:focus {
//                        background-color: #e9ecef;
//                    }
//
//                    .microphone-button {
//                        position: absolute;
//                        right: 15px;
//                        top: 50%;
//                        transform: translateY(-50%);
//                        background: none;
//                        border: none;
//                        padding: 0;
//                        cursor: pointer;
//                    }
//
//                    .microphone-button img {
//                        width: 24px;
//                        height: 24px;
//                        transition: transform 0.3s;
//                    }
//
//                    .microphone-button:hover img {
//                        transform: scale(1.1);
//                    }
//
//                    button[type="submit"] {
//                        width: 100%;
//                        padding: 15px;
//                        background: linear-gradient(135deg, #6a11cb, #2575fc);
//                        border: none;
//                        border-radius: 30px;
//                        color: #fff;
//                        font-size: 18px;
//                        cursor: pointer;
//                        transition: background 0.3s, box-shadow 0.3s;
//                    }
//
//                    button[type="submit"]:hover {
//                        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
//                    }
//
//                    /* Responsive adjustments */
//                    @media (max-width: 320px) {
//                        h1 {
//                            font-size: 28px;
//                        }
//
//                        p {
//                            font-size: 16px;
//                        }
//
//                        input[type="text"], button[type="submit"] {
//                            font-size: 14px;
//                        }
//                    }
//                * {
//                    margin: 0;
//                    padding: 0;
//                    box-sizing: border-box;
//                }
//
//                body {
//                    font-family: 'Roboto', sans-serif;
//                    background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
//                    color: #333;
//                    display: flex;
//                    align-items: center;
//                    justify-content: center;
//                    min-height: 100vh;
//                    overflow: hidden; /* Prevents scrolling */
//                }
//
//                .container {
//                    width: 90%;
//                    max-width: 400px;
//                    background-color: rgba(255, 255, 255, 0.85);
//                    padding: 30px 20px;
//                    border-radius: 20px;
//                    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
//                    text-align: center;
//                    backdrop-filter: blur(10px);
//                }
//
//                </style>
//            </head>
//            <body>
//                <div class="container">
//                    <h1>CoCo Assistant</h1>
//                    <p>Get help with your watch</p>
//                    <form action="http://10.33.35.62:8080/submit" method="post">
//                        <div class="input-group">
//                            <input type="text" id="userInput" name="userInput" placeholder="Ask a question...">
//                            <button type="button" class="microphone-button" onclick="startDictation()">
//                                <img src="https://img.icons8.com/ios-glyphs/30/000000/microphone.png" alt="Mic">
//                            </button>
//                        </div>
//                        <button type="submit">Send</button>
//                    </form>
//                </div>
//
//                <!-- JavaScript for voice-to-text functionality -->
//                <script>
//                    function startDictation() {
//                        // Check if the browser supports speech recognition
//                        var SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
//                        if (SpeechRecognition) {
//                            var recognition = new SpeechRecognition();
//                            recognition.lang = 'en-US';
//                            recognition.start();
//
//                            recognition.onresult = function(event) {
//                                document.getElementById('userInput').value = event.results[0][0].transcript;
//                            };
//
//                            recognition.onerror = function(event) {
//                                alert('Error occurred in recognition: ' + event.error);
//                            };
//                        } else {
//                            alert('Voice input is not supported in this browser.');
//                        }
//                    }
//                </script>
//            </body>
//            </html>
//
//            """)
//            .edgesIgnoringSafeArea(.all) // Expands the 
//    }
//}

//
//  ContentView.swift
//  webViewer
//
//  Created by Kavin Rajasekaran on 9/26/24.
//

import SwiftUI
import WebKit

struct ContentView: View {
    var body: some View {
        URLWebView(urlString: "http://10.33.35.62:8080/")
            .edgesIgnoringSafeArea(.all) // Expands the WebView to fill the screen
    }
}

struct URLWebView: UIViewRepresentable {
    let urlString: String

    func makeUIView(context: Context) -> WKWebView {
        let webView = WKWebView()
        
        // Enable JavaScript and media playback
        webView.configuration.preferences.javaScriptEnabled = true
        webView.configuration.mediaTypesRequiringUserActionForPlayback = []

        // Navigation delegate can be set if needed
        webView.navigationDelegate = context.coordinator

        return webView
    }

    func updateUIView(_ webView: WKWebView, context: Context) {
        if let url = URL(string: urlString) {
            let request = URLRequest(url: url)
            webView.load(request)
        }
    }

    // Coordinator to handle navigation actions if necessary
    func makeCoordinator() -> Coordinator {
        Coordinator()
    }

    class Coordinator: NSObject, WKNavigationDelegate {
        // Implement navigation delegate methods if needed
        func webView(_ webView: WKWebView, didFail navigation: WKNavigation!, withError error: Error) {
            print("WebView navigation failed with error: \(error.localizedDescription)")
        }
    }
}

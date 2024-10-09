//
//  ContentView.swift
//  webViewer
//
//  Created by Kavin Rajasekaran on 9/26/24.
//

import SwiftUI
import SwiftData
import UIKit


struct ContentView: View {
    var body: some View {
        WebView(htmlContent: """
            <html>
                <head>
                    <title>Watch AI</title>
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <style>
                        /*  styles to fit an iPhone screen */
                        body {
                            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
                            padding: 20px;
                            margin: 0;
                            line-height: 1.6;
                            background-color: #f8f9fa;
                        }
                        h1 {
                            color: #333;
                            font-size: 24px;
                            text-align: center;
                            margin-bottom: 20px;
                        }
                        p {
                            color: #666;
                            font-size: 16px;
                            text-align: center;
                        }
                        form {
                            display: flex;
                            flex-direction: column;
                            align-items: center;
                            margin-top: 20px;
                        }
                        .input-group {
                            position: relative;
                            width: 90%;
                            max-width: 400px;
                            margin-bottom: 15px;
                        }
                        input[type="text"] {
                            padding: 10px 40px 10px 10px;
                            width: 100%;
                            border: 1px solid #ccc;
                            border-radius: 4px;
                            font-size: 16px;
                        }
                        .microphone-button {
                            position: absolute;
                            right: 10px;
                            top: 50%;
                            transform: translateY(-50%);
                            background: none;
                            border: none;
                            padding: 0;
                            margin: 0;
                            cursor: pointer;
                        }
                        .microphone-button img {
                            width: 24px;
                            height: 24px;
                        }
                        button[type="submit"] {
                            padding: 10px 20px;
                            background-color: #007bff;
                            color: #fff;
                            border: none;
                            border-radius: 4px;
                            font-size: 16px;
                            cursor: pointer;
                            width: 90%;
                            max-width: 400px;
                        }
                        button[type="submit"]:hover {
                            background-color: #0056b3;
                        }
                    </style>
                </head>
                <body>
                    <h1>Watch AI</h1>
                    <p>Get help with your watch</p>
                    <form action="http://192.168.1.109:5000/submit" method="post">
                        <div class="input-group">
                            <input type="text" id="userInput" name="userInput" placeholder="Type something...">
                            <button type="button" class="microphone-button" onclick="startDictation()">
                                <img src="https://img.icons8.com/ios-glyphs/30/000000/microphone.png" alt="Mic">
                            </button>
                        </div>
                        <button type="submit">Send</button>
                    </form>

                    <!-- JavaScript for voice-to-text functionality -->
                    <script>
                        function startDictation() {
                            // Check if the browser supports speech recognition
                            var SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                            if (SpeechRecognition) {
                                var recognition = new SpeechRecognition();
                                recognition.lang = 'en-US';
                                recognition.start();

                                recognition.onresult = function(event) {
                                    document.getElementById('userInput').value = event.results[0][0].transcript;
                                };

                                recognition.onerror = function(event) {
                                    alert('Error occurred in recognition: ' + event.error);
                                };
                            } else {
                                alert('Voice input is not supported in this browser.');
                            }
                        }
                    </script>
                </body>
            </html>

            """)
            .edgesIgnoringSafeArea(.all) // Expands the web view to the entire screen
    }
}

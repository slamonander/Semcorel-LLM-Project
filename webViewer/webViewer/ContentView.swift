//
//  ContentView.swift
//  webViewer
//
//  Created by Kavin Rajasekaran on 9/26/24.
//


// -------------------working -------------------

//import SwiftUI
//import SwiftData
//import UIKit
//
//
//struct ContentView: View {
//    var body: some View {
//        WebView(htmlContent: """
//            <html>
//                <head>
//                    <title>Watch AI</title>
//                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
//                    <style>
//                        /*  styles to fit an iPhone screen */
//                        body {
//                            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
//                            padding: 20px;
//                            margin: 0;
//                            line-height: 1.6;
//                            background-color: #f8f9fa;
//                        }
//                        h1 {
//                            color: #333;
//                            font-size: 24px;
//                            text-align: center;
//                            margin-bottom: 20px;
//                        }
//                        p {
//                            color: #666;
//                            font-size: 16px;
//                            text-align: center;
//                        }
//                        form {
//                            display: flex;
//                            flex-direction: column;
//                            align-items: center;
//                            margin-top: 20px;
//                        }
//                        .input-group {
//                            position: relative;
//                            width: 90%;
//                            max-width: 400px;
//                            margin-bottom: 15px;
//                        }
//                        input[type="text"] {
//                            padding: 10px 40px 10px 10px;
//                            width: 100%;
//                            border: 1px solid #ccc;
//                            border-radius: 4px;
//                            font-size: 16px;
//                        }
//                        .microphone-button {
//                            position: absolute;
//                            right: 10px;
//                            top: 50%;
//                            transform: translateY(-50%);
//                            background: none;
//                            border: none;
//                            padding: 0;
//                            margin: 0;
//                            cursor: pointer;
//                        }
//                        .microphone-button img {
//                            width: 24px;
//                            height: 24px;
//                        }
//                        button[type="submit"] {
//                            padding: 10px 20px;
//                            background-color: #007bff;
//                            color: #fff;
//                            border: none;
//                            border-radius: 4px;
//                            font-size: 16px;
//                            cursor: pointer;
//                            width: 90%;
//                            max-width: 400px;
//                        }
//                        button[type="submit"]:hover {
//                            background-color: #0056b3;
//                        }
//                    </style>
//                </head>
//                <body>
//                    <h1>Watch AI</h1>
//                    <p>Get help with your watch</p>
//                    <form action="http://192.168.1.119:8080/submit" method="post">
//                        <div class="input-group">
//                            <input type="text" id="userInput" name="userInput" placeholder="Type something...">
//                            <button type="button" class="microphone-button" onclick="startDictation()">
//                                <img src="https://img.icons8.com/ios-glyphs/30/000000/microphone.png" alt="Mic">
//                            </button>
//                        </div>
//                        <button type="submit">Send</button>
//                    </form>
//
//                    <!-- JavaScript for voice-to-text functionality -->
//                    <script>
//                        function startDictation() {
//                            // Check if the browser supports speech recognition
//                            var SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
//                            if (SpeechRecognition) {
//                                var recognition = new SpeechRecognition();
//                                recognition.lang = 'en-US';
//                                recognition.start();
//
//                                recognition.onresult = function(event) {
//                                    document.getElementById('userInput').value = event.results[0][0].transcript;
//                                };
//
//                                recognition.onerror = function(event) {
//                                    alert('Error occurred in recognition: ' + event.error);
//                                };
//                            } else {
//                                alert('Voice input is not supported in this browser.');
//                                
//                            }
//                        }
//                    </script>
//                </body>
//            </html>
//
//            """)
//            .edgesIgnoringSafeArea(.all) // Expands the web view to the entire screen
//    }
//}
// -------------------working -------------------


//import SwiftUI
//import WebKit
//
//struct ContentView: View {
//    @StateObject private var speechRecognizer = SpeechRecognizer()
//    @State private var webView = WKWebView()
//
//    var body: some View {
//        ZStack(alignment: .bottomTrailing) {
//            URLWebView(webView: webView, urlString: "http://10.33.35.62:8080/")
//                .edgesIgnoringSafeArea(.all)
//
//            Button(action: {
//                if speechRecognizer.isRecording {
//                    speechRecognizer.stopRecording()
//                } else {
//                    speechRecognizer.startRecording { result in
//                        if let text = result {
//                            injectTextIntoWebView(text: text)
//                        }
//                    }
//                }
//            }) {
//                Image(systemName: speechRecognizer.isRecording ? "mic.circle.fill" : "mic.circle")
//                    .resizable()
//                    .frame(width: 60, height: 60)
//                    .padding()
//            }
//        }
//    }
//
//    private func injectTextIntoWebView(text: String) {
//        let escapedText = text.replacingOccurrences(of: "'", with: "\\'")
//        let jsCode = "document.getElementById('user-input').value = '\(escapedText)';"
//        webView.evaluateJavaScript(jsCode, completionHandler: nil)
//    }
//}
//
//struct URLWebView: UIViewRepresentable {
//    let webView: WKWebView
//    let urlString: String
//
//    func makeUIView(context: Context) -> WKWebView {
//        webView.navigationDelegate = context.coordinator
//        webView.configuration.preferences.javaScriptEnabled = true
//        webView.configuration.mediaTypesRequiringUserActionForPlayback = []
//
//        if let url = URL(string: urlString) {
//            let request = URLRequest(url: url)
//            webView.load(request)
//        }
//
//        return webView
//    }
//
//    func updateUIView(_ uiView: WKWebView, context: Context) {
//        // No updates needed in this method
//    }
//
//    func makeCoordinator() -> Coordinator {
//        Coordinator(self)
//    }
//
//    class Coordinator: NSObject, WKNavigationDelegate {
//        var parent: URLWebView
//
//        init(_ parent: URLWebView) {
//            self.parent = parent
//        }
//
//        func webView(_ webView: WKWebView, didFail navigation: WKNavigation!, withError error: Error) {
//            print("WebView navigation failed with error: \(error.localizedDescription)")
//        }
//    }
//}




//import SwiftUI
//import WebKit
//
//struct ContentView: View {
//    var body: some View {
////        URLWebView(urlString: "http://192.168.1.119:8080/")
//        URLWebView(urlString: "http://10.34.3.151:8080/")
//
//            .edgesIgnoringSafeArea(.all) // Expands the WebView to fill the screen
//    }
//}
//
//struct URLWebView: UIViewRepresentable {
//    let urlString: String
//
//    func makeUIView(context: Context) -> WKWebView {
//        let webView = WKWebView()
//        
//        // Enable JavaScript and media playback
//        webView.configuration.preferences.javaScriptEnabled = true
//        webView.configuration.mediaTypesRequiringUserActionForPlayback = []
//        
//        // Set the navigation delegate and scroll view delegate
//        webView.navigationDelegate = context.coordinator
//        webView.scrollView.delegate = context.coordinator
//
//        return webView
//    }
//
//    func updateUIView(_ webView: WKWebView, context: Context) {
//        if let url = URL(string: urlString) {
//            let request = URLRequest(url: url)
//            webView.load(request)
//        }
//    }
//
//    // Coordinator to handle navigation and scroll view actions
//    func makeCoordinator() -> Coordinator {
//        Coordinator()
//    }
//
//    class Coordinator: NSObject, WKNavigationDelegate, UIScrollViewDelegate {
//        // Implement navigation delegate methods if needed
//        func webView(_ webView: WKWebView, didFail navigation: WKNavigation!, withError error: Error) {
//            print("WebView navigation failed with error: \(error.localizedDescription)")
//        }
//        
//        // Implement UIScrollViewDelegate method to prevent zooming
//        func viewForZooming(in scrollView: UIScrollView) -> UIView? {
//            // Returning nil prevents zooming
//            return nil
//        }
//    }
//}


import SwiftUI
import WebKit
import AVFoundation // Import AVFoundation to request microphone permission

struct ContentView: View {
    var body: some View {
        URLWebView(urlString: "http://192.168.1.119:8080/")
            .edgesIgnoringSafeArea(.all)
            .onAppear {
                // Request microphone permission when the view appears
                AVAudioSession.sharedInstance().requestRecordPermission { granted in
                    if granted {
                        print("Microphone permission granted")
                    } else {
                        print("Microphone permission denied")
                    }
                }
            }
    }
}

struct URLWebView: UIViewRepresentable {
    let urlString: String

    func makeUIView(context: Context) -> WKWebView {
        let webView = WKWebView()
        
        // Enable JavaScript and media playback
        webView.configuration.preferences.javaScriptEnabled = true
        webView.configuration.mediaTypesRequiringUserActionForPlayback = []
        
        // Set the navigation delegate, scroll view delegate, and UI delegate
        webView.navigationDelegate = context.coordinator
        webView.scrollView.delegate = context.coordinator
        webView.uiDelegate = context.coordinator // Set the UI delegate

        return webView
    }

    func updateUIView(_ webView: WKWebView, context: Context) {
        if let url = URL(string: urlString) {
            let request = URLRequest(url: url)
            webView.load(request)
        }
    }

    // Coordinator to handle navigation, scroll view, and UI actions
    func makeCoordinator() -> Coordinator {
        Coordinator()
    }

    class Coordinator: NSObject, WKNavigationDelegate, UIScrollViewDelegate, WKUIDelegate {
        // Implement navigation delegate methods if needed
        func webView(_ webView: WKWebView, didFail navigation: WKNavigation!, withError error: Error) {
            print("WebView navigation failed with error: \(error.localizedDescription)")
        }
        
        // Implement UIScrollViewDelegate method to prevent zooming
//        func viewForZooming(in scrollView: UIScrollView) -> UIView? {
//            // Returning nil prevents zooming
//            return nil
//        }
        
        // Implement the method to handle media capture permission requests
        func webView(_ webView: WKWebView,
                     requestMediaCapturePermissionFor origin: WKSecurityOrigin,
                     initiatedByFrame frame: WKFrameInfo,
                     type: WKMediaCaptureType,
                     decisionHandler: @escaping (WKPermissionDecision) -> Void) {
            if type == .microphone {
                decisionHandler(.grant) // Grant microphone access
            } else {
                decisionHandler(.deny) // Deny other types of media capture
            }
        }
    }
}

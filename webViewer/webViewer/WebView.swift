//
//  WebView.swift
//  webViewer
//
//  Created by Kavin Rajasekaran on 9/26/24.
//

// WebView.swift

import SwiftUI
import WebKit

struct WebView: UIViewRepresentable {
    let htmlContent: String

    func makeUIView(context: Context) -> WKWebView {
        return WKWebView()
    }

    func updateUIView(_ uiView: WKWebView, context: Context) {
        uiView.loadHTMLString(htmlContent, baseURL: nil)
    }
}

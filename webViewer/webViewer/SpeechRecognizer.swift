//import Foundation
//import Speech
//import AVFoundation
//
//class SpeechRecognizer: NSObject, ObservableObject, SFSpeechRecognizerDelegate {
//    @Published var isRecording = false
//
//    private let speechRecognizer: SFSpeechRecognizer?
//    private var recognitionRequest: SFSpeechAudioBufferRecognitionRequest?
//    private var recognitionTask: SFSpeechRecognitionTask?
//    private let audioEngine = AVAudioEngine()
//    private var completionHandler: ((String?) -> Void)?
//
//    override init() {
//        // Set the locale explicitly to a supported language (e.g., English - United States)
//        speechRecognizer = SFSpeechRecognizer(locale: Locale(identifier: "en-US"))
//        super.init()
//        speechRecognizer?.delegate = self
//    }
//
//    func startRecording(completion: @escaping (String?) -> Void) {
//        self.completionHandler = completion
//        requestAuthorization()
//    }
//
//    private func requestAuthorization() {
//        SFSpeechRecognizer.requestAuthorization { status in
//            DispatchQueue.main.async {
//                switch status {
//                case .authorized:
//                    self.requestMicrophonePermission()
//                case .denied, .restricted, .notDetermined:
//                    print("Speech recognition authorization denied.")
//                    self.isRecording = false
//                @unknown default:
//                    print("Unknown speech recognition authorization status.")
//                    self.isRecording = false
//                }
//            }
//        }
//    }
//
//    private func requestMicrophonePermission() {
//        AVAudioSession.sharedInstance().requestRecordPermission { granted in
//            DispatchQueue.main.async {
//                if granted {
//                    self.startSession()
//                } else {
//                    print("Microphone access denied.")
//                    self.isRecording = false
//                }
//            }
//        }
//    }
//
//    private func startSession() {
//        if audioEngine.isRunning {
//            stopRecording()
//            return
//        }
//
//        do {
//            recognitionRequest = SFSpeechAudioBufferRecognitionRequest()
//            guard let recognitionRequest = recognitionRequest else {
//                print("Unable to create recognition request.")
//                return
//            }
//
//            recognitionRequest.shouldReportPartialResults = false
//
//            let audioSession = AVAudioSession.sharedInstance()
//            try audioSession.setCategory(.record, mode: .measurement, options: .duckOthers)
//            try audioSession.setMode(.measurement)
//            try audioSession.setActive(true, options: .notifyOthersOnDeactivation)
//
//            let inputNode = audioEngine.inputNode
//            let recordingFormat = inputNode.outputFormat(forBus: 0)
//
//            inputNode.removeTap(onBus: 0)
//            inputNode.installTap(onBus: 0, bufferSize: 1024, format: recordingFormat) { buffer, when in
//                self.recognitionRequest?.append(buffer)
//            }
//
//            audioEngine.prepare()
//            try audioEngine.start()
//            isRecording = true
//
//            recognitionTask = speechRecognizer?.recognitionTask(with: recognitionRequest!) { result, error in
//                if let result = result {
//                    self.completionHandler?(result.bestTranscription.formattedString)
//                    if result.isFinal {
//                        self.stopRecording()
//                    }
//                }
//
//                if let error = error {
//                    print("Recognition error: \(error.localizedDescription)")
//                    self.stopRecording()
//                }
//            }
//        } catch {
//            print("Audio Engine couldn't start due to error: \(error.localizedDescription)")
//            stopRecording()
//        }
//    }
//
//    func stopRecording() {
//        if audioEngine.isRunning {
//            audioEngine.stop()
//            audioEngine.inputNode.removeTap(onBus: 0)
//        }
//        recognitionRequest?.endAudio()
//        recognitionTask?.cancel()
//        recognitionRequest = nil
//        recognitionTask = nil
//        isRecording = false
//    }
//
//    // MARK: - SFSpeechRecognizerDelegate
//
//    func speechRecognizer(_ speechRecognizer: SFSpeechRecognizer, availabilityDidChange available: Bool) {
//        print("Speech recognizer availability changed: \(available)")
//        if !available {
//            print("Speech recognition is not available at the moment.")
//            stopRecording()
//        }
//    }
//}

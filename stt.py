# import speech_recognition as sr

# # initialize recognizer
# recognizer = sr.Recognizer()

# # Function to capture and transcribe speech
# def listen_speech():
#     with sr.Microphone() as source:
#         print("Listening...")
#         recognizer.adjust_for_ambient_noise(source, duration=0.5) # Adjusting for background noise
#         audio = recognizer.listen(source)

#         try:
#             # use google web speech API for transcription
#             text = recognizer.recognize_google_cloud(audio)
#             print("You: ", text)
#             return text
#         except sr.UnknownValueError:
#             print("Sorry, I didn't catch that. Please repeat.")
#             return None
#         except sr.RequestError:
#             print("API unavailable or network error.")
#             return None

import speech_recognition as sr

# Initialize recognizer
recognizer = sr.Recognizer()

def test_speech_to_text():
    with sr.Microphone() as source:
        print("Say something...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)  # Adjust for background noise
        recognizer.energy_threshold = 300  # Experiment with values between 300-400 for quieter environments


        # Setting thresholds to listen for longer inputs.
        recognizer.pause_threshold = 1.5
        recognizer.phrase_time_limit = 15

        print("Listening for up to 15 seconds...")
        audio = recognizer.listen(source, timeout=7) # Captures audio, timeout if no speech detected in 7 seconds

    try:
        # Use Google Web Speech API to recognize speech
        text = recognizer.recognize_google(audio)
        print("You said:", text)
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that.")
    except sr.RequestError:
        print("Network error or API unavailable.")

# Run the test
test_speech_to_text()

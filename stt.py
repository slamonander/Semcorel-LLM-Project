import speech_recognition as sr

# Initialize the speech recognizer
recognizer = sr.Recognizer()

# Function to capture and transcribe speech
def speech_to_text():
    with sr.Microphone() as source:
        print("Listening...")

        # Adjustments for better audio capture
        recognizer.adjust_for_ambient_noise(source, duration=0.5) # Background noise adjustments
        recognizer.energy_threshold = 300 # Use values 300-400 for quieter environments

        # Thresholds for longer audio inputs
        recognizer.pause_threshold = 1.5
        recognizer.phrase_time_limit = 15

        audio = recognizer.listen(source, timeout = 7) # Times out if no speech detected in 7 seconds.

        try:
            # Use Google Web Speech API for recognizing speech
            text = recognizer.recognize_google_cloud(audio)
            print("You: ", text)
            return text
        
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that. Please repeat.")
            return None
        
        except sr.RequestError:
            print("API unavailable or network error.")
            return None



# Run the test
speech_to_text()

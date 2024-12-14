import pyttsx3

def tts_engine():
    engine = pyttsx3.init()
    engine.setProperty('rate', 150) # Speed of speech
    engine.setProperty('volume', 0.9) # Volume (0.0 to 1.0)

    return engine

def speak(text, engine=None):
    if engine is None:
        engine = tts_engine()
    engine.say(text)
    engine.runAndWait()
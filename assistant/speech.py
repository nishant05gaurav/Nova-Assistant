# Importing necessary libraries
import pyttsx3
import platform
import time

def speak(text):
    print(f"Nova says: {text}")

    system = platform.system()

    if system == "Windows":
        engine = pyttsx3.init("sapi5")
        voices = engine.getProperty("voices")
        engine.setProperty("voice", voices[1].id)

    # For macOS
    elif system == "Darwin":  
        engine = pyttsx3.init("nsss")

    # For Linux
    else:  
        engine = pyttsx3.init("espeak")

    engine.setProperty("rate", 170)
    engine.setProperty("volume", 1.0)

    engine.say(text)
    engine.runAndWait()
    engine.stop()
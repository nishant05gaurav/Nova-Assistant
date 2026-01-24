import speech_recognition as sr
import random
import webbrowser
import datetime
from datetime import datetime

# Assistant modules
from assistant.speech import speak
from assistant.time_date import tell_time, tell_date
from assistant.webs_ops import openLink
from assistant.news_weather import news, weather
from assistant.calendar import gcalendar
from assistant.todo_ops import todo_voice_handler
from assistant.gemini_api import ask_gemini
from assistant.favmusic import music
from assistant.quotes_facts import quotes, facts

# Initialize recognizer
recognizer = sr.Recognizer()

def take_command():
    """Listen and recognize voice command"""
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print(f"User said: {command}")
        return command.lower()

    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that.")
        return ""

    except sr.RequestError as e:
        print(f"Speech service error: {e}")
        return ""

def play_music(command):
    """Play favorite music"""
    for song in music:
        if song in command:
            speak(f"Playing {song}")
            webbrowser.open(music[song])
            return True
    return False

def tell_quote_or_fact(command):
    """Speak random quotes or facts"""
    if "quote" in command:
        speak(random.choice(quotes))
        return True

    if "fact" in command:
        speak(random.choice(facts))
        return True
    return False

# def listening_nova(startAgain="nova"):
#     """
#     Keeps listening until the wake word is detected.
#     """
#     while True:
#         command = take_command()

        # if startAgain in command:
        #     speak("Aaaaahaa... sir")
        #     return


def greet():
    hour = datetime.now().hour

    if hour < 12:
        speak("Good morning sir")
    elif hour < 18:
        speak("Good afternoon sir")
    else:
        speak("Good evening sir")

    speak("I am Nova. How can I help you?")

def main():
    speak("Initializing Nova")
    greet()

    while True:
        # listening_nova("nova")
        command = take_command()

        if not command:
            continue

        # Exit
        if "exit" in command or "quit" in command or "stop" in command:
            speak("Goodbye sir.")
            break

        # Time & Date
        if "time" in command:
            tell_time()
            continue

        if "date" in command:
            tell_date()
            continue

        # Web
        if openLink(command):
            continue
        
        # Music
        if play_music(command):
            continue

        # Quotes / Facts
        if tell_quote_or_fact(command):
            continue

        # News & Weather
        news(command)
        weather(command)

        # Calendar
        gcalendar(command)

        # Todo
        todo_voice_handler(command)

        # Gemini AI
        if "who" in command or "what" in command or "why" in command or "tell" in command or "how" in command:
            ask_gemini(command)
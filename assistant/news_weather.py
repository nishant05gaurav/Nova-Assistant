# Importing necessary libraries
import speech_recognition as sr
import pyttsx3
import requests
from assistant.speech import speak

# Initialize Recognizer for speech input
recognizer = sr.Recognizer()

# Initialise Engine:
engine = pyttsx3.init()

# API's Credentials:
newsApi = "570354365b19664a93a33fdbf3f3c9ed"
weatherApi = "570354365b19664a93a33fdbf3f3c9ed"

# News Section:
def news(command):
    '''
        Fetch and speak out the latest top news headlines from India.
        
        This function checks whether the user's command contains the word "news".
        If yes, it requests the top headlines from the NewsAPI, extracts the 
        article titles, and reads them aloud using the `speak()` function.
    '''
    if "news" in command.lower():
        try:
            
            # Fetching top news Headlines:
            r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsApi}")
                
            # Convert JSON response to a Python dictionary
            data = r.json()     

            # It makes sure that if the "articles" key is present in the dictionary we get from the JSON, then it will added in the articles; or else it'll assighn a empty list
            articles = data.get('articles', [])

            # Iterating and speaking each news headlines
            for article in articles: 
                speak(article['title'])
        except:
            speak("Couldn't fetch the news, there was an error.")

# Weather Section:
def weather(command):
    """
        Fetch and speak the current weather details for either the user's 
        current location or a specific city based on voice input.

        This function first checks if the user's command contains the keyword 
        "weather". If yes, it asks whether the user wants the weather of the 
        current location or a specific city. It listens to the user's reply, 
        determines the city name accordingly, retrieves weather data from the 
        OpenWeatherMap API, and finally speaks the temperature, pressure, 
        and humidity levels.
    """
    if "weather" in command.lower():
        speak("Current location or Specific City?")
        
        try:
            # Listening User's choice:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                choice = recognizer.listen(source, timeout = 5, phrase_time_limit = 4)
                choice = recognizer.recognize_google(choice).lower()
                
            city = ""
            
            if "current" in choice:
                city = requests.get("https://ipinfo.io/json").json().get("city", "")
                
            elif "specific" in choice:
                speak("Which city?")
                recognizer.adjust_for_ambient_noise(source, duration = 0.5)
                city_audio = recognizer.listen(source, timeout = 5, phrase_time_limit = 4)
                city = recognizer.recognize_google(city_audio)
                
            else:
                speak("Didn't understand.")
                return
            
            if city:
                # Constructing the URL to get the weathet data
                URL = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weatherApi}&units=metric"


                # Fetching the response:
                response = requests.get(URL).json()

                # Extract temperature, pressure, and humidity
                temperature = response["main"]["temp"]
                pressure = response["main"]["pressure"]
                humidity = response["main"]["humidity"]

                # Printing the result
                speak(f"Temperature (in Celsius) = {temperature}°C, Atmospheric Pressure (in hPa) = {pressure} hPa and the Humidity (in percentage) = {humidity}%")
        except:
            speak("Couldn't fetch the weather, there was an error.")
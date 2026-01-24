import time
from datetime import datetime
from assistant.speech import speak

# Function to tell current time
def tell_time():
    """
    Announces the current system time using speech output.

    This function retrieves the current local time using the `datetime` module,
    formats it into a 12-hour clock format with AM/PM, and then calls the `speak`
    function to audibly announce the time.
    """
    
    # Get the current system time
    now = datetime.now()
    
    # Format the time in 12-hour format with AM/PM (Example: "02:15 PM")
    current_time = now.strftime("%I:%M %p")
    
     # Speak the formatted time     
    speak(f"The current time is {current_time}")

# Function to tell current date
def tell_date():
    '''
    Announces the current time using the speech output
    
    This function retrives the current time using the 'datetime' module,
    formats it and then calls the 'speak' function to audibly announce the 
    day.
    '''
    # Get the current date and time from the system
    today = datetime.now()
    
    # Format the date into a readable string like "Monday, September 10, 2025"
    current_date = today.strftime("%A, %B %d, %Y")
    
    # Speak the formatted date
    speak(f"Today is {current_date}")
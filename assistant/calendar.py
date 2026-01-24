# Importing necessary libraries
from __future__ import print_function
import datetime
import os.path
import google.generativeai as genai
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from assistant.speech import speak

'''
Google requires SCOPES to define what permission your app is requesting.
"calendar.readonly" → You can only read events, not create/update/delete.
Without SCOPES: Access not granted or insufficient permissions.
'''
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def format_datetime (dt_str):
    '''
    Convert Google's date/dateTime into human-readable format.
    '''
    try:
        dt = datetime.datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
        return dt.strftime("%A, %d %B %Y at %I:%M %p")
    
    except:
        # If only full-day date (no time)
        dt = datetime.datetime.strptime(dt_str, "%Y-%m-%d")
        return dt.strftime("%A, %d %B %Y")

def get_calendar_service():
    """
    Authenticate the user (using OAuth 2.0) and return a Google Calendar API service object.

    Steps:
    1. Check if token.json exists → load saved credentials.
    2. If token is missing/invalid/expired → run OAuth login flow.
    3. Save new token.json after successful login.
    4. Build and return the Google Calendar API service.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:

        # Loads identity from credentials.json and opens browser then user gives permission
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)

        # Saving new tokens to avoid login for future 
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
            
    service = build('calendar', 'v3', credentials=creds)
    return service

def list_events(n=5):
    """
    Fetch the user's next 'n' upcoming events.

    Parameters:
        n (int): Number of upcoming events to fetch.

    Returns:
        list of str:
            A list where each item is formatted as:
            "START_TIME - EVENT_TITLE"
            OR a single element: ["No upcoming events found."]
    """
    service = get_calendar_service()
    now = datetime.datetime.utcnow().isoformat() + 'Z'              # 'Z' indicates UTC time

    # Fetch the upcoming events
    events_result = service.events().list(
                                          calendarId='primary',
                                          timeMin=now,              # Only future events
                                          maxResults=n, 
                                          singleEvents=True,        # Break recurring events into separate ones
                                          orderBy='startTime'       # Sort by event start time
                                          ).execute()
    events = events_result.get('items', [])
    
    # If no events found
    if not events:
        return ["No upcoming events found."]

    event_list = []
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        summary = event.get('summary', 'No Title')
        readable = format_datetime(start)
        event_list.append(f"{readable} — {summary}")
    return event_list

# Google Calendar
def gcalendar(cmmd):
    """
    If the user mentions "calendar" or "events",
    the assistant speaks the next 5 upcoming events.
    """
    if "calendar" in cmmd.lower() or "events" in cmmd.lower():
        speak("Here are your upcoming events:")
        events = list_events(5)  # next 5 events
        for e in events:
            speak(e)
        return True
    return False
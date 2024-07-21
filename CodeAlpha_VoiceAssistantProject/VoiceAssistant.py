
# import when I get the Google Calendar API
from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
# SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

import os #provides a collection of functions for interacting with the operating system
import time
import playsound
import speech_recognition as sr 
from gtts import gTTS

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
MONTHS = ["january", "february", "march", "april", "may", "june","july", "august", "september","october", "november", "december"]
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
DAY_EXTENTIONS = ["rd", "th", "st", "nd"]

def speak(text): # this is just for tacking text and reading
    tts = gTTS(text=text, lang='en', slow=False)
    filename = 'temp.mp3'
    tts.save(filename)
    playsound.playsound(filename)
    os.close(filename) # we close mp3 file before the anohter task
    os.remove(filename)
    

# speak("Please say everything you want!")

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""
        try:
            said = r.recognize_google(audio)
            print("You said: ", said)
        except Exception as e:
            print("Exception: ", str(e))
    return said

def authenticate_google():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    return service


def get_events(n, service):
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print(f'Getting the upcoming {n} events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=n, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])


def get_date(text):
    text = text.lower()
    today = datetime.date.today()
    
    if text.count("today") > 0:
        return today
    day = -1
    day_of_week = -1
    month = -1
    year = today.year
    
    for word in text.split():
        if word in MONTHS:
            month = month.index(word) + 1
        elif word in DAYS:
            day_of_week = DAYS.index(word)
        elif word.isdigit():
            day = int(word)
        else:
            for ext in DAY_EXTENTIONS:
                found = word.find(ext)
                if found > 0:
                    try:
                        day = int(word[:found])
                    except:
                        pass
    if month < today.month & month != -1:
        year += 1
    if day < today.day & month != -1 & day != -1:
        month += 1
    
    
                    

service = authenticate_google()
get_events(2, service)
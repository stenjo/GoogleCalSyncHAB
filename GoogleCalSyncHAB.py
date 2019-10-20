#######################################################################################################################
#
# GoogleCalSyncHAB
# Fetches events from a google calendar and sends them to OpenHAB
#
# Code based in part on this article: https://medium.com/@butteredwaffles/working-with-google-calendar-api-8121d5048597
#
#######################################################################################################################

# Imports
from __future__ import print_function
import datetime
import pickle
import os.path
import Settings as S
import requests
import json
import time
import dateutil.parser as dateparser
from urllib import request, parse
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Globals to be moved to config file

def sendEventToOpenHAB(index, event):

    EventStart = dateparser.parse(event['start'].get('dateTime', event['start'].get('date')))
    EventEnd = dateparser.parse(event['end'].get('dateTime', event['end'].get('date')))

    data = {
        'summary'       : event['summary'] if 'summary' in event else '',
        'location'      : event['location'] if 'location' in event else '',
        'description'   : event['description'] if 'description' in event else '',
        'startDate'     : EventStart.strftime('%Y-%m-%d'),
        'startTime'     : EventStart.strftime('%H:%M'),
        'endDate'       : EventEnd.strftime('%Y-%m-%d'),
        'endTime'       : EventEnd.strftime('%H:%M'),
        'allDay'        : True if 'date' in event['start'] else False,
        'multipleDays'  : False if EventStart.strftime('%Y-%m-%d') == EventEnd.strftime('%Y-%m-%d') else True
    }

    postMessage(index, data, S.TrimmedHostAndPort)

def postMessage(index, info, target, postFix = ''):
    url = 'http://' + target + '/rest/items/' + S.OpenHABItemPrefix + 'Event' + str(index) + postFix
    OpenHABResponse = requests.post(url, data = json.dumps(info).encode('utf-8'), allow_redirects = True)

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', S.CalendarScope)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    # print('Getting the upcoming 10 events')

    RetrievedEvents = []
    for calendarId in S.CalendarIds:
        events_result = service.events().list(
            calendarId=calendarId, 
            timeMin=now,
            maxResults=10, 
            singleEvents=True,
            orderBy='startTime').execute()
        RetrievedEvents +=  events_result.get('items', [])

    for event in RetrievedEvents:
        event['timestamp'] = dateparser.parse(event['start'].get('dateTime', event['start'].get('date'))).timestamp()

    RetrievedEvents.sort(key=lambda x: float(x['timestamp']), reverse=False)

    if not RetrievedEvents:
        # print('No upcoming events found.')
        exit()

    for index in range(int(S.CalendarMaxEvents)):
        if index < len(RetrievedEvents):
            event = RetrievedEvents[index]
            start = event['start'].get('dateTime')
            sendEventToOpenHAB(index+1, event)
        else:
            sendEventToOpenHAB(index+1, {})
        time.sleep(1)

if __name__ == '__main__':
    main()


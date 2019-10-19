import configparser
import os

ApplicationDir = os.path.dirname(os.path.abspath(__file__))
# HomeDir = os.path.expanduser('~')
# CredentialDir = os.path.join(HomeDir, '.credentials')

# if not os.path.exists(CredentialDir):
#     os.makedirs(CredentialDir)

# CredentialFilePath = os.path.join(CredentialDir, 'GoogleCalSyncHAB.json')
CalSyncHABSettings = os.path.join(ApplicationDir, 'GoogleCalSyncHAB.ini')

Settings = configparser.ConfigParser()
Settings.read(CalSyncHABSettings)

ApplicationName = Settings.get('General', 'ApplicationName')

CalendarScope = Settings.get('Calendar', 'Scope')
CalendarIds = Settings.get('Calendar', 'CalendarId').split(',')
CalendarMaxEvents = Settings.get('Calendar', 'MaxEvents')
CalendarTimeZone = Settings.get('Calendar', 'TimeZone')
CalendarClientSecretFile = Settings.get('Calendar', 'ClientSecretFile')

OpenHABHostName = Settings.get('OpenHAB', 'HostName')
OpenHABPort = Settings.get('OpenHAB', 'Port')
OpenHABItemPrefix = Settings.get('OpenHAB', 'ItemPrefix')

TrimmedHostAndPort = OpenHABHostName.strip()
if OpenHABPort.strip() != '':
    TrimmedHostAndPort = OpenHABHostName.strip() + ':' + OpenHABPort.strip()


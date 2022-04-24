# Text Home Control

Small server that uses Twilio and interacts with your local Hue API.

## .env file @ ./src/.env
```pycon
TZ = America/New_York

HUE_HUB_URL = http://<HUE-HUB-ADDRESS>
HUE_HUB_USERNAME = <HUE-HUB-USERNAME>

SNAKE_URL = http://<CLIMATE-SENSOR-URL>/values

TWILIO_SID = <TWILIO-SID>
TWILIO_ACCT_TOKEN = <TWILIO-ACCT-TOKEN>
TWILIO_FROM_NUMBER = <TWILIO-FROM-URL>
TWILIO_WHITELIST = True
```

## .whitelist file @ ./src/.whitelist
This is a file that contains a list of phone numbers that can interact with your system. One phone number per line.

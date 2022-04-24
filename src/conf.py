import os
from dotenv import load_dotenv


class Config:
    load_dotenv()

    TZ = os.environ['TZ']

    HUE_HUB_URL = os.environ['HUE_HUB_URL']
    HUE_HUB_USERNAME = os.environ['HUE_HUB_USERNAME']

    SNAKE_URL = os.environ['SNAKE_URL']

    TWILIO_SID = os.environ['TWILIO_SID']
    TWILIO_ACCT_TOKEN = os.environ['TWILIO_ACCT_TOKEN']
    TWILIO_FROM_NUMBER = os.environ['TWILIO_FROM_NUMBER']
    TWILIO_IS_WHITELISTED = os.environ['TWILIO_WHITELIST']
    TWILIO_WHITELIST_NUMBERS = []

    if TWILIO_IS_WHITELISTED:
        _whitelist_file = open('.whitelist', 'r')
        _whitelisted_file_lines = [line.replace('\n','') for line in _whitelist_file.readlines()]
        TWILIO_WHITELIST_NUMBERS.extend(_whitelisted_file_lines)

    print(f"Loaded config, {len(TWILIO_WHITELIST_NUMBERS)} whitelisted numbers")


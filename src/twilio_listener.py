import arrow
from twilio.rest import Client
from datetime import datetime
import pytz
import time
import threading
import socket



class TwilioThreadedListener:
    def __init__(self, acct_sid, acct_token, from_number, tz, handler, poll_time=3, whitelist=[]):
        self.twilio_client = Client(username=acct_sid, password=acct_token)
        self._from_number = from_number
        self._local_tz = pytz.timezone(tz)
        self._handler = handler
        self._poll_pd = poll_time
        self._whitelist = whitelist
        self._received_sids = set()

        startup_msg = f"Text Control Initialized on host {socket.gethostname()}. You are whitelisted, send 'help' for" \
                      f" documentation."

        for wl_number in self._whitelist:
            print(f"Alerting {wl_number} to initialization.")
            self.twilio_client.messages.create(to=wl_number, from_=self._from_number, body=startup_msg)

        self._main_loop_thread = threading.Thread(self._loop())
        self._main_loop_thread.start()
        print("Listener Thread started...")

    def _single_loop(self, utc):
        before = utc.shift(seconds=-self._poll_pd).datetime
        messages = self.twilio_client.messages.list(date_sent_after=before, date_sent_before=utc.datetime)

        received = [message for message in messages if
                    message.direction == "inbound"
                    and message.sid not in self._received_sids]

        rejections = []
        if len(self._whitelist) > 0:
            rejections = [message for message in received if
                        message.from_ not in self._whitelist]
            received = [message for message in received if
                        message.from_ in self._whitelist]

        # handle rejections, if any
        for message in rejections:
            self._received_sids.add(message.sid)
            rejection_msg = f"You are not whitelisted. Begone {message.from_}, begone!"
            self.twilio_client.messages.create(to=message.from_, from_=self._from_number, body=rejection_msg)

        # handle positive matches
        for message in received:
            self._received_sids.add(message.sid)
            response = self._handler(message)
            if response:
                self.twilio_client.messages.create(to=message.from_, from_=self._from_number, body=response)

    def _loop(self):

        while True:
            # 5 seconds before now:
            now_utc = arrow.utcnow()
            if now_utc.time().second % self._poll_pd == 0:
                self._single_loop(now_utc)
                time.sleep(self._poll_pd / 2)
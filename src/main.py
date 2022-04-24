#!/usr/local/bin/python
import json
import time
from munch import Munch
from twilio.rest.api.v2010.account.message import MessageInstance
from twilio_listener import TwilioThreadedListener
from hue_client import HueLocal
import requests as rq
from conf import Config


if __name__ == "__main__":

    cfg = Config()

    hueClient = HueLocal(base_url=cfg.HUE_HUB_URL,
                             username=cfg.HUE_HUB_USERNAME)


    def sms_callback(message:MessageInstance) -> str:
        """
        Given message, builds string response
        """

        if len(message.media.list()) == 0:
            print(f"Received text message '{message.body}' from {message.from_}")
            if "help" in message.body.lower():
                return "Lights can be controlled through hotwords. Replace [PIN] with your pin.\n" \
                       "  lights info -> display current state with light names\n" \
                       "  lights all on -> turn on all lights\n" \
                       "  lights all off -> turn off all lights\n" \
                       "  lights all flash1 -> turn off/on all lights one time\n" \
                       "  lights all flash2 -> turn on/off all lights one time\n" \
                       "  lights on:xx -> turn on light with id 'xx' - NOT IMPLEMENTED\n" \
                       "  lights off:xx -> turn off light with id 'xx' - NOT IMPLEMENTED\n" \
                       "Weather can be accessed as well:" \
                       "  wx:[zipcode] -> returns current weather - NOT IMPLEMENTED"
            elif "lights" in message.body.lower():
                if "info" in message.body.lower():
                    return hueClient.info()
                elif "on:" in message.body.lower():
                    return "not implemented - single on"
                elif "off:" in message.body.lower():
                    return "not implemented - single off"
                elif "all" in message.body.lower():
                    if "off" in message.body.lower():
                        hueClient.turn_off_all()
                        return f"{hueClient.get_light_count()} lights are now off"
                    elif "on" in message.body.lower():
                        hueClient.turn_on_all()
                        return f"{hueClient.get_light_count()} lights are now on"
                    elif "flash1" in message.body.lower():
                        hueClient.turn_off_all()
                        time.sleep(1)
                        hueClient.turn_on_all()
                        return f"{hueClient.get_light_count()} lights are now on"
                    elif "flash2" in message.body.lower():
                        hueClient.turn_on_all()
                        time.sleep(1)
                        hueClient.turn_off_all()
                        return f"{hueClient.get_light_count()} lights are now on"

                else:
                    return "invalid lights command"
            elif "wx:" in message.body.lower():
                return "not implemented"
            elif "snake" in message.body.lower():
                resp = rq.get(url=cfg.SNAKE_URL)
                if resp.status_code == 200:
                    snake_data = Munch(json.loads(resp.content))
                    temp_c = snake_data.temperature
                    temp_f = (temp_c * 9.0/5.0) + 32.0
                    rel_h = snake_data.humidity
                    temp_emoji = "😀"
                    humi_emoji = "😀"

                    if temp_f > 85:
                        temp_emoji = "🥵"
                    elif temp_f < 60:
                        temp_emoji = "🥶"

                    if rel_h > 80:
                        humi_emoji = "💦"
                    elif rel_h < 60:
                        humi_emoji = "🌵"

                    return "Snake Habitat\n" \
                           f"•Temperature {temp_emoji}: {temp_f:.0f}°F\n" \
                           f"•Humidity {humi_emoji}: {snake_data.humidity:.0f}%\n"
                else:
                    return "Error: Cannot reach snake climate sensor!"
            else:
                return f"Invalid Command '{message.body}'"
        else:
            print(f"Received message '{message.body}' from {message.from_} with {len(message.media.list())} media attachments")
            return "Media messages not implemented yet."
            # for media_item in message.media.list():
            #     media_uri = media_item.uri
            #     print(media_uri)


    TwilioThreadedListener(acct_sid=cfg.TWILIO_SID,
                           acct_token=cfg.TWILIO_ACCT_TOKEN,
                           from_number=cfg.TWILIO_FROM_NUMBER,
                           tz=cfg.TZ,
                           handler=sms_callback,
                           whitelist=(cfg.TWILIO_WHITELIST_NUMBERS if cfg.TWILIO_IS_WHITELISTED else []))

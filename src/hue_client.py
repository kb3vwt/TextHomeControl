import json

import requests
from munch import Munch
# documentation at https://developers.meethue.com/develop/get-started-2/


class HueLocal:
    def __init__(self, base_url, username):
        self.base_url = base_url
        self.username = username
        self.lights = self._get_lights()
        print(f"Hue Local system at {self.base_url} found with {len(self.lights)} lights!")
    def _get_lights(self):
        full_url = self.base_url + f"/api/{self.username}/lights"
        resp = requests.get(full_url)
        if resp.status_code != 200:
            raise RuntimeError("Failed to get list of lights.")
        else:
            return Munch(json.loads(resp.content))

    def get_light_count(self):
        return len(self.lights)

    def turn_on_all(self):
        for light_id in self.lights.keys():
            full_url = self.base_url + f"/api/{self.username}/lights/{light_id}/state"
            body = {
                'on': True
            }
            resp = requests.put(url=full_url, data=json.dumps(body))
            # print(f"Turning on light {light_id}: {resp.status_code}, {resp.content}")

    def turn_off_all(self):
        for light_id in self.lights.keys():
            full_url = self.base_url + f"/api/{self.username}/lights/{light_id}/state"
            body = {
                'on': False
            }
            resp = requests.put(url=full_url, data=json.dumps(body))
            # print(f"Turning off light {light_id}: {resp.status_code}, {resp.content}")

    def info(self):
        lights = self._get_lights()

        on = []
        off = []
        unreachable = []
        for light_id in lights.keys():
            if lights[light_id]['state']['on']:
                on.append(light_id)
            else:
                off.append(light_id)

            if not lights[light_id]['state']['reachable']:
                unreachable.append(light_id)

        status = f"System has {len(lights)} lights."
        status = status + f"Lights that are on ({len(on)}):\n"
        for light_id in on:
            name = lights[light_id]['name']
            brightness = f"{((float(lights[light_id]['state']['bri']) / 254) * 100):.0f}%"
            status = status + f"  - Light #{int(light_id):02d} ({name}) @ {brightness}\n"

        status = status + f"Lights that are off ({len(off)}):\n"
        for light_id in off:
            name = lights[light_id]['name']
            status = status + f"  - Light #{int(light_id):02d} ({name})\n"

        status = status + f"Lights that are unreachable ({len(unreachable)}):\n"
        for light_id in unreachable:
            status = status + f"  - Light #{int(light_id):02d} ({lights[light_id]['name']})\n"

        return status

import base64
import hashlib
import hmac
import time
import uuid
from dataclasses import dataclass
from typing import Any

import requests


@dataclass
class SwitchBotDevice:
    device_id: str
    device_name: str
    device_type: str


class SwitchBotAPIRepository:
    HOST_DOMAIN = "https://api.switch-bot.com"

    def __init__(self, token: str, secret: str):
        self.token = token
        self.secret = secret

    def __prepare_headers(self) -> dict[str, str]:
        # https://github.com/OpenWonderLabs/SwitchBotAPI
        nonce = uuid.uuid4()
        t = int(round(time.time() * 1000))
        string_to_sign = "{}{}{}".format(self.token, t, nonce)
        string_to_sign = bytes(string_to_sign, "utf-8")
        secret = bytes(self.secret, "utf-8")
        sign = base64.b64encode(
            hmac.new(secret, msg=string_to_sign, digestmod=hashlib.sha256).digest()
        )

        headers = {
            "Authorization": self.token,
            "Content-Type": "application/json",
            "charset": "utf8",
            "t": str(t),
            "sign": str(sign, "utf-8"),
            "nonce": str(nonce),
        }
        return headers

    def get_devices(self) -> list[SwitchBotDevice]:
        headers = self.__prepare_headers()
        response = requests.get(self.HOST_DOMAIN + "/v1.1/devices", headers=headers)
        try:
            response.raise_for_status()
        except Exception as e:
            raise SwitchBotGetDevicesError() from e

        devices = [
            SwitchBotDevice(e["deviceId"], e["deviceName"], e["deviceType"])
            for e in response.json()["body"]["deviceList"]
        ]
        return devices

    def get_status(self, device_id: str) -> dict[str, Any]:
        headers = self.__prepare_headers()
        response = requests.get(
            self.HOST_DOMAIN + f"/v1.1/devices/{device_id}/status", headers=headers
        )
        try:
            response.raise_for_status()
        except Exception as e:
            raise SwitchBotGetStatusError(device_id) from e

        return response.json()


class SwitchBotGetDevicesError(Exception):
    def __init__(self):
        super().__init__("failed to get devices from switchbot api.")


class SwitchBotGetStatusError(Exception):
    def __init__(self, device_id: str):
        super().__init__(f"failed to get status from switchbot api ({device_id}).")

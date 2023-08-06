# -*- coding: utf-8 -*-
# Copyright © 2022 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import base64

import contrast

from contrast.agent.settings_state import SettingsState


class BaseTsMessage:
    def __init__(self):
        self.settings = SettingsState()

        self.msg_name = None
        self.path = None
        self.base_url = f"{self.settings.api_url}/api/ng/"

        self.headers = {
            "Authorization": base64.b64encode(
                bytes(
                    f"{self.settings.api_user_name}:{self.settings.api_service_key}",
                    "utf8",
                )
            ),
            "API-Key": self.settings.api_key,
            "Server-Name": base64.b64encode(
                bytes(self.settings.get_server_name(), "utf8")
            ),
            "Server-Path": base64.b64encode(
                bytes(self.settings.get_server_path(), "utf8")
            ),
            "Server-Type": base64.b64encode(
                bytes(self.settings.get_server_type(), "utf8")
            ),
            "X-Contrast-Agent": f"Python {contrast.__version__}",
            "X-Contrast-Header-Encoding": "base64",
        }

        self.body = ""

    @property
    def name(self):
        return self.msg_name


class ServerActivity(BaseTsMessage):
    def __init__(self):
        super().__init__()

        self.msg_name = "activity_server"
        self.path = "activity/server"
        self.body = {"lastUpdate": self.settings.last_update}

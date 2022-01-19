from typing import Any, Dict

import attr
from synapse.module_api import ModuleApi


@attr.s(auto_attribs=True, frozen=True)
class FosdemDemoConfig:
    pass


class FosdemDemo:
    def __init__(self, config: FosdemDemoConfig, api: ModuleApi):
        # Keep a reference to the config and Module API
        self._api = api
        self._config = config

        self._api.register_third_party_rules_callbacks(
            on_new_event=self.change_room_avatar,
        )

    @staticmethod
    def parse_config(config: Dict[str, Any]) -> FosdemDemoConfig:
        # Parse the module's configuration here.
        # If there is an issue with the configuration, raise a
        # synapse.module_api.errors.ConfigError.
        #
        # Example:
        #
        #     some_option = config.get("some_option")
        #     if some_option is None:
        #          raise ConfigError("Missing option 'some_option'")
        #      if not isinstance(some_option, str):
        #          raise ConfigError("Config option 'some_option' must be a string")
        #
        return FosdemDemoConfig()

    async def change_room_avatar(self, event, state):
        if event.type == "m.room.message" or event.type == "m.room.encrypted":
            sender = event.sender
            membership = state.get(("m.room.member", sender))
            avatar_url = membership.content["avatar_url"]

            await self._api.create_and_send_event_into_room(
                {
                    "room_id": event.room_id,
                    "state_key": "",
                    "type": "m.room.avatar",
                    "sender": sender,
                    "content": {"url": avatar_url},
                }
            )

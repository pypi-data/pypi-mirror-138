from .base_class import TradfriBaseDevice as TradfriBaseDevice
from .const import ATTR_MODEL as ATTR_MODEL, CONF_GATEWAY_ID as CONF_GATEWAY_ID, DEVICES as DEVICES, DOMAIN as DOMAIN, KEY_API as KEY_API
from collections.abc import Callable as Callable
from homeassistant.components.cover import ATTR_POSITION as ATTR_POSITION, CoverEntity as CoverEntity
from homeassistant.config_entries import ConfigEntry as ConfigEntry
from homeassistant.core import HomeAssistant as HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback as AddEntitiesCallback
from pytradfri.command import Command as Command
from typing import Any

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None: ...

class TradfriCover(TradfriBaseDevice, CoverEntity):
    _attr_unique_id: Any
    def __init__(self, device: Command, api: Callable[[Union[Command, list[Command]]], Any], gateway_id: str) -> None: ...
    @property
    def extra_state_attributes(self) -> Union[dict[str, str], None]: ...
    @property
    def current_cover_position(self) -> Union[int, None]: ...
    async def async_set_cover_position(self, **kwargs: Any) -> None: ...
    async def async_open_cover(self, **kwargs: Any) -> None: ...
    async def async_close_cover(self, **kwargs: Any) -> None: ...
    async def async_stop_cover(self, **kwargs: Any) -> None: ...
    @property
    def is_closed(self) -> bool: ...
    _device: Any
    _device_control: Any
    _device_data: Any
    def _refresh(self, device: Command, write_ha: bool = ...) -> None: ...

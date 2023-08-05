from .const import CONF_DISABLE_RTSP as CONF_DISABLE_RTSP, DEVICES_THAT_ADOPT as DEVICES_THAT_ADOPT, DEVICES_WITH_ENTITIES as DEVICES_WITH_ENTITIES
from collections.abc import Generator, Iterable
from datetime import timedelta
from homeassistant.config_entries import ConfigEntry as ConfigEntry
from homeassistant.core import CALLBACK_TYPE as CALLBACK_TYPE, HomeAssistant as HomeAssistant, callback as callback
from homeassistant.helpers.event import async_track_time_interval as async_track_time_interval
from pyunifiprotect import ProtectApiClient as ProtectApiClient
from pyunifiprotect.data import Bootstrap as Bootstrap, ModelType as ModelType, WSSubscriptionMessage as WSSubscriptionMessage
from pyunifiprotect.data.base import ProtectAdoptableDeviceModel as ProtectAdoptableDeviceModel, ProtectDeviceModel as ProtectDeviceModel
from typing import Any

_LOGGER: Any

class ProtectData:
    _hass: Any
    _entry: Any
    _update_interval: Any
    _subscriptions: Any
    _unsub_interval: Any
    _unsub_websocket: Any
    last_update_success: bool
    api: Any
    def __init__(self, hass: HomeAssistant, protect: ProtectApiClient, update_interval: timedelta, entry: ConfigEntry) -> None: ...
    @property
    def disable_stream(self) -> bool: ...
    def get_by_types(self, device_types: Iterable[ModelType]) -> Generator[ProtectAdoptableDeviceModel, None, None]: ...
    async def async_setup(self) -> None: ...
    async def async_stop(self, *args: Any) -> None: ...
    async def async_refresh(self, *_: Any, force: bool = ...) -> None: ...
    def _async_process_ws_message(self, message: WSSubscriptionMessage) -> None: ...
    def _async_process_updates(self, updates: Union[Bootstrap, None]) -> None: ...
    def async_subscribe_device_id(self, device_id: str, update_callback: CALLBACK_TYPE) -> CALLBACK_TYPE: ...
    def async_unsubscribe_device_id(self, device_id: str, update_callback: CALLBACK_TYPE) -> None: ...
    def async_signal_device_id_update(self, device_id: str) -> None: ...

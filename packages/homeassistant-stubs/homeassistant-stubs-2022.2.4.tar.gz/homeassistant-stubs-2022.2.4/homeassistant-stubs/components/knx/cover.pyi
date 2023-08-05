from .const import DATA_KNX_CONFIG as DATA_KNX_CONFIG, DOMAIN as DOMAIN
from .knx_entity import KnxEntity as KnxEntity
from .schema import CoverSchema as CoverSchema
from collections.abc import Callable as Callable
from datetime import datetime
from homeassistant import config_entries as config_entries
from homeassistant.components.cover import ATTR_POSITION as ATTR_POSITION, ATTR_TILT_POSITION as ATTR_TILT_POSITION, CoverDeviceClass as CoverDeviceClass, CoverEntity as CoverEntity, SUPPORT_CLOSE as SUPPORT_CLOSE, SUPPORT_CLOSE_TILT as SUPPORT_CLOSE_TILT, SUPPORT_OPEN as SUPPORT_OPEN, SUPPORT_OPEN_TILT as SUPPORT_OPEN_TILT, SUPPORT_SET_POSITION as SUPPORT_SET_POSITION, SUPPORT_SET_TILT_POSITION as SUPPORT_SET_TILT_POSITION, SUPPORT_STOP as SUPPORT_STOP, SUPPORT_STOP_TILT as SUPPORT_STOP_TILT
from homeassistant.const import CONF_DEVICE_CLASS as CONF_DEVICE_CLASS, CONF_ENTITY_CATEGORY as CONF_ENTITY_CATEGORY, CONF_NAME as CONF_NAME, Platform as Platform
from homeassistant.core import HomeAssistant as HomeAssistant, callback as callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback as AddEntitiesCallback
from homeassistant.helpers.event import async_track_utc_time_change as async_track_utc_time_change
from homeassistant.helpers.typing import ConfigType as ConfigType
from typing import Any
from xknx import XKNX as XKNX
from xknx.devices import Cover as XknxCover, Device as XknxDevice

async def async_setup_entry(hass: HomeAssistant, config_entry: config_entries.ConfigEntry, async_add_entities: AddEntitiesCallback) -> None: ...

class KNXCover(KnxEntity, CoverEntity):
    _device: XknxCover
    _unsubscribe_auto_updater: Any
    _attr_entity_category: Any
    _attr_supported_features: Any
    _attr_device_class: Any
    _attr_unique_id: Any
    def __init__(self, xknx: XKNX, config: ConfigType) -> None: ...
    async def after_update_callback(self, device: XknxDevice) -> None: ...
    @property
    def current_cover_position(self) -> Union[int, None]: ...
    @property
    def is_closed(self) -> Union[bool, None]: ...
    @property
    def is_opening(self) -> bool: ...
    @property
    def is_closing(self) -> bool: ...
    async def async_close_cover(self, **kwargs: Any) -> None: ...
    async def async_open_cover(self, **kwargs: Any) -> None: ...
    async def async_set_cover_position(self, **kwargs: Any) -> None: ...
    async def async_stop_cover(self, **kwargs: Any) -> None: ...
    @property
    def current_cover_tilt_position(self) -> Union[int, None]: ...
    async def async_set_cover_tilt_position(self, **kwargs: Any) -> None: ...
    async def async_open_cover_tilt(self, **kwargs: Any) -> None: ...
    async def async_close_cover_tilt(self, **kwargs: Any) -> None: ...
    async def async_stop_cover_tilt(self, **kwargs: Any) -> None: ...
    def start_auto_updater(self) -> None: ...
    def stop_auto_updater(self) -> None: ...
    def auto_updater_hook(self, now: datetime) -> None: ...

import datetime
from .const import DATA_SUBSCRIBER as DATA_SUBSCRIBER, DOMAIN as DOMAIN
from .device_info import NestDeviceInfo as NestDeviceInfo
from collections.abc import Callable as Callable
from google_nest_sdm.camera_traits import RtspStream as RtspStream
from google_nest_sdm.device import Device as Device
from google_nest_sdm.event_media import EventMedia as EventMedia
from homeassistant.components.camera import Camera as Camera, SUPPORT_STREAM as SUPPORT_STREAM
from homeassistant.components.camera.const import STREAM_TYPE_WEB_RTC as STREAM_TYPE_WEB_RTC
from homeassistant.components.ffmpeg import async_get_image as async_get_image
from homeassistant.config_entries import ConfigEntry as ConfigEntry
from homeassistant.core import HomeAssistant as HomeAssistant
from homeassistant.exceptions import HomeAssistantError as HomeAssistantError, PlatformNotReady as PlatformNotReady
from homeassistant.helpers.entity import DeviceInfo as DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback as AddEntitiesCallback
from homeassistant.helpers.event import async_track_point_in_utc_time as async_track_point_in_utc_time
from homeassistant.util.dt import utcnow as utcnow
from typing import Any

_LOGGER: Any
PLACEHOLDER: Any
STREAM_EXPIRATION_BUFFER: Any

async def async_setup_sdm_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None: ...

class NestCamera(Camera):
    _device: Any
    _device_info: Any
    _stream: Any
    _create_stream_url_lock: Any
    _stream_refresh_unsub: Any
    _attr_is_streaming: Any
    _placeholder_image: Any
    def __init__(self, device: Device) -> None: ...
    @property
    def should_poll(self) -> bool: ...
    @property
    def unique_id(self) -> str: ...
    @property
    def name(self) -> Union[str, None]: ...
    @property
    def device_info(self) -> DeviceInfo: ...
    @property
    def brand(self) -> Union[str, None]: ...
    @property
    def model(self) -> Union[str, None]: ...
    @property
    def supported_features(self) -> int: ...
    @property
    def frontend_stream_type(self) -> Union[str, None]: ...
    async def stream_source(self) -> Union[str, None]: ...
    def _schedule_stream_refresh(self) -> None: ...
    stream: Any
    async def _handle_stream_refresh(self, now: datetime.datetime) -> None: ...
    async def async_will_remove_from_hass(self) -> None: ...
    async def async_added_to_hass(self) -> None: ...
    async def async_camera_image(self, width: Union[int, None] = ..., height: Union[int, None] = ...) -> Union[bytes, None]: ...
    async def async_handle_web_rtc_offer(self, offer_sdp: str) -> Union[str, None]: ...

from .const import CONF_HUB as CONF_HUB, DEFAULT_HUB as DEFAULT_HUB, DOMAIN as DOMAIN, LOGGER as LOGGER
from homeassistant import config_entries as config_entries
from homeassistant.components import dhcp as dhcp, zeroconf as zeroconf
from homeassistant.config_entries import ConfigEntry as ConfigEntry
from homeassistant.const import CONF_PASSWORD as CONF_PASSWORD, CONF_USERNAME as CONF_USERNAME
from homeassistant.data_entry_flow import FlowResult as FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession as async_get_clientsession
from typing import Any

class ConfigFlow(config_entries.ConfigFlow):
    VERSION: int
    _config_entry: Union[ConfigEntry, None]
    _default_user: Union[None, str]
    _default_hub: str
    def __init__(self) -> None: ...
    async def async_validate_input(self, user_input: dict[str, Any]) -> None: ...
    async def async_step_user(self, user_input: Union[dict[str, Any], None] = ...) -> FlowResult: ...
    async def async_step_dhcp(self, discovery_info: dhcp.DhcpServiceInfo) -> FlowResult: ...
    async def async_step_zeroconf(self, discovery_info: zeroconf.ZeroconfServiceInfo) -> FlowResult: ...
    async def async_step_reauth(self, user_input: Union[dict[str, Any], None] = ...) -> FlowResult: ...

from .const import BITMASK_SCHEMA as BITMASK_SCHEMA, CONF_DATA_COLLECTION_OPTED_IN as CONF_DATA_COLLECTION_OPTED_IN, DATA_CLIENT as DATA_CLIENT, DOMAIN as DOMAIN, EVENT_DEVICE_ADDED_TO_REGISTRY as EVENT_DEVICE_ADDED_TO_REGISTRY, LOGGER as LOGGER
from .helpers import async_enable_statistics as async_enable_statistics, update_data_collection_preference as update_data_collection_preference
from .migrate import ZWaveMigrationData as ZWaveMigrationData, async_get_migration_data as async_get_migration_data, async_map_legacy_zwave_values as async_map_legacy_zwave_values, async_migrate_legacy_zwave as async_migrate_legacy_zwave
from aiohttp import web as web
from collections.abc import Callable as Callable
from homeassistant.components import websocket_api as websocket_api
from homeassistant.components.http.view import HomeAssistantView as HomeAssistantView
from homeassistant.components.websocket_api.connection import ActiveConnection as ActiveConnection
from homeassistant.components.websocket_api.const import ERR_INVALID_FORMAT as ERR_INVALID_FORMAT, ERR_NOT_FOUND as ERR_NOT_FOUND, ERR_NOT_SUPPORTED as ERR_NOT_SUPPORTED, ERR_UNKNOWN_ERROR as ERR_UNKNOWN_ERROR
from homeassistant.config_entries import ConfigEntry as ConfigEntry, ConfigEntryState as ConfigEntryState
from homeassistant.const import CONF_URL as CONF_URL
from homeassistant.core import HomeAssistant as HomeAssistant, callback as callback
from homeassistant.exceptions import Unauthorized as Unauthorized
from homeassistant.helpers.aiohttp_client import async_get_clientsession as async_get_clientsession
from homeassistant.helpers.device_registry import DeviceEntry as DeviceEntry
from homeassistant.helpers.dispatcher import async_dispatcher_connect as async_dispatcher_connect
from typing import Any
from zwave_js_server.client import Client as Client
from zwave_js_server.model.controller import ControllerStatistics as ControllerStatistics, ProvisioningEntry, QRProvisioningInformation
from zwave_js_server.model.firmware import FirmwareUpdateFinished as FirmwareUpdateFinished, FirmwareUpdateProgress as FirmwareUpdateProgress
from zwave_js_server.model.log_message import LogMessage as LogMessage
from zwave_js_server.model.node import Node as Node, NodeStatistics as NodeStatistics

DATA_UNSUBSCRIBE: str
ID: str
ENTRY_ID: str
ERR_NOT_LOADED: str
NODE_ID: str
COMMAND_CLASS_ID: str
TYPE: str
PROPERTY: str
PROPERTY_KEY: str
VALUE: str
CONFIG: str
LEVEL: str
LOG_TO_FILE: str
FILENAME: str
ENABLED: str
FORCE_CONSOLE: str
VALUE_ID: str
STATUS: str
OPTED_IN: str
SECURITY_CLASSES: str
CLIENT_SIDE_AUTH: str
DRY_RUN: str
INCLUSION_STRATEGY: str
PIN: str
FORCE_SECURITY: str
PLANNED_PROVISIONING_ENTRY: str
QR_PROVISIONING_INFORMATION: str
QR_CODE_STRING: str
DSK: str
VERSION: str
GENERIC_DEVICE_CLASS: str
SPECIFIC_DEVICE_CLASS: str
INSTALLER_ICON_TYPE: str
MANUFACTURER_ID: str
PRODUCT_TYPE: str
PRODUCT_ID: str
APPLICATION_VERSION: str
MAX_INCLUSION_REQUEST_INTERVAL: str
UUID: str
SUPPORTED_PROTOCOLS: str
ADDITIONAL_PROPERTIES: str
FEATURE: str
UNPROVISION: str
MINIMUM_QR_STRING_LENGTH: int

def convert_planned_provisioning_entry(info: dict) -> ProvisioningEntry: ...
def convert_qr_provisioning_information(info: dict) -> QRProvisioningInformation: ...

PLANNED_PROVISIONING_ENTRY_SCHEMA: Any
QR_PROVISIONING_INFORMATION_SCHEMA: Any
QR_CODE_STRING_SCHEMA: Any

def async_get_entry(orig_func: Callable) -> Callable: ...
def async_get_node(orig_func: Callable) -> Callable: ...
def async_handle_failed_command(orig_func: Callable) -> Callable: ...
def async_register_api(hass: HomeAssistant) -> None: ...
async def websocket_network_status(hass: HomeAssistant, connection: ActiveConnection, msg: dict, entry: ConfigEntry, client: Client) -> None: ...
async def websocket_node_ready(hass: HomeAssistant, connection: ActiveConnection, msg: dict, node: Node) -> None: ...
async def websocket_node_status(hass: HomeAssistant, connection: ActiveConnection, msg: dict, node: Node) -> None: ...
async def websocket_node_metadata(hass: HomeAssistant, connection: ActiveConnection, msg: dict, node: Node) -> None: ...
async def websocket_ping_node(hass: HomeAssistant, connection: ActiveConnection, msg: dict, node: Node) -> None: ...
async def websocket_add_node(hass: HomeAssistant, connection: ActiveConnection, msg: dict, entry: ConfigEntry, client: Client) -> None: ...
async def websocket_grant_security_classes(hass: HomeAssistant, connection: ActiveConnection, msg: dict, entry: ConfigEntry, client: Client) -> None: ...
async def websocket_validate_dsk_and_enter_pin(hass: HomeAssistant, connection: ActiveConnection, msg: dict, entry: ConfigEntry, client: Client) -> None: ...
async def websocket_provision_smart_start_node(hass: HomeAssistant, connection: ActiveConnection, msg: dict, entry: ConfigEntry, client: Client) -> None: ...
async def websocket_unprovision_smart_start_node(hass: HomeAssistant, connection: ActiveConnection, msg: dict, entry: ConfigEntry, client: Client) -> None: ...
async def websocket_get_provisioning_entries(hass: HomeAssistant, connection: ActiveConnection, msg: dict, entry: ConfigEntry, client: Client) -> None: ...
async def websocket_parse_qr_code_string(hass: HomeAssistant, connection: ActiveConnection, msg: dict, entry: ConfigEntry, client: Client) -> None: ...
async def websocket_supports_feature(hass: HomeAssistant, connection: ActiveConnection, msg: dict, entry: ConfigEntry, client: Client) -> None: ...
async def websocket_stop_inclusion(hass: HomeAssistant, connection: ActiveConnection, msg: dict, entry: ConfigEntry, client: Client) -> None: ...
async def websocket_stop_exclusion(hass: HomeAssistant, connection: ActiveConnection, msg: dict, entry: ConfigEntry, client: Client) -> None: ...
async def websocket_remove_node(hass: HomeAssistant, connection: ActiveConnection, msg: dict, entry: ConfigEntry, client: Client) -> None: ...
async def websocket_replace_failed_node(hass: HomeAssistant, connection: ActiveConnection, msg: dict, entry: ConfigEntry, client: Client) -> None: ...
async def websocket_remove_failed_node(hass: HomeAssistant, connection: ActiveConnection, msg: dict, entry: ConfigEntry, client: Client) -> None: ...
async def websocket_begin_healing_network(hass: HomeAssistant, connection: ActiveConnection, msg: dict, entry: ConfigEntry, client: Client) -> None: ...
async def websocket_subscribe_heal_network_progress(hass: HomeAssistant, connection: ActiveConnection, msg: dict, entry: ConfigEntry, client: Client) -> None: ...
async def websocket_stop_healing_network(hass: HomeAssistant, connection: ActiveConnection, msg: dict, entry: ConfigEntry, client: Client) -> None: ...
async def websocket_heal_node(hass: HomeAssistant, connection: ActiveConnection, msg: dict, entry: ConfigEntry, client: Client) -> None: ...
async def websocket_refresh_node_info(hass: HomeAssistant, connection: ActiveConnection, msg: dict, node: Node) -> None: ...
async def websocket_refresh_node_values(hass: HomeAssistant, connection: ActiveConnection, msg: dict, node: Node) -> None: ...
async def websocket_refresh_node_cc_values(hass: HomeAssistant, connection: ActiveConnection, msg: dict, node: Node) -> None: ...
async def websocket_set_config_parameter(hass: HomeAssistant, connection: ActiveConnection, msg: dict, node: Node) -> None: ...
async def websocket_get_config_parameters(hass: HomeAssistant, connection: ActiveConnection, msg: dict, node: Node) -> None: ...
def filename_is_present_if_logging_to_file(obj: dict) -> dict: ...
async def websocket_subscribe_log_updates(hass: HomeAssistant, connection: ActiveConnection, msg: dict, entry: ConfigEntry, client: Client) -> None: ...
async def websocket_update_log_config(hass: HomeAssistant, connection: ActiveConnection, msg: dict, entry: ConfigEntry, client: Client) -> None: ...
async def websocket_get_log_config(hass: HomeAssistant, connection: ActiveConnection, msg: dict, entry: ConfigEntry, client: Client) -> None: ...
async def websocket_update_data_collection_preference(hass: HomeAssistant, connection: ActiveConnection, msg: dict, entry: ConfigEntry, client: Client) -> None: ...
async def websocket_data_collection_status(hass: HomeAssistant, connection: ActiveConnection, msg: dict, entry: ConfigEntry, client: Client) -> None: ...
async def websocket_abort_firmware_update(hass: HomeAssistant, connection: ActiveConnection, msg: dict, node: Node) -> None: ...
def _get_firmware_update_progress_dict(progress: FirmwareUpdateProgress) -> dict[str, int]: ...
async def websocket_subscribe_firmware_update_status(hass: HomeAssistant, connection: ActiveConnection, msg: dict, node: Node) -> None: ...

class FirmwareUploadView(HomeAssistantView):
    url: str
    name: str
    async def post(self, request: web.Request, config_entry_id: str, node_id: str) -> web.Response: ...

async def websocket_check_for_config_updates(hass: HomeAssistant, connection: ActiveConnection, msg: dict, entry: ConfigEntry, client: Client) -> None: ...
async def websocket_install_config_update(hass: HomeAssistant, connection: ActiveConnection, msg: dict, entry: ConfigEntry, client: Client) -> None: ...
def _get_controller_statistics_dict(statistics: ControllerStatistics) -> dict[str, int]: ...
async def websocket_subscribe_controller_statistics(hass: HomeAssistant, connection: ActiveConnection, msg: dict, entry: ConfigEntry, client: Client) -> None: ...
def _get_node_statistics_dict(statistics: NodeStatistics) -> dict[str, int]: ...
async def websocket_subscribe_node_statistics(hass: HomeAssistant, connection: ActiveConnection, msg: dict, node: Node) -> None: ...
async def websocket_migrate_zwave(hass: HomeAssistant, connection: ActiveConnection, msg: dict, entry: ConfigEntry, client: Client) -> None: ...

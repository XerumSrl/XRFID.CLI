from typing import Literal, cast

ManagementEventsConfigurationHeartbeatFieldsSystemItem = Literal['CPU', 'FLASH', 'GPI', 'GPO', 'HOSTNAME', 'MAC_ADDRESS', 'MACADDRESS', 'NTP', 'POWER_NEGOTIATION', 'POWER_SOURCE', 'RAM', 'SYSTEMTIME', 'TEMPERATURE', 'UPTIME']

MANAGEMENT_EVENTS_CONFIGURATION_HEARTBEAT_FIELDS_SYSTEM_ITEM_VALUES: set[ManagementEventsConfigurationHeartbeatFieldsSystemItem] = { 'CPU', 'FLASH', 'GPI', 'GPO', 'HOSTNAME', 'MAC_ADDRESS', 'MACADDRESS', 'NTP', 'POWER_NEGOTIATION', 'POWER_SOURCE', 'RAM', 'SYSTEMTIME', 'TEMPERATURE', 'UPTIME',  }

def check_management_events_configuration_heartbeat_fields_system_item(value: str) -> ManagementEventsConfigurationHeartbeatFieldsSystemItem:
    if value in MANAGEMENT_EVENTS_CONFIGURATION_HEARTBEAT_FIELDS_SYSTEM_ITEM_VALUES:
        return cast(ManagementEventsConfigurationHeartbeatFieldsSystemItem, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {MANAGEMENT_EVENTS_CONFIGURATION_HEARTBEAT_FIELDS_SYSTEM_ITEM_VALUES!r}")

from typing import Literal, cast

ManagementEventsConfigurationHeartbeatFieldsUserappsItem = Literal['CPU', 'INCOMING_DATA_BUFFER_PERCENTAGE_REMAINING', 'NUM_DATA_MESSAGES_RXED', 'NUM_DATA_MESSAGES_TXED', 'OUTGOING_DATA_BUFFER_PERCENTAGE_REMAINING', 'RAM', 'STATUS', 'UPTIME']

MANAGEMENT_EVENTS_CONFIGURATION_HEARTBEAT_FIELDS_USERAPPS_ITEM_VALUES: set[ManagementEventsConfigurationHeartbeatFieldsUserappsItem] = { 'CPU', 'INCOMING_DATA_BUFFER_PERCENTAGE_REMAINING', 'NUM_DATA_MESSAGES_RXED', 'NUM_DATA_MESSAGES_TXED', 'OUTGOING_DATA_BUFFER_PERCENTAGE_REMAINING', 'RAM', 'STATUS', 'UPTIME',  }

def check_management_events_configuration_heartbeat_fields_userapps_item(value: str) -> ManagementEventsConfigurationHeartbeatFieldsUserappsItem:
    if value in MANAGEMENT_EVENTS_CONFIGURATION_HEARTBEAT_FIELDS_USERAPPS_ITEM_VALUES:
        return cast(ManagementEventsConfigurationHeartbeatFieldsUserappsItem, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {MANAGEMENT_EVENTS_CONFIGURATION_HEARTBEAT_FIELDS_USERAPPS_ITEM_VALUES!r}")

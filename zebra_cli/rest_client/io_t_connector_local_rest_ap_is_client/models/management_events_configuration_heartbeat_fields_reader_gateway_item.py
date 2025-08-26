from typing import Literal, cast

ManagementEventsConfigurationHeartbeatFieldsReaderGatewayItem = Literal['CPU', 'INTERFACE_CONNECTION_STATUS', 'NOLOCKQ_DEPTH', 'NUM_DATA_MESSAGES_DROPPED', 'NUM_DATA_MESSAGES_RETAINED', 'NUM_DATA_MESSAGES_RXED', 'NUM_DATA_MESSAGES_TXED', 'NUM_ERRORS', 'NUM_MANAGEMENT_EVENTS_TXED', 'NUM_WARNINGS', 'RAM', 'UPTIME']

MANAGEMENT_EVENTS_CONFIGURATION_HEARTBEAT_FIELDS_READER_GATEWAY_ITEM_VALUES: set[ManagementEventsConfigurationHeartbeatFieldsReaderGatewayItem] = { 'CPU', 'INTERFACE_CONNECTION_STATUS', 'NOLOCKQ_DEPTH', 'NUM_DATA_MESSAGES_DROPPED', 'NUM_DATA_MESSAGES_RETAINED', 'NUM_DATA_MESSAGES_RXED', 'NUM_DATA_MESSAGES_TXED', 'NUM_ERRORS', 'NUM_MANAGEMENT_EVENTS_TXED', 'NUM_WARNINGS', 'RAM', 'UPTIME',  }

def check_management_events_configuration_heartbeat_fields_reader_gateway_item(value: str) -> ManagementEventsConfigurationHeartbeatFieldsReaderGatewayItem:
    if value in MANAGEMENT_EVENTS_CONFIGURATION_HEARTBEAT_FIELDS_READER_GATEWAY_ITEM_VALUES:
        return cast(ManagementEventsConfigurationHeartbeatFieldsReaderGatewayItem, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {MANAGEMENT_EVENTS_CONFIGURATION_HEARTBEAT_FIELDS_READER_GATEWAY_ITEM_VALUES!r}")

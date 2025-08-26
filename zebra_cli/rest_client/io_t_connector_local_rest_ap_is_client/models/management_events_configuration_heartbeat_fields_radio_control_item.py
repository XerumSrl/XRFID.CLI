from typing import Literal, cast

ManagementEventsConfigurationHeartbeatFieldsRadioControlItem = Literal['ANTENNAS', 'CPU', 'NUM_DATA_MESSAGES_TXED', 'NUM_ERRORS', 'NUM_RADIO_PACKETS_RXED', 'NUM_TAG_READS', 'NUM_TAG_READS_PER_ANTENNA', 'NUM_WARNINGS', 'RADIO_ACTIVITY', 'RADIO_CONNECTION', 'RAM', 'UPTIME']

MANAGEMENT_EVENTS_CONFIGURATION_HEARTBEAT_FIELDS_RADIO_CONTROL_ITEM_VALUES: set[ManagementEventsConfigurationHeartbeatFieldsRadioControlItem] = { 'ANTENNAS', 'CPU', 'NUM_DATA_MESSAGES_TXED', 'NUM_ERRORS', 'NUM_RADIO_PACKETS_RXED', 'NUM_TAG_READS', 'NUM_TAG_READS_PER_ANTENNA', 'NUM_WARNINGS', 'RADIO_ACTIVITY', 'RADIO_CONNECTION', 'RAM', 'UPTIME',  }

def check_management_events_configuration_heartbeat_fields_radio_control_item(value: str) -> ManagementEventsConfigurationHeartbeatFieldsRadioControlItem:
    if value in MANAGEMENT_EVENTS_CONFIGURATION_HEARTBEAT_FIELDS_RADIO_CONTROL_ITEM_VALUES:
        return cast(ManagementEventsConfigurationHeartbeatFieldsRadioControlItem, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {MANAGEMENT_EVENTS_CONFIGURATION_HEARTBEAT_FIELDS_RADIO_CONTROL_ITEM_VALUES!r}")

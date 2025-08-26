from typing import Literal, cast

EventConnectionsItemType = Literal['httpPost', 'keyboard-emulation', 'mqtt', 'mqtt-AWS', 'mqtt-AZURE', 'tcpip-server', 'WEBSOCKET']

EVENT_CONNECTIONS_ITEM_TYPE_VALUES: set[EventConnectionsItemType] = { 'httpPost', 'keyboard-emulation', 'mqtt', 'mqtt-AWS', 'mqtt-AZURE', 'tcpip-server', 'WEBSOCKET',  }

def check_event_connections_item_type(value: str) -> EventConnectionsItemType:
    if value in EVENT_CONNECTIONS_ITEM_TYPE_VALUES:
        return cast(EventConnectionsItemType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {EVENT_CONNECTIONS_ITEM_TYPE_VALUES!r}")

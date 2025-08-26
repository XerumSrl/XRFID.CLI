from typing import Literal, cast

GetReaderCapabilitesCapabilitiesEndpointTypesSupportedItemType = Literal['AWS_IOT_CORE', 'AZURE_IOT_HUB', 'HTTP', 'MQTT', 'MQTT_WS', 'TCPIP', 'WEBSOCKET']

GET_READER_CAPABILITES_CAPABILITIES_ENDPOINT_TYPES_SUPPORTED_ITEM_TYPE_VALUES: set[GetReaderCapabilitesCapabilitiesEndpointTypesSupportedItemType] = { 'AWS_IOT_CORE', 'AZURE_IOT_HUB', 'HTTP', 'MQTT', 'MQTT_WS', 'TCPIP', 'WEBSOCKET',  }

def check_get_reader_capabilites_capabilities_endpoint_types_supported_item_type(value: str) -> GetReaderCapabilitesCapabilitiesEndpointTypesSupportedItemType:
    if value in GET_READER_CAPABILITES_CAPABILITIES_ENDPOINT_TYPES_SUPPORTED_ITEM_TYPE_VALUES:
        return cast(GetReaderCapabilitesCapabilitiesEndpointTypesSupportedItemType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GET_READER_CAPABILITES_CAPABILITIES_ENDPOINT_TYPES_SUPPORTED_ITEM_TYPE_VALUES!r}")

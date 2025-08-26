from typing import Literal, cast

GetReaderCapabilitesCapabilitiesNetworkInterfacesItemType = Literal['BLUETOOTH', 'ETHERNET', 'WIFI']

GET_READER_CAPABILITES_CAPABILITIES_NETWORK_INTERFACES_ITEM_TYPE_VALUES: set[GetReaderCapabilitesCapabilitiesNetworkInterfacesItemType] = { 'BLUETOOTH', 'ETHERNET', 'WIFI',  }

def check_get_reader_capabilites_capabilities_network_interfaces_item_type(value: str) -> GetReaderCapabilitesCapabilitiesNetworkInterfacesItemType:
    if value in GET_READER_CAPABILITES_CAPABILITIES_NETWORK_INTERFACES_ITEM_TYPE_VALUES:
        return cast(GetReaderCapabilitesCapabilitiesNetworkInterfacesItemType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GET_READER_CAPABILITES_CAPABILITIES_NETWORK_INTERFACES_ITEM_TYPE_VALUES!r}")

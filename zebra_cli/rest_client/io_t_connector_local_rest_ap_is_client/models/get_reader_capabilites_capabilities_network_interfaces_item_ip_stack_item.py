from typing import Literal, cast

GetReaderCapabilitesCapabilitiesNetworkInterfacesItemIpStackItem = Literal['IPv4', 'IPv6']

GET_READER_CAPABILITES_CAPABILITIES_NETWORK_INTERFACES_ITEM_IP_STACK_ITEM_VALUES: set[GetReaderCapabilitesCapabilitiesNetworkInterfacesItemIpStackItem] = { 'IPv4', 'IPv6',  }

def check_get_reader_capabilites_capabilities_network_interfaces_item_ip_stack_item(value: str) -> GetReaderCapabilitesCapabilitiesNetworkInterfacesItemIpStackItem:
    if value in GET_READER_CAPABILITES_CAPABILITIES_NETWORK_INTERFACES_ITEM_IP_STACK_ITEM_VALUES:
        return cast(GetReaderCapabilitesCapabilitiesNetworkInterfacesItemIpStackItem, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GET_READER_CAPABILITES_CAPABILITIES_NETWORK_INTERFACES_ITEM_IP_STACK_ITEM_VALUES!r}")

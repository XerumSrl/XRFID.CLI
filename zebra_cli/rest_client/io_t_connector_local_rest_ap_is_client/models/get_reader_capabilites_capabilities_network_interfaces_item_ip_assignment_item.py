from typing import Literal, cast

GetReaderCapabilitesCapabilitiesNetworkInterfacesItemIpAssignmentItem = Literal['DHCP', 'STATIC']

GET_READER_CAPABILITES_CAPABILITIES_NETWORK_INTERFACES_ITEM_IP_ASSIGNMENT_ITEM_VALUES: set[GetReaderCapabilitesCapabilitiesNetworkInterfacesItemIpAssignmentItem] = { 'DHCP', 'STATIC',  }

def check_get_reader_capabilites_capabilities_network_interfaces_item_ip_assignment_item(value: str) -> GetReaderCapabilitesCapabilitiesNetworkInterfacesItemIpAssignmentItem:
    if value in GET_READER_CAPABILITES_CAPABILITIES_NETWORK_INTERFACES_ITEM_IP_ASSIGNMENT_ITEM_VALUES:
        return cast(GetReaderCapabilitesCapabilitiesNetworkInterfacesItemIpAssignmentItem, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GET_READER_CAPABILITES_CAPABILITIES_NETWORK_INTERFACES_ITEM_IP_ASSIGNMENT_ITEM_VALUES!r}")

from typing import Literal, cast

GetReaderCapabilitesCapabilitiesExternalSerialPortItem = Literal['DEBUG', 'NONE', 'USER']

GET_READER_CAPABILITES_CAPABILITIES_EXTERNAL_SERIAL_PORT_ITEM_VALUES: set[GetReaderCapabilitesCapabilitiesExternalSerialPortItem] = { 'DEBUG', 'NONE', 'USER',  }

def check_get_reader_capabilites_capabilities_external_serial_port_item(value: str) -> GetReaderCapabilitesCapabilitiesExternalSerialPortItem:
    if value in GET_READER_CAPABILITES_CAPABILITIES_EXTERNAL_SERIAL_PORT_ITEM_VALUES:
        return cast(GetReaderCapabilitesCapabilitiesExternalSerialPortItem, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GET_READER_CAPABILITES_CAPABILITIES_EXTERNAL_SERIAL_PORT_ITEM_VALUES!r}")

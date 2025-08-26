from typing import Literal, cast

GetReaderCapabilitesCapabilitiesAntennasItemType = Literal['EXTERNAL', 'INTERNAL']

GET_READER_CAPABILITES_CAPABILITIES_ANTENNAS_ITEM_TYPE_VALUES: set[GetReaderCapabilitesCapabilitiesAntennasItemType] = { 'EXTERNAL', 'INTERNAL',  }

def check_get_reader_capabilites_capabilities_antennas_item_type(value: str) -> GetReaderCapabilitesCapabilitiesAntennasItemType:
    if value in GET_READER_CAPABILITES_CAPABILITIES_ANTENNAS_ITEM_TYPE_VALUES:
        return cast(GetReaderCapabilitesCapabilitiesAntennasItemType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GET_READER_CAPABILITES_CAPABILITIES_ANTENNAS_ITEM_TYPE_VALUES!r}")

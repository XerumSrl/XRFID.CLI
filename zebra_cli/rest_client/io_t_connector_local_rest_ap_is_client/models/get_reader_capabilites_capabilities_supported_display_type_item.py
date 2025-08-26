from typing import Literal, cast

GetReaderCapabilitesCapabilitiesSupportedDisplayTypeItem = Literal['LCD', 'NONE']

GET_READER_CAPABILITES_CAPABILITIES_SUPPORTED_DISPLAY_TYPE_ITEM_VALUES: set[GetReaderCapabilitesCapabilitiesSupportedDisplayTypeItem] = { 'LCD', 'NONE',  }

def check_get_reader_capabilites_capabilities_supported_display_type_item(value: str) -> GetReaderCapabilitesCapabilitiesSupportedDisplayTypeItem:
    if value in GET_READER_CAPABILITES_CAPABILITIES_SUPPORTED_DISPLAY_TYPE_ITEM_VALUES:
        return cast(GetReaderCapabilitesCapabilitiesSupportedDisplayTypeItem, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GET_READER_CAPABILITES_CAPABILITIES_SUPPORTED_DISPLAY_TYPE_ITEM_VALUES!r}")

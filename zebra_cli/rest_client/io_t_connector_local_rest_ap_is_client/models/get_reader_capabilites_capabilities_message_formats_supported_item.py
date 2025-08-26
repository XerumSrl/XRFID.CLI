from typing import Literal, cast

GetReaderCapabilitesCapabilitiesMessageFormatsSupportedItem = Literal['JSON']

GET_READER_CAPABILITES_CAPABILITIES_MESSAGE_FORMATS_SUPPORTED_ITEM_VALUES: set[GetReaderCapabilitesCapabilitiesMessageFormatsSupportedItem] = { 'JSON',  }

def check_get_reader_capabilites_capabilities_message_formats_supported_item(value: str) -> GetReaderCapabilitesCapabilitiesMessageFormatsSupportedItem:
    if value in GET_READER_CAPABILITES_CAPABILITIES_MESSAGE_FORMATS_SUPPORTED_ITEM_VALUES:
        return cast(GetReaderCapabilitesCapabilitiesMessageFormatsSupportedItem, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GET_READER_CAPABILITES_CAPABILITIES_MESSAGE_FORMATS_SUPPORTED_ITEM_VALUES!r}")

from typing import Literal, cast

GetReaderCapabilitesCapabilitiesSupportedTagDataFormatItem = Literal['GS1', 'HEX']

GET_READER_CAPABILITES_CAPABILITIES_SUPPORTED_TAG_DATA_FORMAT_ITEM_VALUES: set[GetReaderCapabilitesCapabilitiesSupportedTagDataFormatItem] = { 'GS1', 'HEX',  }

def check_get_reader_capabilites_capabilities_supported_tag_data_format_item(value: str) -> GetReaderCapabilitesCapabilitiesSupportedTagDataFormatItem:
    if value in GET_READER_CAPABILITES_CAPABILITIES_SUPPORTED_TAG_DATA_FORMAT_ITEM_VALUES:
        return cast(GetReaderCapabilitesCapabilitiesSupportedTagDataFormatItem, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GET_READER_CAPABILITES_CAPABILITIES_SUPPORTED_TAG_DATA_FORMAT_ITEM_VALUES!r}")

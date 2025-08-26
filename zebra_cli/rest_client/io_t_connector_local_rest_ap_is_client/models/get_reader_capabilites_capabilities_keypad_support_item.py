from typing import Literal, cast

GetReaderCapabilitesCapabilitiesKeypadSupportItem = Literal['28-KEY', 'NONE']

GET_READER_CAPABILITES_CAPABILITIES_KEYPAD_SUPPORT_ITEM_VALUES: set[GetReaderCapabilitesCapabilitiesKeypadSupportItem] = { '28-KEY', 'NONE',  }

def check_get_reader_capabilites_capabilities_keypad_support_item(value: str) -> GetReaderCapabilitesCapabilitiesKeypadSupportItem:
    if value in GET_READER_CAPABILITES_CAPABILITIES_KEYPAD_SUPPORT_ITEM_VALUES:
        return cast(GetReaderCapabilitesCapabilitiesKeypadSupportItem, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GET_READER_CAPABILITES_CAPABILITIES_KEYPAD_SUPPORT_ITEM_VALUES!r}")

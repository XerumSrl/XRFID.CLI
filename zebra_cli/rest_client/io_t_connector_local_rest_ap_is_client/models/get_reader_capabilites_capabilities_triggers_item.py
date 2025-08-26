from typing import Literal, cast

GetReaderCapabilitesCapabilitiesTriggersItem = Literal['GPI', 'HANDHELD']

GET_READER_CAPABILITES_CAPABILITIES_TRIGGERS_ITEM_VALUES: set[GetReaderCapabilitesCapabilitiesTriggersItem] = { 'GPI', 'HANDHELD',  }

def check_get_reader_capabilites_capabilities_triggers_item(value: str) -> GetReaderCapabilitesCapabilitiesTriggersItem:
    if value in GET_READER_CAPABILITES_CAPABILITIES_TRIGGERS_ITEM_VALUES:
        return cast(GetReaderCapabilitesCapabilitiesTriggersItem, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GET_READER_CAPABILITES_CAPABILITIES_TRIGGERS_ITEM_VALUES!r}")

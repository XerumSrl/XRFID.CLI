from typing import Literal, cast

GetReaderCapabilitesCapabilitiesSupportedPowerSourceItem = Literal['BATTERY', 'DC', 'POE', 'POE+']

GET_READER_CAPABILITES_CAPABILITIES_SUPPORTED_POWER_SOURCE_ITEM_VALUES: set[GetReaderCapabilitesCapabilitiesSupportedPowerSourceItem] = { 'BATTERY', 'DC', 'POE', 'POE+',  }

def check_get_reader_capabilites_capabilities_supported_power_source_item(value: str) -> GetReaderCapabilitesCapabilitiesSupportedPowerSourceItem:
    if value in GET_READER_CAPABILITES_CAPABILITIES_SUPPORTED_POWER_SOURCE_ITEM_VALUES:
        return cast(GetReaderCapabilitesCapabilitiesSupportedPowerSourceItem, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GET_READER_CAPABILITES_CAPABILITIES_SUPPORTED_POWER_SOURCE_ITEM_VALUES!r}")

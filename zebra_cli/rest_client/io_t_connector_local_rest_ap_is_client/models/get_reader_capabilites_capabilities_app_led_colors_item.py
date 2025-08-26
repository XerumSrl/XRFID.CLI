from typing import Literal, cast

GetReaderCapabilitesCapabilitiesAppLedColorsItem = Literal['AMBER', 'GREEN', 'RED']

GET_READER_CAPABILITES_CAPABILITIES_APP_LED_COLORS_ITEM_VALUES: set[GetReaderCapabilitesCapabilitiesAppLedColorsItem] = { 'AMBER', 'GREEN', 'RED',  }

def check_get_reader_capabilites_capabilities_app_led_colors_item(value: str) -> GetReaderCapabilitesCapabilitiesAppLedColorsItem:
    if value in GET_READER_CAPABILITES_CAPABILITIES_APP_LED_COLORS_ITEM_VALUES:
        return cast(GetReaderCapabilitesCapabilitiesAppLedColorsItem, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GET_READER_CAPABILITES_CAPABILITIES_APP_LED_COLORS_ITEM_VALUES!r}")

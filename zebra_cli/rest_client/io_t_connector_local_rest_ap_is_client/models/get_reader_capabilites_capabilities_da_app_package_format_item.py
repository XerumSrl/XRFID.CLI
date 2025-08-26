from typing import Literal, cast

GetReaderCapabilitesCapabilitiesDaAppPackageFormatItem = Literal['DEBIAN']

GET_READER_CAPABILITES_CAPABILITIES_DA_APP_PACKAGE_FORMAT_ITEM_VALUES: set[GetReaderCapabilitesCapabilitiesDaAppPackageFormatItem] = { 'DEBIAN',  }

def check_get_reader_capabilites_capabilities_da_app_package_format_item(value: str) -> GetReaderCapabilitesCapabilitiesDaAppPackageFormatItem:
    if value in GET_READER_CAPABILITES_CAPABILITIES_DA_APP_PACKAGE_FORMAT_ITEM_VALUES:
        return cast(GetReaderCapabilitesCapabilitiesDaAppPackageFormatItem, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GET_READER_CAPABILITES_CAPABILITIES_DA_APP_PACKAGE_FORMAT_ITEM_VALUES!r}")

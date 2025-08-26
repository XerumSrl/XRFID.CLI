from typing import Literal, cast

GetReaderCapabilitesCapabilitiesDaLanguageBindingsItem = Literal['NODEJS', 'PYTHON']

GET_READER_CAPABILITES_CAPABILITIES_DA_LANGUAGE_BINDINGS_ITEM_VALUES: set[GetReaderCapabilitesCapabilitiesDaLanguageBindingsItem] = { 'NODEJS', 'PYTHON',  }

def check_get_reader_capabilites_capabilities_da_language_bindings_item(value: str) -> GetReaderCapabilitesCapabilitiesDaLanguageBindingsItem:
    if value in GET_READER_CAPABILITES_CAPABILITIES_DA_LANGUAGE_BINDINGS_ITEM_VALUES:
        return cast(GetReaderCapabilitesCapabilitiesDaLanguageBindingsItem, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GET_READER_CAPABILITES_CAPABILITIES_DA_LANGUAGE_BINDINGS_ITEM_VALUES!r}")

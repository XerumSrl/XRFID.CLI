from typing import Literal, cast

GetReaderCapabilitesCapabilitiesEndpointTypesSupportedItemAuthenticationTypesSupportedItem = Literal['ANY', 'ANYSAFE', 'BASIC', 'DIGEST', 'DIGEST_IE', 'MTLS', 'NTLM', 'NTLM_WB', 'ONLY', 'TLS']

GET_READER_CAPABILITES_CAPABILITIES_ENDPOINT_TYPES_SUPPORTED_ITEM_AUTHENTICATION_TYPES_SUPPORTED_ITEM_VALUES: set[GetReaderCapabilitesCapabilitiesEndpointTypesSupportedItemAuthenticationTypesSupportedItem] = { 'ANY', 'ANYSAFE', 'BASIC', 'DIGEST', 'DIGEST_IE', 'MTLS', 'NTLM', 'NTLM_WB', 'ONLY', 'TLS',  }

def check_get_reader_capabilites_capabilities_endpoint_types_supported_item_authentication_types_supported_item(value: str) -> GetReaderCapabilitesCapabilitiesEndpointTypesSupportedItemAuthenticationTypesSupportedItem:
    if value in GET_READER_CAPABILITES_CAPABILITIES_ENDPOINT_TYPES_SUPPORTED_ITEM_AUTHENTICATION_TYPES_SUPPORTED_ITEM_VALUES:
        return cast(GetReaderCapabilitesCapabilitiesEndpointTypesSupportedItemAuthenticationTypesSupportedItem, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GET_READER_CAPABILITES_CAPABILITIES_ENDPOINT_TYPES_SUPPORTED_ITEM_AUTHENTICATION_TYPES_SUPPORTED_ITEM_VALUES!r}")

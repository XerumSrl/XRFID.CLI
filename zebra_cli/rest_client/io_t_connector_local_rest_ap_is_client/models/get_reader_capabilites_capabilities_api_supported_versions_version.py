from typing import Literal, cast

GetReaderCapabilitesCapabilitiesApiSupportedVersionsVersion = Literal['v1']

GET_READER_CAPABILITES_CAPABILITIES_API_SUPPORTED_VERSIONS_VERSION_VALUES: set[GetReaderCapabilitesCapabilitiesApiSupportedVersionsVersion] = { 'v1',  }

def check_get_reader_capabilites_capabilities_api_supported_versions_version(value: str) -> GetReaderCapabilitesCapabilitiesApiSupportedVersionsVersion:
    if value in GET_READER_CAPABILITES_CAPABILITIES_API_SUPPORTED_VERSIONS_VERSION_VALUES:
        return cast(GetReaderCapabilitesCapabilitiesApiSupportedVersionsVersion, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GET_READER_CAPABILITES_CAPABILITIES_API_SUPPORTED_VERSIONS_VERSION_VALUES!r}")

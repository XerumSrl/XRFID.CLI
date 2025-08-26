from typing import Literal, cast

SupportedStandardListRegion = Literal['Argentina']

SUPPORTED_STANDARD_LIST_REGION_VALUES: set[SupportedStandardListRegion] = { 'Argentina',  }

def check_supported_standard_list_region(value: str) -> SupportedStandardListRegion:
    if value in SUPPORTED_STANDARD_LIST_REGION_VALUES:
        return cast(SupportedStandardListRegion, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {SUPPORTED_STANDARD_LIST_REGION_VALUES!r}")

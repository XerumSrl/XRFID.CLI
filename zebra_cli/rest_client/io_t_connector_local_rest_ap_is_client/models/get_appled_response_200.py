from typing import Literal, cast

GetAppledResponse200 = Literal['DEFAULT', 'NON_DEFAULT']

GET_APPLED_RESPONSE_200_VALUES: set[GetAppledResponse200] = { 'DEFAULT', 'NON_DEFAULT',  }

def check_get_appled_response_200(value: str) -> GetAppledResponse200:
    if value in GET_APPLED_RESPONSE_200_VALUES:
        return cast(GetAppledResponse200, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GET_APPLED_RESPONSE_200_VALUES!r}")

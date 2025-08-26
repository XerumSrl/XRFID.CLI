from typing import Literal, cast

GetGpiStatusResponse2001 = Literal['HIGH', 'LOW']

GET_GPI_STATUS_RESPONSE_2001_VALUES: set[GetGpiStatusResponse2001] = { 'HIGH', 'LOW',  }

def check_get_gpi_status_response_2001(value: str) -> GetGpiStatusResponse2001:
    if value in GET_GPI_STATUS_RESPONSE_2001_VALUES:
        return cast(GetGpiStatusResponse2001, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GET_GPI_STATUS_RESPONSE_2001_VALUES!r}")

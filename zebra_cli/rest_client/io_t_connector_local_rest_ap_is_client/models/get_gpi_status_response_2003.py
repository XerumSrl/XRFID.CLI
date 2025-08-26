from typing import Literal, cast

GetGpiStatusResponse2003 = Literal['HIGH', 'LOW']

GET_GPI_STATUS_RESPONSE_2003_VALUES: set[GetGpiStatusResponse2003] = { 'HIGH', 'LOW',  }

def check_get_gpi_status_response_2003(value: str) -> GetGpiStatusResponse2003:
    if value in GET_GPI_STATUS_RESPONSE_2003_VALUES:
        return cast(GetGpiStatusResponse2003, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GET_GPI_STATUS_RESPONSE_2003_VALUES!r}")

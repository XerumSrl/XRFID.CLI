from typing import Literal, cast

GetGpiStatusResponse2002 = Literal['HIGH', 'LOW']

GET_GPI_STATUS_RESPONSE_2002_VALUES: set[GetGpiStatusResponse2002] = { 'HIGH', 'LOW',  }

def check_get_gpi_status_response_2002(value: str) -> GetGpiStatusResponse2002:
    if value in GET_GPI_STATUS_RESPONSE_2002_VALUES:
        return cast(GetGpiStatusResponse2002, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GET_GPI_STATUS_RESPONSE_2002_VALUES!r}")

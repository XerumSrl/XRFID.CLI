from typing import Literal, cast

GetGpoStatusResponse2001 = Literal['HIGH', 'LOW']

GET_GPO_STATUS_RESPONSE_2001_VALUES: set[GetGpoStatusResponse2001] = { 'HIGH', 'LOW',  }

def check_get_gpo_status_response_2001(value: str) -> GetGpoStatusResponse2001:
    if value in GET_GPO_STATUS_RESPONSE_2001_VALUES:
        return cast(GetGpoStatusResponse2001, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GET_GPO_STATUS_RESPONSE_2001_VALUES!r}")

from typing import Literal, cast

GetGpoStatusResponse2004 = Literal['HIGH', 'LOW']

GET_GPO_STATUS_RESPONSE_2004_VALUES: set[GetGpoStatusResponse2004] = { 'HIGH', 'LOW',  }

def check_get_gpo_status_response_2004(value: str) -> GetGpoStatusResponse2004:
    if value in GET_GPO_STATUS_RESPONSE_2004_VALUES:
        return cast(GetGpoStatusResponse2004, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GET_GPO_STATUS_RESPONSE_2004_VALUES!r}")

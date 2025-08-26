from typing import Literal, cast

GetGpoStatusResponse2003 = Literal['HIGH', 'LOW']

GET_GPO_STATUS_RESPONSE_2003_VALUES: set[GetGpoStatusResponse2003] = { 'HIGH', 'LOW',  }

def check_get_gpo_status_response_2003(value: str) -> GetGpoStatusResponse2003:
    if value in GET_GPO_STATUS_RESPONSE_2003_VALUES:
        return cast(GetGpoStatusResponse2003, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GET_GPO_STATUS_RESPONSE_2003_VALUES!r}")

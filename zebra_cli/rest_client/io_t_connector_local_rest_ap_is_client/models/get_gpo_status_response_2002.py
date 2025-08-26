from typing import Literal, cast

GetGpoStatusResponse2002 = Literal['HIGH', 'LOW']

GET_GPO_STATUS_RESPONSE_2002_VALUES: set[GetGpoStatusResponse2002] = { 'HIGH', 'LOW',  }

def check_get_gpo_status_response_2002(value: str) -> GetGpoStatusResponse2002:
    if value in GET_GPO_STATUS_RESPONSE_2002_VALUES:
        return cast(GetGpoStatusResponse2002, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GET_GPO_STATUS_RESPONSE_2002_VALUES!r}")

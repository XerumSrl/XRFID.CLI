from typing import Literal, cast

OsUpdateAuthenticationType = Literal['BASIC', 'NONE']

OS_UPDATE_AUTHENTICATION_TYPE_VALUES: set[OsUpdateAuthenticationType] = { 'BASIC', 'NONE',  }

def check_os_update_authentication_type(value: str) -> OsUpdateAuthenticationType:
    if value in OS_UPDATE_AUTHENTICATION_TYPE_VALUES:
        return cast(OsUpdateAuthenticationType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {OS_UPDATE_AUTHENTICATION_TYPE_VALUES!r}")

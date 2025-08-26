from typing import Literal, cast

AccessType = Literal['ACCESS']

ACCESS_TYPE_VALUES: set[AccessType] = { 'ACCESS',  }

def check_access_type(value: str) -> AccessType:
    if value in ACCESS_TYPE_VALUES:
        return cast(AccessType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {ACCESS_TYPE_VALUES!r}")

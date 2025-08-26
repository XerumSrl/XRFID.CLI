from typing import Literal, cast

WriteType = Literal['WRITE']

WRITE_TYPE_VALUES: set[WriteType] = { 'WRITE',  }

def check_write_type(value: str) -> WriteType:
    if value in WRITE_TYPE_VALUES:
        return cast(WriteType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {WRITE_TYPE_VALUES!r}")

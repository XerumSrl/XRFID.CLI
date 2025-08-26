from typing import Literal, cast

ReadType = Literal['READ']

READ_TYPE_VALUES: set[ReadType] = { 'READ',  }

def check_read_type(value: str) -> ReadType:
    if value in READ_TYPE_VALUES:
        return cast(ReadType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {READ_TYPE_VALUES!r}")

from typing import Literal, cast

LockType = Literal['LOCK']

LOCK_TYPE_VALUES: set[LockType] = { 'LOCK',  }

def check_lock_type(value: str) -> LockType:
    if value in LOCK_TYPE_VALUES:
        return cast(LockType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LOCK_TYPE_VALUES!r}")

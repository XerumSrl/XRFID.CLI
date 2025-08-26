from typing import Literal, cast

KillType = Literal['KILL']

KILL_TYPE_VALUES: set[KillType] = { 'KILL',  }

def check_kill_type(value: str) -> KillType:
    if value in KILL_TYPE_VALUES:
        return cast(KillType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {KILL_TYPE_VALUES!r}")

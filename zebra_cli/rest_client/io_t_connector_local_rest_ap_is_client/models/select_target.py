from typing import Literal, cast

SelectTarget = Literal['S0', 'S1', 'S2', 'S3', 'SL']

SELECT_TARGET_VALUES: set[SelectTarget] = { 'S0', 'S1', 'S2', 'S3', 'SL',  }

def check_select_target(value: str) -> SelectTarget:
    if value in SELECT_TARGET_VALUES:
        return cast(SelectTarget, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {SELECT_TARGET_VALUES!r}")

from typing import Literal, cast

SetAppledColor = Literal['amber', 'green', 'off', 'red']

SET_APPLED_COLOR_VALUES: set[SetAppledColor] = { 'amber', 'green', 'off', 'red',  }

def check_set_appled_color(value: str) -> SetAppledColor:
    if value in SET_APPLED_COLOR_VALUES:
        return cast(SetAppledColor, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {SET_APPLED_COLOR_VALUES!r}")

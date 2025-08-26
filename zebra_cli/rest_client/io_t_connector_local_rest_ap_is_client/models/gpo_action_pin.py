from typing import Literal, cast

GPOActionPin = Literal[1, 2, 3, 4]

GPO_ACTION_PIN_VALUES: set[GPOActionPin] = { 1, 2, 3, 4,  }

def check_gpo_action_pin(value: int) -> GPOActionPin:
    if value in GPO_ACTION_PIN_VALUES:
        return cast(GPOActionPin, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GPO_ACTION_PIN_VALUES!r}")

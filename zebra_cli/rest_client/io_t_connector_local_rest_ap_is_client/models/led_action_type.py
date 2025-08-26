from typing import Literal, cast

LEDActionType = Literal['LED']

LED_ACTION_TYPE_VALUES: set[LEDActionType] = { 'LED',  }

def check_led_action_type(value: str) -> LEDActionType:
    if value in LED_ACTION_TYPE_VALUES:
        return cast(LEDActionType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LED_ACTION_TYPE_VALUES!r}")

from typing import Literal, cast

LEDActionLed = Literal[1, 2, 3]

LED_ACTION_LED_VALUES: set[LEDActionLed] = { 1, 2, 3,  }

def check_led_action_led(value: int) -> LEDActionLed:
    if value in LED_ACTION_LED_VALUES:
        return cast(LEDActionLed, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LED_ACTION_LED_VALUES!r}")

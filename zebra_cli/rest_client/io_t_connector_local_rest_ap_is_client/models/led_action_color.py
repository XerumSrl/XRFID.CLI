from typing import Literal, cast

LEDActionColor = Literal['AMBER', 'GREEN', 'RED']

LED_ACTION_COLOR_VALUES: set[LEDActionColor] = { 'AMBER', 'GREEN', 'RED',  }

def check_led_action_color(value: str) -> LEDActionColor:
    if value in LED_ACTION_COLOR_VALUES:
        return cast(LEDActionColor, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LED_ACTION_COLOR_VALUES!r}")

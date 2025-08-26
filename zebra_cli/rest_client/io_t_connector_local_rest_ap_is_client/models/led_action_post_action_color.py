from typing import Literal, cast

LEDActionPostActionColor = Literal['AMBER', 'GREEN', 'RED']

LED_ACTION_POST_ACTION_COLOR_VALUES: set[LEDActionPostActionColor] = { 'AMBER', 'GREEN', 'RED',  }

def check_led_action_post_action_color(value: str) -> LEDActionPostActionColor:
    if value in LED_ACTION_POST_ACTION_COLOR_VALUES:
        return cast(LEDActionPostActionColor, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LED_ACTION_POST_ACTION_COLOR_VALUES!r}")

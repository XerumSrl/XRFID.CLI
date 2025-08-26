from typing import Literal, cast

GPIOLEDConfigurationLEDDefaults2 = Literal['AMBER', 'GREEN', 'RED']

GPIOLED_CONFIGURATION_LED_DEFAULTS_2_VALUES: set[GPIOLEDConfigurationLEDDefaults2] = { 'AMBER', 'GREEN', 'RED',  }

def check_gpioled_configuration_led_defaults_2(value: str) -> GPIOLEDConfigurationLEDDefaults2:
    if value in GPIOLED_CONFIGURATION_LED_DEFAULTS_2_VALUES:
        return cast(GPIOLEDConfigurationLEDDefaults2, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GPIOLED_CONFIGURATION_LED_DEFAULTS_2_VALUES!r}")

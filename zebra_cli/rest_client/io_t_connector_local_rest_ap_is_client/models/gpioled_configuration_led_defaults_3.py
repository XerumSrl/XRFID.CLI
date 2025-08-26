from typing import Literal, cast

GPIOLEDConfigurationLEDDefaults3 = Literal['AMBER', 'GREEN', 'RED']

GPIOLED_CONFIGURATION_LED_DEFAULTS_3_VALUES: set[GPIOLEDConfigurationLEDDefaults3] = { 'AMBER', 'GREEN', 'RED',  }

def check_gpioled_configuration_led_defaults_3(value: str) -> GPIOLEDConfigurationLEDDefaults3:
    if value in GPIOLED_CONFIGURATION_LED_DEFAULTS_3_VALUES:
        return cast(GPIOLEDConfigurationLEDDefaults3, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GPIOLED_CONFIGURATION_LED_DEFAULTS_3_VALUES!r}")

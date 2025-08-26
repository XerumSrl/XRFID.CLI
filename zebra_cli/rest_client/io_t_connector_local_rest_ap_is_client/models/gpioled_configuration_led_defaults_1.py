from typing import Literal, cast

GPIOLEDConfigurationLEDDefaults1 = Literal['AMBER', 'GREEN', 'RED']

GPIOLED_CONFIGURATION_LED_DEFAULTS_1_VALUES: set[GPIOLEDConfigurationLEDDefaults1] = { 'AMBER', 'GREEN', 'RED',  }

def check_gpioled_configuration_led_defaults_1(value: str) -> GPIOLEDConfigurationLEDDefaults1:
    if value in GPIOLED_CONFIGURATION_LED_DEFAULTS_1_VALUES:
        return cast(GPIOLEDConfigurationLEDDefaults1, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GPIOLED_CONFIGURATION_LED_DEFAULTS_1_VALUES!r}")

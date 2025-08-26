from typing import Literal, cast

GPIOLEDConfigurationGPODefaults2 = Literal['HIGH', 'LOW']

GPIOLED_CONFIGURATION_GPO_DEFAULTS_2_VALUES: set[GPIOLEDConfigurationGPODefaults2] = { 'HIGH', 'LOW',  }

def check_gpioled_configuration_gpo_defaults_2(value: str) -> GPIOLEDConfigurationGPODefaults2:
    if value in GPIOLED_CONFIGURATION_GPO_DEFAULTS_2_VALUES:
        return cast(GPIOLEDConfigurationGPODefaults2, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GPIOLED_CONFIGURATION_GPO_DEFAULTS_2_VALUES!r}")

from typing import Literal, cast

GPIOLEDConfigurationGPODefaults3 = Literal['HIGH', 'LOW']

GPIOLED_CONFIGURATION_GPO_DEFAULTS_3_VALUES: set[GPIOLEDConfigurationGPODefaults3] = { 'HIGH', 'LOW',  }

def check_gpioled_configuration_gpo_defaults_3(value: str) -> GPIOLEDConfigurationGPODefaults3:
    if value in GPIOLED_CONFIGURATION_GPO_DEFAULTS_3_VALUES:
        return cast(GPIOLEDConfigurationGPODefaults3, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GPIOLED_CONFIGURATION_GPO_DEFAULTS_3_VALUES!r}")

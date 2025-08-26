from typing import Literal, cast

GPIOLEDConfigurationGPODefaults1 = Literal['HIGH', 'LOW']

GPIOLED_CONFIGURATION_GPO_DEFAULTS_1_VALUES: set[GPIOLEDConfigurationGPODefaults1] = { 'HIGH', 'LOW',  }

def check_gpioled_configuration_gpo_defaults_1(value: str) -> GPIOLEDConfigurationGPODefaults1:
    if value in GPIOLED_CONFIGURATION_GPO_DEFAULTS_1_VALUES:
        return cast(GPIOLEDConfigurationGPODefaults1, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GPIOLED_CONFIGURATION_GPO_DEFAULTS_1_VALUES!r}")

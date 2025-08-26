from typing import Literal, cast

GPIOLEDConfigurationGPODefaults4 = Literal['HIGH', 'LOW']

GPIOLED_CONFIGURATION_GPO_DEFAULTS_4_VALUES: set[GPIOLEDConfigurationGPODefaults4] = { 'HIGH', 'LOW',  }

def check_gpioled_configuration_gpo_defaults_4(value: str) -> GPIOLEDConfigurationGPODefaults4:
    if value in GPIOLED_CONFIGURATION_GPO_DEFAULTS_4_VALUES:
        return cast(GPIOLEDConfigurationGPODefaults4, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GPIOLED_CONFIGURATION_GPO_DEFAULTS_4_VALUES!r}")

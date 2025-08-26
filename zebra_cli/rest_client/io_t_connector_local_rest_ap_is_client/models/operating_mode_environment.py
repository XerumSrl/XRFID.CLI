from typing import Literal, cast

OperatingModeEnvironment = Literal['AUTO_DETECT', 'DEMO', 'HIGH_INTERFERENCE', 'LOW_INTERFERENCE', 'VERY_HIGH_INTERFERENCE']

OPERATING_MODE_ENVIRONMENT_VALUES: set[OperatingModeEnvironment] = { 'AUTO_DETECT', 'DEMO', 'HIGH_INTERFERENCE', 'LOW_INTERFERENCE', 'VERY_HIGH_INTERFERENCE',  }

def check_operating_mode_environment(value: str) -> OperatingModeEnvironment:
    if value in OPERATING_MODE_ENVIRONMENT_VALUES:
        return cast(OperatingModeEnvironment, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {OPERATING_MODE_ENVIRONMENT_VALUES!r}")

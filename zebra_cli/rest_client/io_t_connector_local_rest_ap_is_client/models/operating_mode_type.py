from typing import Literal, cast

OperatingModeType = Literal['CONVEYOR', 'CUSTOM', 'DIRECTIONALITY', 'INVENTORY', 'PORTAL', 'SIMPLE']

OPERATING_MODE_TYPE_VALUES: set[OperatingModeType] = { 'CONVEYOR', 'CUSTOM', 'DIRECTIONALITY', 'INVENTORY', 'PORTAL', 'SIMPLE',  }

def check_operating_mode_type(value: str) -> OperatingModeType:
    if value in OPERATING_MODE_TYPE_VALUES:
        return cast(OperatingModeType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {OPERATING_MODE_TYPE_VALUES!r}")

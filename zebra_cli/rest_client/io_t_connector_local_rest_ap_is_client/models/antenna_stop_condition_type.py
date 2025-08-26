from typing import Literal, cast

AntennaStopConditionType = Literal['DURATION', 'GPI', 'INVENTORY_COUNT', 'SINGLE_INVENTORY_LIMITED_DURATION']

ANTENNA_STOP_CONDITION_TYPE_VALUES: set[AntennaStopConditionType] = { 'DURATION', 'GPI', 'INVENTORY_COUNT', 'SINGLE_INVENTORY_LIMITED_DURATION',  }

def check_antenna_stop_condition_type(value: str) -> AntennaStopConditionType:
    if value in ANTENNA_STOP_CONDITION_TYPE_VALUES:
        return cast(AntennaStopConditionType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {ANTENNA_STOP_CONDITION_TYPE_VALUES!r}")

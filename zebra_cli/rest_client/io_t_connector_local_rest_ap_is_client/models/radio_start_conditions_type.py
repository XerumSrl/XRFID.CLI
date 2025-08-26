from typing import Literal, cast

RadioStartConditionsType = Literal['GPI', 'GPI_WITH_RESTART']

RADIO_START_CONDITIONS_TYPE_VALUES: set[RadioStartConditionsType] = { 'GPI', 'GPI_WITH_RESTART',  }

def check_radio_start_conditions_type(value: str) -> RadioStartConditionsType:
    if value in RADIO_START_CONDITIONS_TYPE_VALUES:
        return cast(RadioStartConditionsType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {RADIO_START_CONDITIONS_TYPE_VALUES!r}")

from typing import Literal, cast

DelayBetweenAntennaCyclesType = Literal['DISABLED', 'NO_TAGS', 'NO_UNIQUE_TAGS']

DELAY_BETWEEN_ANTENNA_CYCLES_TYPE_VALUES: set[DelayBetweenAntennaCyclesType] = { 'DISABLED', 'NO_TAGS', 'NO_UNIQUE_TAGS',  }

def check_delay_between_antenna_cycles_type(value: str) -> DelayBetweenAntennaCyclesType:
    if value in DELAY_BETWEEN_ANTENNA_CYCLES_TYPE_VALUES:
        return cast(DelayBetweenAntennaCyclesType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DELAY_BETWEEN_ANTENNA_CYCLES_TYPE_VALUES!r}")

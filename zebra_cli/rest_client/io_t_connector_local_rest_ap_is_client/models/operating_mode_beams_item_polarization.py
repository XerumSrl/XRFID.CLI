from typing import Literal, cast

OperatingModeBeamsItemPolarization = Literal['LHCP', 'PHI', 'RHCP', 'THETA', 'TOTAL']

OPERATING_MODE_BEAMS_ITEM_POLARIZATION_VALUES: set[OperatingModeBeamsItemPolarization] = { 'LHCP', 'PHI', 'RHCP', 'THETA', 'TOTAL',  }

def check_operating_mode_beams_item_polarization(value: str) -> OperatingModeBeamsItemPolarization:
    if value in OPERATING_MODE_BEAMS_ITEM_POLARIZATION_VALUES:
        return cast(OperatingModeBeamsItemPolarization, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {OPERATING_MODE_BEAMS_ITEM_POLARIZATION_VALUES!r}")

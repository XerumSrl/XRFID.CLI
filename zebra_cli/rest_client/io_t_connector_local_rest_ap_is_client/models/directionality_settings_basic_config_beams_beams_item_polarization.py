from typing import Literal, cast

DirectionalitySettingsBasicConfigBeamsBeamsItemPolarization = Literal['LHCP', 'PHI', 'RHCP', 'THETA', 'TOTAL']

DIRECTIONALITY_SETTINGS_BASIC_CONFIG_BEAMS_BEAMS_ITEM_POLARIZATION_VALUES: set[DirectionalitySettingsBasicConfigBeamsBeamsItemPolarization] = { 'LHCP', 'PHI', 'RHCP', 'THETA', 'TOTAL',  }

def check_directionality_settings_basic_config_beams_beams_item_polarization(value: str) -> DirectionalitySettingsBasicConfigBeamsBeamsItemPolarization:
    if value in DIRECTIONALITY_SETTINGS_BASIC_CONFIG_BEAMS_BEAMS_ITEM_POLARIZATION_VALUES:
        return cast(DirectionalitySettingsBasicConfigBeamsBeamsItemPolarization, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DIRECTIONALITY_SETTINGS_BASIC_CONFIG_BEAMS_BEAMS_ITEM_POLARIZATION_VALUES!r}")

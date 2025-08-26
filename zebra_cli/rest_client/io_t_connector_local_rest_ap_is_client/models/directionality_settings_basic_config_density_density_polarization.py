from typing import Literal, cast

DirectionalitySettingsBasicConfigDensityDensityPolarization = Literal['LHCP', 'PHI', 'RHCP', 'THETA', 'TOTAL']

DIRECTIONALITY_SETTINGS_BASIC_CONFIG_DENSITY_DENSITY_POLARIZATION_VALUES: set[DirectionalitySettingsBasicConfigDensityDensityPolarization] = { 'LHCP', 'PHI', 'RHCP', 'THETA', 'TOTAL',  }

def check_directionality_settings_basic_config_density_density_polarization(value: str) -> DirectionalitySettingsBasicConfigDensityDensityPolarization:
    if value in DIRECTIONALITY_SETTINGS_BASIC_CONFIG_DENSITY_DENSITY_POLARIZATION_VALUES:
        return cast(DirectionalitySettingsBasicConfigDensityDensityPolarization, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DIRECTIONALITY_SETTINGS_BASIC_CONFIG_DENSITY_DENSITY_POLARIZATION_VALUES!r}")

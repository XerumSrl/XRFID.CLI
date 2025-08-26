from typing import Literal, cast

DirectionalitySettingsBasicConfigDensityDensityType = Literal['DEFAULT', 'DENSE', 'SPARSE']

DIRECTIONALITY_SETTINGS_BASIC_CONFIG_DENSITY_DENSITY_TYPE_VALUES: set[DirectionalitySettingsBasicConfigDensityDensityType] = { 'DEFAULT', 'DENSE', 'SPARSE',  }

def check_directionality_settings_basic_config_density_density_type(value: str) -> DirectionalitySettingsBasicConfigDensityDensityType:
    if value in DIRECTIONALITY_SETTINGS_BASIC_CONFIG_DENSITY_DENSITY_TYPE_VALUES:
        return cast(DirectionalitySettingsBasicConfigDensityDensityType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DIRECTIONALITY_SETTINGS_BASIC_CONFIG_DENSITY_DENSITY_TYPE_VALUES!r}")

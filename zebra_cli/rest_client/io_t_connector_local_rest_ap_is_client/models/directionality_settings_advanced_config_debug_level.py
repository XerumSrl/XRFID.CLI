from typing import Literal, cast

DirectionalitySettingsAdvancedConfigDebugLevel = Literal['DEBUG', 'ERROR', 'INFO', 'WARNING']

DIRECTIONALITY_SETTINGS_ADVANCED_CONFIG_DEBUG_LEVEL_VALUES: set[DirectionalitySettingsAdvancedConfigDebugLevel] = { 'DEBUG', 'ERROR', 'INFO', 'WARNING',  }

def check_directionality_settings_advanced_config_debug_level(value: str) -> DirectionalitySettingsAdvancedConfigDebugLevel:
    if value in DIRECTIONALITY_SETTINGS_ADVANCED_CONFIG_DEBUG_LEVEL_VALUES:
        return cast(DirectionalitySettingsAdvancedConfigDebugLevel, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DIRECTIONALITY_SETTINGS_ADVANCED_CONFIG_DEBUG_LEVEL_VALUES!r}")

from typing import Literal, cast

DirectionalitySettingsBasicConfigZonePlan = Literal[4, 6]

DIRECTIONALITY_SETTINGS_BASIC_CONFIG_ZONE_PLAN_VALUES: set[DirectionalitySettingsBasicConfigZonePlan] = { 4, 6,  }

def check_directionality_settings_basic_config_zone_plan(value: int) -> DirectionalitySettingsBasicConfigZonePlan:
    if value in DIRECTIONALITY_SETTINGS_BASIC_CONFIG_ZONE_PLAN_VALUES:
        return cast(DirectionalitySettingsBasicConfigZonePlan, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DIRECTIONALITY_SETTINGS_BASIC_CONFIG_ZONE_PLAN_VALUES!r}")

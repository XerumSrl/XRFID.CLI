from typing import Literal, cast

DirectionalitySettingsAdvancedConfigReportDirectionItem = Literal['ERROR', 'IN', 'NONE', 'OUT', 'UNKNOWN']

DIRECTIONALITY_SETTINGS_ADVANCED_CONFIG_REPORT_DIRECTION_ITEM_VALUES: set[DirectionalitySettingsAdvancedConfigReportDirectionItem] = { 'ERROR', 'IN', 'NONE', 'OUT', 'UNKNOWN',  }

def check_directionality_settings_advanced_config_report_direction_item(value: str) -> DirectionalitySettingsAdvancedConfigReportDirectionItem:
    if value in DIRECTIONALITY_SETTINGS_ADVANCED_CONFIG_REPORT_DIRECTION_ITEM_VALUES:
        return cast(DirectionalitySettingsAdvancedConfigReportDirectionItem, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DIRECTIONALITY_SETTINGS_ADVANCED_CONFIG_REPORT_DIRECTION_ITEM_VALUES!r}")

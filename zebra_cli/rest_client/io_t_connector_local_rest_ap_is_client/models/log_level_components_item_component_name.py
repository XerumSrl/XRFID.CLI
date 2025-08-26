from typing import Literal, cast

LogLevelComponentsItemComponentName = Literal['cloud_agent', 'radio_control']

LOG_LEVEL_COMPONENTS_ITEM_COMPONENT_NAME_VALUES: set[LogLevelComponentsItemComponentName] = { 'cloud_agent', 'radio_control',  }

def check_log_level_components_item_component_name(value: str) -> LogLevelComponentsItemComponentName:
    if value in LOG_LEVEL_COMPONENTS_ITEM_COMPONENT_NAME_VALUES:
        return cast(LogLevelComponentsItemComponentName, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LOG_LEVEL_COMPONENTS_ITEM_COMPONENT_NAME_VALUES!r}")

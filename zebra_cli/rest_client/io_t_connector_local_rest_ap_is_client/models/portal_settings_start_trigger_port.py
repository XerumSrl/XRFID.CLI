from typing import Literal, cast

PortalSettingsStartTriggerPort = Literal[1, 2, 3, 4]

PORTAL_SETTINGS_START_TRIGGER_PORT_VALUES: set[PortalSettingsStartTriggerPort] = { 1, 2, 3, 4,  }

def check_portal_settings_start_trigger_port(value: int) -> PortalSettingsStartTriggerPort:
    if value in PORTAL_SETTINGS_START_TRIGGER_PORT_VALUES:
        return cast(PortalSettingsStartTriggerPort, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PORTAL_SETTINGS_START_TRIGGER_PORT_VALUES!r}")
